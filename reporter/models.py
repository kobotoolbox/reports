from StringIO import StringIO
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from django.conf import settings
from urlparse import urlparse
from requests.exceptions import HTTPError
import json
import os
import pandas as pd
import requests
import subprocess
import tempfile
import logging
import datetime
import dateutil


logger = logging.getLogger('TIMING')


class NotFoundInFormBuilder(Exception):
    pass


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

    # Store the name and primary key of the associated `Form` to ease
    # reporting. Avoid using a `ForeignKey` since this data should not be
    # subject to referential integrity checks
    form_name = models.CharField(max_length=255, blank=True)
    form_pk = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'name')

    def submission_count(self):
        lines = self.data.split('\n')
        return len(lines) - 1

    def __unicode__(self):
        return unicode(self.id)

    @staticmethod
    def _csv_from_response(response):
        # Raise exception if status code does not indicate success
        response.raise_for_status()
        stripped_content = response.content.strip()
        # An empty response is expected when there's no data, but Pandas won't
        # tolerate it
        if len(stripped_content):
            # Quasi-validate the CSV by trying to parse it with Pandas
            pd.DataFrame.from_csv(StringIO(response.content), index_col=None)
        return stripped_content

    @classmethod
    def _get_csv(cls, *args, **kwargs):
        response = requests.get(*args, **kwargs)
        return cls._csv_from_response(response)

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
        return self._csv_from_response(response)
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

    def _get_kc_endpoint_url(self, endpoint):
        parsed_url = urlparse(self.url)
        return '{}://{}/api/v1/{}'.format(
            parsed_url.scheme,
            parsed_url.netloc,
            endpoint
        )

    @property
    def _kc_pk(self):
        # Assume the numeric ID is the last component of the URL path before
        # the query string
        parsed_url = urlparse(self.url)
        return int(parsed_url.path.split('/')[-1])

    def _token_auth_request(self, method, url):
        ''' Make a request to KC or KPI, using the associated user's token to
        authenticate.  '''
        headers = {}
        if self.api_token:
            headers['Authorization'] = 'Token {}'.format(self.api_token)
        response = requests.request(method, url, headers=headers)
        return response

    def delete_from_kc_and_kpi(self):
        ''' Delete the corresponding KC form and KPI asset, if any exists '''
        # KPI must be deleted first, because `find_in_form_builder()` depends
        # upon the KC form still existing
        try:
            kpi_asset_uid = self.find_in_form_builder(attempt_create=False)
        except NotFoundInFormBuilder:
            # Don't fail if we can't locate a corresponding KPI asset
            pass
        else:
            # Without `?format=json`, KPI will return 200 instead of 204 after
            # successful deletion
            kpi_asset_url = '{kpi_url}assets/{asset_uid}/?format=json'.format(
                kpi_url=settings.KPI_URL,
                asset_uid=kpi_asset_uid
            )
            kpi_response = self._token_auth_request('delete', kpi_asset_url)
            # Yes, we found a corresponding asset, but let's not create a race
            # condition by assuming it'll still be there when we go to delete
            # it
            if kpi_response.status_code not in (204, 404):
                raise Exception(
                    'Unexpected status code {} returned by KPI'.format(
                        kpi_response.status_code)
                )

        # Delete any extant KC form
        kc_response = self._token_auth_request(
            'delete',
            # If you include a trailing slash after the pk, KC will reject the
            # request with a 403. Isn't that fun?
            self._get_kc_endpoint_url(
                'forms/{}?format=json'.format(self._kc_pk))
        )
        # Tolerating a 404 is the right thing to do if a user already deleted
        # the project from KC, but it runs the risk of masking programming
        # errors --jnm
        if kc_response.status_code not in (204, 404):
            raise Exception('Unexpected status code {} returned by KC'.format(
                kc_response.status_code))

    @property
    def enter_data_link(self):
        ''' Return the Enketo data-entry link, retrieving it from KC if
        necessary '''
        VALUE_TO_RETURN_ON_FAILURE = u''
        if not len(self._enter_data_link):
            kc_response = self._token_auth_request(
                'get',
                self._get_kc_endpoint_url(
                    'forms/{}/enketo?format=json'.format(self._kc_pk))
            )
            try:
                kc_response.raise_for_status()
            except HTTPError:
                return VALUE_TO_RETURN_ON_FAILURE
            try:
                form_data = kc_response.json()
            except ValueError:
                return VALUE_TO_RETURN_ON_FAILURE
            try:
                self._enter_data_link = form_data['enketo_url']
            except KeyError:
                return VALUE_TO_RETURN_ON_FAILURE
            self.save(update_fields=['_enter_data_link'])
        return self._enter_data_link

    def find_in_form_builder(self, attempt_create=True):
        ''' Look for a matching asset in KPI. If none is found and
        `attempt_create` is True, attempt to create the asset by opting the
        user into KPI. Returns the uid of the KPI asset if successful'''
        # Get the form's id string from KC
        kc_response = self._token_auth_request(
            'get',
            self._get_kc_endpoint_url('forms/{}?format=json'.format(
                self._kc_pk))
        )
        # FIXME: Match only 404 here once KC #227 is fixed:
        # https://github.com/kobotoolbox/kobocat/issues/227
        if kc_response.status_code in (404, 500):
            raise NotFoundInFormBuilder(
                'The corresponding KC form is missing; without it, no KPI '
                'asset can be located or created'
            )
        kc_form_data = kc_response.json()
        # Construct an identifier URL using the username and id string
        parsed_url = urlparse(self.url)
        identifier = u'{scheme}://{netloc}/{username}/forms/{id_string}'.format(
            scheme=parsed_url.scheme,
            netloc=parsed_url.netloc,
            username=self.user.username,
            id_string=kc_form_data['id_string']
        )
        # Search KPI for an asset whose deployment identifier matches our KC
        # project
        headers = {'Authorization': 'Token {}'.format(self.api_token)}
        kpi_search_url = '{}assets/?format=json&' \
            'q=deployment__identifier:"{}"'.format(
                settings.KPI_URL, identifier)
        response = requests.get(kpi_search_url, headers=headers)
        kpi_search_results = response.json()
        if kpi_search_results['count'] == 1:
            return kpi_search_results['results'][0]['uid']
        elif kpi_search_results['count'] > 1:
            raise Exception('Multiple KPI assets for a single KC project')
        elif kpi_search_results['count'] == 0 and attempt_create:
            # Opt the user into KPI, which syncs KC projects to KPI assets
            kpi_opt_in_url = '{}hub/switch_builder?beta=1&migrate=1'.format(
                settings.KPI_URL)
            response = requests.get(
                kpi_opt_in_url, headers=headers, allow_redirects=False)
            # Search again, but don't recurse
            return self.find_in_form_builder(attempt_create=False)
        raise NotFoundInFormBuilder('Failed to find matching KPI asset')
