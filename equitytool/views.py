from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def index(request):
    return render(request, 'equity.html')


class ProjectForm(forms.Form):
    name = forms.CharField(label='Project name', max_length=1000)
    urban = forms.BooleanField(label='This is an urban-focused project')


@xframe_options_exempt
def create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        form = ProjectForm()

    return render(request, 'create.html', {'form': form})
