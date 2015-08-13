from StringIO import StringIO
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
import json
import os
import pandas as pd
import requests
import subprocess
import tempfile


class Template(models.Model):
    user = models.ForeignKey(User, null=True)
    rmd = models.TextField()
    slug = models.SlugField(default='')

    @classmethod
    def create(cls, path):
        with open(path) as f:
            rmd = f.read()
        l = os.path.split(path)
        name, ext = os.path.splitext(l[-1])
        return cls.objects.create(rmd=rmd, slug=name)


class Rendering(models.Model):
    user = models.ForeignKey(User, null=True)
    template = models.ForeignKey(Template)
    url = models.URLField(blank=True)
    api_token = models.TextField(blank=True)
    data = models.TextField(default='')

    @classmethod
    def _get_csv(cls, *args, **kwargs):
        response = requests.get(*args, **kwargs)
        text = response.content
        return text.strip()

    def download_data(self):
        if self.api_token is None:
            self.data = self._get_csv(self.url)
        elif self.data:
            self._download_new_data()
        else:
            headers = {
                'Authorization': 'Token %s' % self.api_token
            }
            self.data = self._get_csv(self.url, headers=headers)
        self.save()

    def _download_new_data(self):
        old_lines = self.data.split('\n')
        new_lines = self._get_new_data().split('\n')
        combined_lines = new_lines + old_lines[1:len(old_lines)]
        self.data = '\n'.join(combined_lines)

    def _get_new_data(self):
        f = StringIO(self.data)
        df = pd.DataFrame.from_csv(f, index_col=None)
        last_submission = df['_submission_time'].max()

        query = json.dumps({
            '_submission_time': {'$gt': last_submission}
        })
        url = self.url
        full_url = '%(url)s&query=%(query)s' % locals()

        options = '--silent --globoff --insecure'
        api_token = self.api_token
        cmd = "curl %(options)s -X GET '%(full_url)s' -H 'Authorization: Token %(api_token)s'" % locals()
        text = subprocess.check_output(cmd, shell=True)
        return text.strip()

    def render(self):
        folder = tempfile.gettempdir()
        filename = '%s.Rmd' % self.template.slug
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
            path = os.path.join(folder, self.template.slug + '.' + extension)
            with open(path) as f:
                results[extension] = f.read()

        return results
