from StringIO import StringIO
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from django.conf import settings
from urlparse import urlparse, urlunparse
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
    """ Retrieves data from KPI and processes it through a `Template` """
    user = models.ForeignKey(
        User, null=True, editable=False, related_name='renderings'
    )
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

    def _get_csv(self):
        if not self.api_token:
            raise Exception('Cannot download data without an API token')
        headers = {
            'Authorization': 'Token %s' % self.api_token
        }
        parsed_url = urlparse(self.url)

        if parsed_url.path.startswith(KC_PATH_HEAD):
            # Old project that was deployed to KoBoCAT
            response = requests.get(self.url, headers=headers)
            # For easier debugging
            response.raise_for_status()
            return self._csv_from_response(response)
        elif not parsed_url.path.startswith(KPI_PATH_HEAD):
            raise Exception('Cannot download data: invalid KoBo URL')

        # New project using KPI
        asset_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                '',  # remove the query parameters
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
        }
        # Request the export
        export_list_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                '/exports/',
                '',  # remove the params
                '',  # remove the query parameters
                '',  # remove the fragment
            )
        )
        response = requests.post(
            export_list_url, headers=headers, data=export_options
        )
        assert response.status_code == 201
        export_url = response.json()['url']
        export_result_url = None
        # Poll for export completion; rely on the server (e.g. gunicorn) to
        # kill us if this takes too long
        while True:
            time.sleep(2)
            response = requests.get(export_url, headers=headers)
            assert response.status_code == 200
            export_info = response.json()
            if export_info['status'] == 'complete':
                export_result_url = export_info['result']
                break
            elif export_info['status'] == 'error':
                raise Exception('Cannot download data: KPI export failed')
        # Get the exported CSV at last
        response = requests.get(export_result_url, headers=headers)
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
        # Raising an exception here doesn't help the user, but it at least
        # makes debugging easier
        response.raise_for_status()
        return self._csv_from_response(response)

    def _log_message(self, msg):
        full_msg = '<Rendering: %s> | %s' % (str(self), msg)
        logger.info(full_msg)

    @staticmethod
    def _write_variable_to_file(folder, name, value):
        filename = os.path.join(folder, name)
        with open(filename, 'w') as f:
            f.write(value)
        return filename

    def render(self, extension, request=None):
        self._log_message('render begin  ')
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
                self._log_message('download begin')
                self.download_data()
                self._log_message('download end  ')
                data_csv = os.path.join(folder, 'data.csv')
                if not self.data.endswith('\n'):
                    self.data += '\n'
                with open(data_csv, 'w') as f:
                    f.write(self.data.encode('utf-8'))

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
            with open(path) as f:
                result = f.read()

            self._log_message('render end    ')
            return result
        finally:
            shutil.rmtree(folder)

    def _get_kc_endpoint_url(self, endpoint):
        parsed_url = urlparse(self.url)
        assert parsed_url.path.startswith(KC_PATH_HEAD)
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
        assert parsed_url.path.startswith(KC_PATH_HEAD)
        return int(parsed_url.path.split('/')[-1])

    def _token_auth_request(self, method, url):
        """
        Make a request to KPI, using the associated user's token to
        authenticate
        """
        headers = {}
        if self.api_token:
            headers['Authorization'] = 'Token {}'.format(self.api_token)
        response = requests.request(method, url, headers=headers)
        return response

    def delete_from_kobo(self):
        """
        Delete the corresponding KPI asset and/or KC project, if it exists
        """
        parsed_url = urlparse(self.url)
        if parsed_url.path.startswith(KPI_PATH_HEAD):
            kpi_asset_url = self.url
        elif parsed_url.path.startswith(KC_PATH_HEAD):
            # Old project that was deployed to KoBoCAT, but may have been
            # synced to KPI at some point
            kpi_asset_url = self.find_kpi_asset_url_for_kc_project()
            if not kpi_asset_url:
                # This is a KC-only project
                kc_response = self._token_auth_request(
                    'delete',
                    # If you include a trailing slash after the pk, KC will
                    # reject the request with a 403. Isn't that fun?
                    self._get_kc_endpoint_url(
                        'forms/{}?format=json'.format(self._kc_pk)
                    ),
                )
                # Tolerating a 404 is the right thing to do if a user already
                # deleted the project from KC, but it runs the risk of masking
                # programming errors --jnm
                if kc_response.status_code not in (204, 404):
                    raise Exception(
                        'Unexpected status code {} returned by KC'.format(
                            kc_response.status_code
                        )
                    )
        else:
            raise Exception('Cannot delete: invalid KoBo URL')

        if kpi_asset_url:
            # Delete from KPI, which should clean up the KC project
            # automatically
            kpi_response = self._token_auth_request('delete', kpi_asset_url)
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
        VALUE_TO_RETURN_ON_FAILURE = u''
        if self._enter_data_link:
            return self._enter_data_link

        parsed_url = urlparse(self.url)
        if parsed_url.path.startswith(KC_PATH_HEAD):
            url = self._get_kc_endpoint_url(
                'forms/{}/enketo?format=json'.format(self._kc_pk)
            )
        elif parsed_url.path.startswith(KPI_PATH_HEAD):
            url = self.url
        else:
            return VALUE_TO_RETURN_ON_FAILURE

        response = self._token_auth_request(
            'get',
            url,
        )
        try:
            response.raise_for_status()
            form_data = response.json()
        except (HTTPError, ValueError):
            return VALUE_TO_RETURN_ON_FAILURE

        try:
            if parsed_url.path.startswith(KPI_PATH_HEAD):
                self._enter_data_link = form_data['deployment__links'][
                    'offline_url'
                ]
            else:
                self._enter_data_link = form_data['enketo_url']
        except KeyError:
            return VALUE_TO_RETURN_ON_FAILURE

        self.save(update_fields=['_enter_data_link'])
        return self._enter_data_link

    def find_kpi_asset_url_for_kc_project(self):
        """
        Assuming that `self` refers to a KC project, return the URL of its
        corresponding KPI asset if one exists; otherwise return `None`
        """
        # Get the form's id string from KC
        kc_response = self._token_auth_request(
            'get',
            self._get_kc_endpoint_url('forms/{}?format=json'.format(
                self._kc_pk))
        )
        if kc_response.status_code == 404:
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
        kpi_search_url = '{}api/v2/assets/?format=json&' \
            'q=deployment__identifier:"{}"'.format(
                settings.KPI_URL, identifier)
        response = requests.get(kpi_search_url, headers=headers)
        # Raising an exception here doesn't help the user, but it at least
        # makes debugging easier
        response.raise_for_status()
        kpi_search_results = response.json()
        if kpi_search_results['count'] == 1:
            return kpi_search_results['results'][0]['url']
        elif kpi_search_results['count'] > 1:
            raise Exception('Multiple KPI assets for a single KC project')
        else:
            return None
