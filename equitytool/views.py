from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.urlresolvers import reverse
import requests
import os
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

    KC_URL = 'kc.kobotoolbox.org'
    # KR_URL = 'http://localhost:8000'

    def __init__(self, user, name, urban):
        self.user = user
        self.name = name
        self.urban = urban

    def get_rmd(self):
        filename = 'wealth2.Rmd' if self.urban else 'wealth.Rmd'
        path = os.path.join('reporter', 'rmd_templates', filename)
        with open(path) as f:
            rmd = f.read()
        return rmd

    def create_template(self):
        data = {'user': self.user, 'slug': self.name, 'rmd': self.get_rmd()}
        template, created = Template.objects.get_or_create(**data)
        return template

    def create_rendering(self, template):
        rendering, created = Rendering.objects.get_or_create(
            user=self.user,
            template=template,
            url='fake'
        )
        return rendering

    @classmethod
    def create_project(cls, **kwargs):
        w = cls(**kwargs)
        template = w.create_template()
        rendering = w.create_rendering(template)
