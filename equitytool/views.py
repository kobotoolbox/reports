from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.urlresolvers import reverse
import requests
import os
import json
from bs4 import BeautifulSoup
# TODO: These objects should be made through API calls. Handling the
# authentication required to make those calls seems a little
# tricky. And it seems like unnecessary work at the moment.
from reporter.models import Template, Rendering
from django.utils.text import slugify
from xls2csv import xls2csv


@xframe_options_exempt
def index(request):
    extensions = ['html', 'pdf', 'docx']
    return render(request, 'equity.html', locals())


class ProjectForm(forms.Form):
    name = forms.CharField(label='Project name', max_length=1000)
    urban = forms.BooleanField(label='This is an urban-focused project', required=False)


@xframe_options_exempt
def create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data.copy()
            d['user'] = request.user
            Wrapper.create_project(**d)
            return HttpResponseRedirect(reverse('equity-tool'))
    else:
        form = ProjectForm()
    return render(request, 'create.html', {'form': form})


class Wrapper(object):

    KC_URL = 'https://kc.kobotoolbox.org'

    def __init__(self, user, name, urban):
        self.user = user
        self.name = name
        self.urban = urban
        self.set_api_token()

    def get_rmd(self):
        filename = 'wealth2.Rmd' if self.urban else 'wealth.Rmd'
        path = os.path.join('reporter', 'rmd_templates', filename)
        with open(path) as f:
            rmd = f.read()
        return rmd

    def set_template(self):
        slug = 'urban' if self.urban else 'national'
        template, created = Template.objects.get_or_create(user=self.user, slug=slug)
        template.rmd = self.get_rmd()
        template.save()
        self.template = template

    def set_api_token(self):
        path = '/%s/api-token' % self.user.username
        url = self.KC_URL + path
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        l = soup.find_all('input')
        assert len(l) == 1, 'Should have found exactly one input element.'
        self.api_token = l[0].attrs['value']

    def get_forms(self):
        path = '/api/v1/forms?owner=%s' % self.user.username
        url = self.KC_URL + path
        response = requests.get(url, headers=self._headers())
        l = json.loads(response.content)
        forms_by_id = dict([(d['id_string'], d) for d in l])
        return forms_by_id

    def _headers(self):
        return {'Authorization': 'Token %s' % self.api_token}

    # TODO: Does the form change based on urban-focus?
    def _create_form(self):
        url = self.KC_URL + '/api/v1/forms'
        path = os.path.join('equitytool', 'static', 'equity_tool.xls')
        csv = xls2csv(path, self.id_string)
        data = {'text_xls_form': csv}
        response = requests.post(url, data=data, headers=self._headers())
        assert response.status_code == 201, response.content

    def set_form(self):
        self.id_string = slugify(self.name)
        forms_by_id = self.get_forms()
        created = self.id_string not in forms_by_id
        if created:
            self._create_form()
            forms_by_id = self.get_forms()
        self.form = forms_by_id[self.id_string]

    def set_rendering(self):
        path = '/api/v1/data/%d?format=csv' % self.form['formid']
        url = self.KC_URL + path
        self.rendering, created = Rendering.objects.get_or_create(
            user=self.user,
            template=self.template,
            url=url,
            api_token=self.api_token,
            name=self.name
        )

    @classmethod
    def create_project(cls, **kwargs):
        w = cls(**kwargs)
        w.set_form()
        w.set_template()
        w.set_rendering()
