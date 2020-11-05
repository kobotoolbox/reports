from django.test import TestCase
from reporter.models import Template, Rendering
import os
import re
import pandas as pd
from StringIO import StringIO


_rmd_path = lambda x: os.path.join(os.path.dirname(__file__), 'rmd_templates', x)


class TestRendering(TestCase):

    # These are associated with the m4m_testing account on
    # kf.kobotoolbox.org
    API_TOKEN = '9b751c0ae200d2f2a82a05f6af510baffe1b4c83'
    FORMID = 25320

    def test_render(self):
        path = _rmd_path('simple.Rmd')
        t = Template.create(path)

        r = Rendering.objects.create(template=t)
        output = r.render('md')
        self.assertTrue(output.strip().endswith('2'))

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
        self.assertEqual(output.strip(), 'WARNING: Need more data.')
'''
    def test_kobo_api(self):
        url = 'https://kc.kobotoolbox.org/api/v1/data/%d.csv' % self.FORMID
        t = Template.objects.create(rmd='`r class(data)`\n', slug='n')
        r = Rendering.objects.create(template=t, url=url, api_token=self.API_TOKEN)
        output = r.render('md')
        self.assertEquals(output.strip(), 'data.frame')

    def test_get_new_data(self):
        my_split = lambda s: re.split('[\n\r]+', s)

        url = 'https://kc.kobotoolbox.org/api/v1/data/%d?format=csv' % self.FORMID
        t = Template.objects.create(rmd='`r class(data)`\n', slug='n')
        r = Rendering.objects.create(template=t, url=url, api_token=self.API_TOKEN)
        r.download_data()

        # keep only the first submission
        lines = my_split(r.data)
        nlines = len(lines)
        df = pd.DataFrame.from_csv(StringIO(r.data), index_col=None)
        i = df.index[df._submission_time == df._submission_time.min()].min() + 1
        r.data = '\n'.join([lines[0], lines[i]])
        r.save()

        # test downloading new data
        new_data = r._get_new_data()
        new_lines = my_split(new_data)
        self.assertEqual(len(new_lines), nlines - 1)

        r.download_data()
        self.assertEquals(set(my_split(r.data)), set(lines))
    def test_google_spreadsheet(self):
        rmd = '`r nrow(data)` rows.\n'
        t = Template.objects.create(rmd=rmd, slug='rows')
        url = (
            'http://docs.google.com/spreadsheets/d/'
            '1n59I4NMc4ykYW540sIFnbo10fZRDdrhBbora_oDSZdY/'
            'export?hl&exportFormat=csv'
        )
        r = Rendering.objects.create(template=t, url=url)
        output = r.render('md')
        match = re.search('^\d+ rows\.', output)
        self.assertTrue(match)
'''
