import base64
import datetime
import json
import os
import re
import requests
import time
import unicodecsv
import xlwt
import zipfile
from io import BytesIO

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core import management
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import Template as DjangoTemplate, Context
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import exceptions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# TODO: These objects should be made through API calls. Handling the
# authentication required to make those calls seems a little
# tricky. And it seems like unnecessary work at the moment.
from reporter.models import Template, Rendering, UserExternalApiToken
from .models import Form


@xframe_options_exempt
def index(request):
    extensions = ['html', 'pdf', 'docx']
    if request.user.is_authenticated:
        projects = request.user.renderings.order_by('name')
    return render(request, 'equity.html', locals())


@xframe_options_exempt
def sync(request, pk):
    r = Rendering.objects.get(pk=pk)
    r.download_data()
    return HttpResponseRedirect(reverse('equity-tool'))


class ProjectForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Form.objects.all())
    name = forms.CharField(label='Project name', max_length=1000)
    regional = forms.BooleanField(
        label='This is an region-focused project', required=False)


def _create_project(posted_data, user):
    form = ProjectForm(posted_data, user)
    if form.is_valid():
        d = form.cleaned_data.copy()
        d['user'] = user
        with transaction.atomic():
            if Rendering.objects.filter(
                    user=user, name__iexact=d['name']).exists():
                raise exceptions.ValidationError(detail={'name': _(
                    'You already have a project with this name')})
            return Wrapper.create_project(**d)

@xframe_options_exempt
def create(request):
    if request.method == 'POST':
        proj = _create_project(request.POST, request.user)
        if proj:
            return HttpResponseRedirect(reverse('equity-tool'))
    else:
        form = ProjectForm()
    return render(request, 'create.html', {'form': form})


@api_view(['POST'])
def create_friendly(request):
    '''
    A version of the 'create' method that returns a 201 "CREATED" code
    on successful creation
    '''
    if not request.user.is_authenticated:
        raise exceptions.NotAuthenticated()
    proj = _create_project(request.POST, request.user)
    if proj:
        return Response({}, status=status.HTTP_201_CREATED)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

class Wrapper(object):
    ''' Allows the user to create useful "projects" by tying together
    `equitytool.Form`, `reporter.Template`, and `reporter.Rendering` '''

    KPI_URL = settings.KPI_URL

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def api_token(self):
        try:
            return self.user.external_api_token.key
        except UserExternalApiToken.DoesNotExist:
            return None

    def get_rmd(self):
        # FIXME: M4M to supply new Rmd for regional projects
        filename = 'wealth.Rmd' if self.regional else 'wealth.Rmd'
        path = os.path.join('reporter', 'rmd_templates', filename)
        with open(path) as f:
            rmd = f.read()
        return rmd

    def set_template(self):
        slug = 'regional' if self.regional else 'urban'
        template, created = Template.objects.get_or_create(slug=slug)
        if created:
            template.rmd = self.get_rmd()
            template.save()
        self.template = template

    def _headers(self):
        return {'Authorization': 'Token %s' % self.api_token}

    @staticmethod
    def _csv_to_xlsform_io(csv_str):
        """
        It'd be better to skip the entire templating process now that we're
        creating forms via KPI, since `id_string` cannot be set manually and
        there's a better way to set the title (`asset.name`). However, while we
        already have CSV strings in the database and possibly do not have their
        original XLSForm sources, let's endure the grossness and convert CSV
        back to XLS
        """
        for line in csv_str.split('\n'):
            csv_io = BytesIO(csv_str.encode('utf-8'))
            xls_io = BytesIO()
            xl_wb = xlwt.Workbook()
            xl_sheet = None
            xl_row_index = 0
            for row in unicodecsv.reader(csv_io):
                if row[0]:
                    # A new sheet in our weird "sheeted" CSV format
                    xl_sheet = xl_wb.add_sheet(row[0])
                    xl_row_index = 0
                else:
                    # A row within a sheet
                    for xl_col_index, xl_value in enumerate(row[1:]):
                        xl_sheet.write(xl_row_index, xl_col_index, xl_value)
                    xl_row_index += 1
            xl_wb.save(xls_io)
            xls_io.seek(0)
            return xls_io

    def _create_kpi_asset(self):
        form = self.country
        template = DjangoTemplate(form.csv_form)
        context = Context({
            'form_title': self.name,
            'form_id': '',  # not applicable to KPI deployments, but still
                            # referenced by templates
        })
        csv = template.render(context)
        # KPI doesn't support CSV imports; convert CSV to XLS
        base64_xlsform = base64.b64encode(self._csv_to_xlsform_io(csv).read())
        url = self.KPI_URL + 'imports/'
        data = {
            'name': self.name,
            'base64Encoded': b'base64:' + base64_xlsform,
            'library': 'false',
        }
        # Start the asynchronous import
        response = requests.post(url, data=data, headers=self._headers())
        assert response.status_code == 201
        import_url = response.json()['url']
        # Poll for import completion; rely on the server (e.g. gunicorn) to
        # kill us if this takes too long
        import_info = None
        while True:
            response = requests.get(import_url, headers=self._headers())
            assert response.status_code == 200
            import_info = response.json()
            if import_info['status'] == 'complete':
                break
            else:
                time.sleep(2)
        # Yikes
        asset_uid = import_info['messages']['created'][0]['uid']
        # Deploy the new KPI asset
        deploy_url = '{}api/v2/assets/{}/deployment/?format=json'.format(
            self.KPI_URL, asset_uid
        )
        data = {'active': True}
        response = requests.post(deploy_url, data=data, headers=self._headers())
        assert response.status_code == 200
        return response.json()['asset']

    def set_form(self):
        self.form = self._create_kpi_asset()

    def set_rendering(self):
        self.rendering, created = Rendering.objects.get_or_create(
            user=self.user,
            template=self.template,
            url=self.form['url'],
            name=self.name,
            form_name=self.country.name,
            form_pk=self.country.pk
        )

        # We don't have to worry about fetching Enketo links from KC because
        # this method only gets called when creating *new* projects, which use
        # KPI
        try:
            self.rendering._enter_data_link = self.form['deployment__links'][
                'offline_url'
            ]
        except KeyError:
            # If Enketo is down, we'll have another opportunity to try again
            pass
        else:
            self.rendering.save(update_fields=['_enter_data_link'])

        self.rendering.download_data()

    @classmethod
    def create_project(cls, **kwargs):
        w = cls(**kwargs)
        w.set_form()
        w.set_template()
        w.set_rendering()
        return w


@user_passes_test(lambda u: u.is_superuser)
def superuser_stats(request):
    REPORTS = {
        'users.csv': {
            'args': {'user_report': True}
        },
        'projects.csv': {
            'args': {'project_report': True}
        }
    }

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment;filename="{}_{}.zip"'.format(
        re.sub('[^a-zA-Z0-9]', '-', request.META['HTTP_HOST']),
        datetime.date.today()
    )
    with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, report_settings in REPORTS.items():
            with BytesIO() as csv_io:
                management.call_command(
                    'print_stats', stdout=csv_io, **report_settings['args'])
                zip_file.writestr(filename, csv_io.getvalue())
    return response
