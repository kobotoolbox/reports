from django.db import models
from django.contrib.auth.models import User
import tempfile
import os
import subprocess
import django


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

    def context(self):
        return {'url': self.url}

    def render(self):
        folder = tempfile.gettempdir()
        filename = '%s.Rmd' % self.template.name

        path = os.path.join(folder, filename)
        t = django.template.Template(self.template.rmd)
        rmd = t.render(django.template.Context(self.context()))
        with open(path, 'w') as f:
            f.write(rmd)

        r_commands = [
            'library(knitr)',
            # 'opts_chunk\\$set(error=FALSE, warning=FALSE)',
            "knit2html('%(filename)s', quiet=TRUE)" % locals(),
        ]
        l = map(lambda s: '-e "%s"' % s, r_commands)
        cmd = ' '.join(['Rscript'] + l)
        retcode = subprocess.call(cmd, shell=True, cwd=folder)

        for extension in ['md', 'html']:
            path = os.path.join(folder, self.template.name + '.' + extension)
            with open(path) as f:
                text = f.read()
                setattr(self, extension, text)

        self.save()
