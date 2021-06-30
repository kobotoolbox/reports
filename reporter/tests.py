from django.test import TestCase
from reporter.models import Template, Rendering
import os
import re
import pandas as pd
from io import StringIO


_rmd_path = lambda x: os.path.join(os.path.dirname(__file__), 'rmd_templates', x)


class TestRendering(TestCase):

    def test_render(self):
        path = _rmd_path('simple.Rmd')
        t = Template.create(path)

        r = Rendering.objects.create(template=t)
        output = r.render('md')
        self.assertEqual(
            output.strip().decode('utf-8'), 'What is one plus one? 2'
        )

        for ext in ['html', 'pdf', 'docx']:
            output = r.render(ext)

    def test_url(self):
        '''
        When rendering a template, if we set the url field then the
        csv file found at the url will be loaded into a data.frame
        called `data` and will be made available to the
        template. Below is a small example using a csv file containing
        2,430 baseball games.
        '''
        rmarkdown = '`r nrow(data)`\n'
        t = Template.objects.create(rmd=rmarkdown, slug='n_observations')
        # url = 'http://www.calvin.edu/~stob/data/bballgames03.csv'
        url = 'http://web.archive.org/web/20191230231342if_/http://www.calvin.edu:80/~stob/data/bballgames03.csv'
        r = Rendering.objects.create(template=t, url=url)
        # Hack to bypass KoBo URL validity check
        r._test_non_kobo_csv = True
        output = r.render('md')
        self.assertEqual(int(output), 2430)

    def test_warning(self):
        '''
        {{#introduction}}
        By using both the `knitr` and `whisker` libraries together, I
        have added support for Mustache tags. This will allow us to
        present users with a warning message if they have not
        collected enough data yet.

        To demostrate this functionality, this test will use this
        docstring as an rmarkdown template, render the template, and
        show that this section of the report will be hidden because
        the variable `introduction` is set to FALSE.
        {{/introduction}}

        {{#warning}}
        ```{r, echo=FALSE, results='asis'}
        warning <- TRUE
        if (warning) {
          cat('WARNING: Need more data.')
          introduction <- FALSE
        }
        ```
        {{/warning}}
        '''
        above_doc_string = self.test_warning.__doc__
        lines = re.split('\s*\n\s*', above_doc_string)
        rmarkdown = '\n'.join(lines)
        t = Template.objects.create(rmd=rmarkdown, slug='warning')
        r = Rendering.objects.create(template=t)
        output = r.render('md')
        self.assertEqual(
            output.strip().decode('utf-8'), 'WARNING: Need more data.'
        )
