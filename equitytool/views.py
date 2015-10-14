from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.urlresolvers import reverse
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework.decorators import api_view
import requests
import os
import json
from bs4 import BeautifulSoup
# TODO: These objects should be made through API calls. Handling the
# authentication required to make those calls seems a little
# tricky. And it seems like unnecessary work at the moment.
from reporter.models import Template, Rendering
from django.utils.text import slugify
from models import Form
from django.template import Template as DjangoTemplate, Context


@xframe_options_exempt
def index(request):
    extensions = ['html', 'pdf', 'docx']
    if request.user.is_authenticated():
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
    urban = forms.BooleanField(label='This is an urban-focused project', required=False)

def _create_project(posted_data, user):
    form = ProjectForm(posted_data, user)
    if form.is_valid():
        d = form.cleaned_data.copy()
        d['user'] = user
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
    proj = _create_project(request.POST, request.user)
    if proj:
        return Response({}, status=status.HTTP_201_CREATED)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

class Wrapper(object):

    KC_URL = 'https://kc.kobotoolbox.org'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
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

    def _create_form(self):
        form = Form.objects.get(name=self.country)
        template = DjangoTemplate(form.csv_form)
        context = Context({
            'form_title': self.name,
            'form_id': self.id_string,
        })
        csv = template.render(context)
        url = self.KC_URL + '/api/v1/forms'
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
        self.rendering.download_data()

    @classmethod
    def create_project(cls, **kwargs):
        w = cls(**kwargs)
        w.set_form()
        w.set_template()
        w.set_rendering()
        return w
