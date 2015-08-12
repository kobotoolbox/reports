from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import tempfile
import os
import subprocess
import requests


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
    api_token = models.TextField(blank=True)

    def download_data(self):
        headers = {}
        if self.api_token is not None:
            headers['Authorization'] = 'Token %s' % self.api_token
        response = requests.get(self.url, headers=headers)
        self.data = response.content

    def render(self):
        folder = tempfile.gettempdir()
        filename = '%s.Rmd' % self.template.name
        path = os.path.join(folder, filename)

        with open(path, 'w') as f:
            f.write(self.template.rmd)

        if self.url:
            self.download_data()
            data_csv = os.path.join(folder, 'data.csv')
            with open(data_csv, 'w') as f:
                f.write(self.data)

        context = {'filename': filename, 'url': self.url}
        script = render_to_string('compile.R', context)
        path = os.path.join(folder, 'temp.R')
        with open(path, 'w') as f:
            f.write(script)

        cmd = 'Rscript temp.R > temp.log'
        retcode = subprocess.call(cmd, shell=True, cwd=folder)
        if retcode != 0:
            path = os.path.join(folder, 'temp.log')
            raise Exception(path)

        results = {}
        for extension in ['md', 'html', 'pdf', 'docx']:
            path = os.path.join(folder, self.template.name + '.' + extension)
            with open(path) as f:
                results[extension] = f.read()

        return results
