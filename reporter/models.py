from io import StringIO
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from django.conf import settings
from urllib.parse import urlparse, urlunparse
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
import shutil
import time


# Used to detect whether an EquityTool survey was deployed to
# KC (old) or KPI (new)
KPI_PATH_HEAD = '/api/v2/'
KC_PATH_HEAD = '/api/v1/data/'


class UserExternalApiToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='external_api_token',
        on_delete=models.CASCADE,
    )
    key = models.CharField(max_length=120)


class Template(models.Model):
    """
    Global R Markdown templates. These transform collected data from its raw
    state into formatted reports (narrative, tables, charts). Available
    read-only to all users, but require model-level permissions or superuser
    access to modify
    """
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

    def __str__(self):
        return self.slug


class Rendering(models.Model):
    """ Retrieves data from KPI and processes it through a `Template` """
    user = models.ForeignKey(
        User,
        null=True,
        editable=False,
        related_name='renderings',
        on_delete=models.CASCADE,
    )
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
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

    def __str__(self):
        return str(self.id)

    @staticmethod
    def _csv_from_response(response):
        # Raise exception if status code does not indicate success
        response.raise_for_status()
        stripped_content = response.text.strip()
        # An empty response is expected when there's no data, but Pandas won't
        # tolerate it
        if len(stripped_content):
            # Quasi-validate the CSV by trying to parse it with Pandas
            df = pd.read_csv(StringIO(response.text), index_col=None)
            if df.size < 2 or len(df.columns) < 2:
                # No real data here; retry using semicolon as the separator
                df = pd.read_csv(StringIO(response.text), index_col=None, sep=';')
                if df.size >= 2 and len(df.columns) >= 2:
                    # Convert to standard comma-separated
                    stripped_content = df.to_csv().strip()

        return stripped_content

    def _get_csv(self):
        if getattr(
            # Hack for unit tests that use non-KoBo CSV
            self, '_test_non_kobo_csv', False
        ):
            response = self._token_auth_request('get', self.url)
            response.raise_for_status()
            return self._csv_from_response(response)

        self._migrate_kc_url_to_kpi()
        parsed_url = urlparse(self.url)
        if not parsed_url.path.startswith(KPI_PATH_HEAD):
            raise Exception('Cannot download data: invalid KoBo URL')

        # New project using KPI
        asset_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                '',  # remove the query string
                '',  # remove the fragment
            )
        )
        # This tool was built to use KoBoCAT CSV exports, so mirror them as
        # closely as possible
        export_options = {
            'source': asset_url,
            'type': 'csv',
            'fields_from_all_versions': 'false',
            'lang': '_xml',
            'hierarchy_in_labels': 'false',
            'group_sep': '/',
            'multiple_select': 'both',
        }
        # Request the export
        export_list_url = '{}exports/'.format(asset_url)
        response = self._token_auth_request(
            'post', export_list_url, data=export_options
        )
        # 201 is expected, unless an identical export is active, in which case
        # a 200 should be returned
        assert response.status_code in (200, 201)
        export_url = response.json()['url']
        export_result_url = None
        # Poll for export completion; rely on the server (e.g. gunicorn) to
        # kill us if this takes too long
        while True:
            time.sleep(2)
            response = self._token_auth_request('get', export_url)
            assert response.status_code == 200
            export_info = response.json()
            if export_info['status'] == 'complete':
                export_result_url = export_info['result']
                break
            elif export_info['status'] == 'error':
                raise Exception('Cannot download data: KPI export failed')
        # Get the exported CSV at last
        response = self._token_auth_request('get', export_result_url)
        return self._csv_from_response(response)

    @property
    def api_token(self):
        if self.user is None:
            return None
        try:
            return self.user.external_api_token.key
        except UserExternalApiToken.DoesNotExist:
            return None

    def download_data(self):
        self.data = self._get_csv()
        self.save()
        '''
        # TODO: use this again once KPI supports filtered exports
        elif self.data:
            try:
                self._download_new_data()
            except pd.parser.CParserError:
                # If the existing data has different (typically fewer) columns
                # than the new data, pandas will raise something like:
                #   Error tokenizing data. C error: Expected 44 fields in line
                #   3, saw 46
                # Work around that by re-fetching the entire data set
                self.data = ''
                self.download_data()
        '''

    def _download_new_data(self):
        # TODO: use this again once KPI supports filtered exports
        raise NotImplementedError(
            'KPI does not yet support exports with queries'
        )
        old_lines = self.data.split('\n')
        new_data = self._get_new_data()
        if new_data:
            new_lines = new_data.split('\n')
            combined_lines = new_lines + old_lines[1:len(old_lines)]
            self.data = '\n'.join(combined_lines)

    def _get_new_data(self):
        # TODO: use this again once KPI supports filtered exports
        raise NotImplementedError(
            'KPI does not yet support exports with queries'
        )
        f = StringIO(self.data)
        df = pd.read_csv(f, index_col=None)
        last_submission = df['_submission_time'].max()
        url = self.url
        query = {"_submission_time": {"$gt": str(last_submission)}}
        params = {
            'format': 'csv',
            'query': json.dumps(query)
        }
        response = self._token_auth_request('get', url, params=params)
        # Raising an exception here doesn't help the user, but it at least
        # makes debugging easier
        response.raise_for_status()
        return self._csv_from_response(response)

    @staticmethod
    def _write_variable_to_file(folder, name, value):
        filename = os.path.join(folder, name)
        with open(filename, 'w') as f:
            f.write(value)
        return filename

    def render(self, extension, request=None):
        folder = tempfile.mkdtemp()
        try:
            filename = '%s.Rmd' % self.template.slug
            path = os.path.join(folder, filename)

            # This relies on the Django template engine, which really has no
            # idea how to escape a string for R. Work around this by writing
            # the unsafe string to a temporary file, which is then read into a
            # variable by the `compile.R` script
            rendering__name_filename = self._write_variable_to_file(
                folder=folder,
                name='rendering__name',
                value=self.name
            )
            form__name_filename = self._write_variable_to_file(
                folder=folder,
                name='form__name',
                value=self.form_name
            )
            request__show_urban_filename = self._write_variable_to_file(
                folder=folder,
                name='request__show_urban',
                value=(
                    request.GET.get('show_urban', 'true') if request
                        else 'true'
                )
            )

            with open(path, 'w') as f:
                f.write(self.template.rmd)

            if self.url:
                self.download_data()
                data_csv = os.path.join(folder, 'data.csv')
                if not self.data.endswith('\n'):
                    self.data += '\n'
                with open(data_csv, 'w') as f:
                    f.write(self.data)

            context = {
                'filename': filename,
                'url': self.url,
                'extension': extension,
                'rendering__name_filename': rendering__name_filename,
                'form__name_filename': form__name_filename,
                'request__show_urban_filename': request__show_urban_filename,
            }
            script = render_to_string('compile.R', context)
            path = os.path.join(folder, 'temp.R')
            with open(path, 'w') as f:
                f.write(script)

            r_interpreter = subprocess.Popen(
                ('Rscript', 'temp.R'),
                cwd=folder,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            r_out, r_err = r_interpreter.communicate()
            if r_interpreter.returncode != 0:
                raise Exception('R failed to render {}: {}'.format(
                    self.pk, r_err))

            path = os.path.join(folder, self.template.slug + '.' + extension)
            with open(path, 'rb') as f:
                result = f.read()

            return result
        finally:
            shutil.rmtree(folder)

    def _migrate_kc_url_to_kpi(self):
        """
        If `self.url` is a defunct V1 API URL from `kobo.apps.openrosa`
        (formerly KoboCAT), attempt to extract `XForm.pk` from it and find the
        matching Asset by querying
        `_deployment_data__backend_response__formid`. If a match is found,
        update `self.url` to the corresponding V2 API URL and save to the
        database.

        Returns `True` if `self.url` already was or has just been updated to a
        KPI V2 API URL, otherwise `False`.
        """
        parsed_url = urlparse(self.url)
        if parsed_url.path.startswith(KPI_PATH_HEAD):
            return True
        if not parsed_url.path.startswith(KC_PATH_HEAD):
            return False

        kpi_search_url = (
            '{}api/v2/assets/?format=json&'
            'q=_deployment_data__backend_response__formid:{}'
        ).format(settings.KPI_URL, self._kc_pk)
        response = self._token_auth_request('get', kpi_search_url)
        # Raising an exception here doesn't help the user, but it at least
        # makes debugging easier
        response.raise_for_status()
        kpi_search_results = response.json()
        if kpi_search_results['count'] == 1:
            self.url = kpi_search_results['results'][0]['url']
            self.save(update_fields=['url'])
            return True
        elif kpi_search_results['count'] > 1:
            raise Exception('Multiple KPI assets for a single KC project')
        else:
            return False

    @property
    def _kc_pk(self):
        # Assume the numeric ID is the last component of the URL path before
        # the query string
        parsed_url = urlparse(self.url)
        assert parsed_url.path.startswith(KC_PATH_HEAD)
        return int(parsed_url.path.split('/')[-1])

    def _token_auth_request(self, method, url, *args, **kwargs):
        """
        Make a request to KPI, using the associated user's token to
        authenticate
        """
        headers = {}
        if self.api_token:
            headers['Authorization'] = 'Token {}'.format(self.api_token)
        response = requests.request(
            method, url, *args, headers=headers, **kwargs
        )
        return response

    def delete_from_kobo(self):
        """
        Delete the corresponding KPI asset, if it exists
        """
        if not self._migrate_kc_url_to_kpi():
            # Nothing to be done; old KoboCAT projects with no matching KPI
            # asset are completely inaccessible
            return

        kpi_response = self._token_auth_request('delete', self.url)

        # Tolerating a 404 is the right thing to do if a user already
        # deleted the project from Kobo, but it runs the risk of masking
        # programming errors
        if kpi_response.status_code not in (204, 404):
            raise Exception(
                'Unexpected status code {} returned by KPI'.format(
                    kpi_response.status_code
                )
            )

    @property
    def enter_data_link(self):
        """
        Return the Enketo data-entry link, retrieving it from KPI if
        necessary
        """
        VALUE_TO_RETURN_ON_FAILURE = ''
        if self._enter_data_link:
            return self._enter_data_link

        if not self._migrate_kc_url_to_kpi():
            # Defunct project that was never migrated to a KPI asset
            return VALUE_TO_RETURN_ON_FAILURE

        response = self._token_auth_request('get', self.url)
        try:
            response.raise_for_status()
            form_data = response.json()
        except (HTTPError, ValueError):
            return VALUE_TO_RETURN_ON_FAILURE

        try:
            self._enter_data_link = form_data['deployment__links'][
                'offline_url'
            ]
        except KeyError:
            return VALUE_TO_RETURN_ON_FAILURE

        self.save(update_fields=['_enter_data_link'])
        return self._enter_data_link

    @property
    def edit_link(self):
        """
        Get from `self.url`, which is something like
            https://kf.kobotoolbox.org/api/v2/assets/aLGo7b3sjQ5iikqY7xhzZ6/?format=json
        ...to a KPI URL that will prompt to login and redirect to the form
        builder, e.g.:
            https://kf.kobotoolbox.org/accounts/login/?next=/%23/forms/aLGo7b3sjQ5iikqY7xhzZ6/edit
        """
        if not self._migrate_kc_url_to_kpi():
            return None
        parsed_url = urlparse(self.url)
        asset_path = parsed_url.path
        asset_uid = asset_path.split('/')[-2]
        # Make sure to use `%23` instead of `#`, otherwise the redirection will
        # fail
        kpi_edit_url = (
            '{scheme}://{netloc}/accounts/login/?next=/%23/forms/{uid}/edit'
        ).format(
            scheme=parsed_url.scheme,
            netloc=parsed_url.netloc,
            uid=asset_uid,
        )
        return kpi_edit_url

