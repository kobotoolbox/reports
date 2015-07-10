from django.test import TestCase
from reporter.models import Template, Rendering, User
import os


class TestRendering(TestCase):

    def test_render(self):
        path = os.path.join(os.path.dirname(__file__), 'simple.Rmd')
        with open(path) as f:
            rmd = f.read()
        t = Template.objects.create(rmd=rmd, name='simple')

        u = User.objects.create(username='bob')
        r = Rendering.objects.create(user=u, template=t, data='')

        r.render()
        self.assertTrue(r.md.strip().endswith('2'))
