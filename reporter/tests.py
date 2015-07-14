from django.test import TestCase
from reporter.models import Template, Rendering
import os


_rmd_path = lambda x: os.path.join(os.path.dirname(__file__), 'rmd_templates', x)


class TestRendering(TestCase):

    def test_render(self):
        path = _rmd_path('simple.Rmd')
        t = Template.create(path)

        r = Rendering.objects.create(template=t)
        r.render()
        self.assertTrue(r.md.strip().endswith('2'))

    def test_url(self):
        path = _rmd_path('baseball.Rmd')
        t = Template.create(path)

        url = 'http://www.calvin.edu/~stob/data/bballgames03.csv'
        r = Rendering.objects.create(template=t, url=url)
        r.render()
        self.assertTrue(r.md.startswith('[1] 2430'))

    def test_warning(self):
        path = _rmd_path('warning.Rmd')
        t = Template.create(path)

        r = Rendering.objects.create(template=t)
        r.render()
        self.assertEqual(r.md.strip(), 'WARNING: Need more data.')
