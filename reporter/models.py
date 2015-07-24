from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import tempfile
import os
import subprocess


class Template(models.Model):
    rmd = models.TextField()
    name = models.TextField()

    @classmethod
    def create(cls, path):
        with open(path) as f:
            rmd = f.read()
        l = os.path.split(path)
        name, ext = os.path.splitext(l[-1])
        return cls.objects.create(rmd=rmd, name=name)


class Rendering(models.Model):
    # I'm putting a user here because each rendering may access
    # private data that relies on the user for authentication.
    user = models.ForeignKey(User, null=True, blank=True)
    template = models.ForeignKey(Template)
    url = models.URLField(blank=True)
    md = models.TextField(editable=False)
    html = models.TextField(editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def render(self):
        folder = tempfile.gettempdir()
        filename = '%s.Rmd' % self.template.name
        path = os.path.join(folder, filename)

        with open(path, 'w') as f:
            f.write(self.template.rmd)

        context = {'filename': filename, 'url': self.url}
        script = render_to_string('compile.R', context)
        path = os.path.join(folder, 'temp.R')
        with open(path, 'w') as f:
            f.write(script)

        cmd = 'Rscript temp.R'
        retcode = subprocess.call(cmd, shell=True, cwd=folder)

        results = {}
        for extension in ['md', 'html', 'pdf', 'docx']:
            path = os.path.join(folder, self.template.name + '.' + extension)
            with open(path) as f:
                results[extension] = f.read()

        return results
