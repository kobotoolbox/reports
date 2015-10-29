from StringIO import StringIO
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from django.conf import settings
from urlparse import urlparse
import json
import os
import pandas as pd
import requests
import subprocess
import tempfile
import logging


logger = logging.getLogger('TIMING')


class UserExternalApiToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='external_api_token')
    key = models.CharField(max_length=120)


class Template(models.Model):
    ''' Global R Markdown templates. Available read-only to all users, but
    require model-level permissions or superuser access to modify '''
    rmd = models.TextField()
    slug = models.SlugField(default='', unique=True)
    name = models.TextField(default='')

    @classmethod
    def create(cls, path):
        with open(path) as f:
            rmd = f.read()
        l = os.path.split(path)
        name, ext = os.path.splitext(l[-1])
        return cls.objects.create(rmd=rmd, slug=name)

    def __unicode__(self):
        return self.slug


class Rendering(models.Model):
    ''' Retrieves data from KoBoCAT and processes it through a Template. The
    data comes from KoBoCAT XForms, which KC calls "forms" in the API and
    "projects" in the UI '''
    user = models.ForeignKey(User, null=True, editable=False, related_name='renderings')
    template = models.ForeignKey(Template)
    url = models.URLField(blank=True)
    name = models.TextField(default='')
    # Getting this requires a slow API call, so store it in our local DB
    _enter_data_link = models.URLField(blank=True)

    data = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def submission_count(self):
        lines = self.data.split('\n')
        return len(lines) - 1

    def __unicode__(self):
        return unicode(self.id)

    @classmethod
    def _get_csv(cls, *args, **kwargs):
        response = requests.get(*args, **kwargs)
        text = response.content
        return text.strip()

    @property
    def api_token(self):
        if self.user is None:
            return None
        try:
            return self.user.external_api_token.key
        except UserExternalApiToken.DoesNotExist:
            return None

    def download_data(self):
        if not self.api_token:
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
        new_data = self._get_new_data()
        if new_data:
            new_lines = new_data.split('\n')
            combined_lines = new_lines + old_lines[1:len(old_lines)]
            self.data = '\n'.join(combined_lines)

    def _get_new_data(self):
        f = StringIO(self.data)
        df = pd.DataFrame.from_csv(f, index_col=None)
        last_submission = df['_submission_time'].max()
        url = self.url
        headers = {'Authorization': 'Token %s' % self.api_token}
        query = {"_submission_time": {"$gt": str(last_submission)}}
        params = {
            'format': 'csv',
            'query': json.dumps(query)
        }
        response = requests.get(url=url, headers=headers, params=params)
        return response.text.strip()

    def _log_message(self, msg):
        full_msg = '<Rendering: %s> | %s' % (str(self), msg)
        logger.info(full_msg)

    def render(self, extension):
        self._log_message('render begin  ')
        folder = tempfile.gettempdir()
        filename = '%s.Rmd' % self.template.slug
        path = os.path.join(folder, filename)

        with open(path, 'w') as f:
            f.write(self.template.rmd)

        if self.url:
            self._log_message('download begin')
            self.download_data()
            self._log_message('download end  ')
            data_csv = os.path.join(folder, 'data.csv')
            if not self.data.endswith('\n'):
                self.data += '\n'
            with open(data_csv, 'w') as f:
                f.write(self.data.encode('utf-8'))

        context = {'filename': filename, 'url': self.url, 'extension': extension}
        script = render_to_string('compile.R', context)
        path = os.path.join(folder, 'temp.R')
        with open(path, 'w') as f:
            f.write(script)

        cmd = 'Rscript temp.R > temp.log'
        retcode = subprocess.call(cmd, shell=True, cwd=folder)
        if retcode != 0:
            path = os.path.join(folder, 'temp.log')
            raise Exception(path)

        path = os.path.join(folder, self.template.slug + '.' + extension)
        with open(path) as f:
            result = f.read()

        self._log_message('render end    ')
        return result

    def _get_kc_form_data(self, endpoint='/forms/{pk}'):
        ''' Attempt to extract the ID from `self.url`, then query KC to
        retrieve data about the form. The extracted ID is available within the
        optional ``endpoint`` parameter as `{pk}`. '''
        # Assume the numeric ID is the last component of the URL path before
        # the query string
        parsed_url = urlparse(self.url)
        numeric_id = int(parsed_url.path.split('/')[-1])
        form_url = '{}://{}/api/v1{}?format=json'.format(
            parsed_url.scheme,
            parsed_url.netloc,
            endpoint.format(pk=numeric_id),
        )
        headers = {}
        if self.api_token:
            headers['Authorization'] = 'Token {}'.format(self.api_token)
        response = requests.get(form_url, headers=headers)
        return json.loads(response.content)

    @property
    def enter_data_link(self):
        ''' Return the Enketo data-entry link, retrieving it from KC if
        necessary '''
        if not len(self._enter_data_link):
            form_data = self._get_kc_form_data(endpoint='/forms/{pk}/enketo')
            self._enter_data_link = form_data['enketo_url']
            self.save(update_fields=['_enter_data_link'])
        return self._enter_data_link
