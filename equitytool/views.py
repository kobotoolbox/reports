from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.urlresolvers import reverse
import requests
import os
from bs4 import BeautifulSoup
# TODO: These objects should be made through API calls. Handling the
# authentication required to make those calls seems a little
# tricky. And it seems like unnecessary work at the moment.
from reporter.models import Template, Rendering


@xframe_options_exempt
def index(request):
    return render(request, 'equity.html')


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

    def create_template(self):
        slug = 'urban' if self.urban else 'national'
        template, created = Template.objects.get_or_create(user=self.user, slug=slug)
        template.rmd = self.get_rmd()
        template.save()
        return template

    def set_api_token(self):
        path = '/%s/api-token' % self.user.username
        url = self.KC_URL + path
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        l = soup.find_all('input')
        assert len(l) == 1, 'Should have found exactly one input element.'
        self.api_token = l[0].attrs['value']

    def create_form(self):
        # TODO: Does the form change based on urban-focus?
        path = os.path.join('equitytool', 'static', 'equity_tool.xls')
        url = self.KC_URL + '/api/v1/forms'
        headers = {'Authorization': 'Token %s' % self.api_token}
        with open(path, 'rb') as f:
            data = {'xls_file': 'equity_tool.xls'}
            files = {'equity_tool.xls': f.read()}
            response = requests.post(url, data=data, files=files, headers=headers)
        print url
        assert response.status_code == 200, response.content

    def create_rendering(self, template):
        rendering, created = Rendering.objects.get_or_create(
            user=self.user,
            template=template,
            name=self.name,
            url='fake'
        )
        return rendering

    @classmethod
    def create_project(cls, **kwargs):
        w = cls(**kwargs)
        # w.create_form()
        template = w.create_template()
        rendering = w.create_rendering(template)
