from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import json
import tempfile
import subprocess
import os

with open('portal/reports.json') as f:
    REPORTS = json.load(f)

def index(request):
    '''
    Return a list of all the report templates.
    '''
    return render(request, 'index.html', dictionary={'reports': REPORTS})

class DynamicForm(forms.Form):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields')
        super(DynamicForm, self).__init__(*args, **kwargs)

        for k, v in fields.items():
            if type(v) == unicode:
                self.fields[k] = forms.CharField(
                    label=k,
                    initial=v
                )
                self.fields[k].widget = forms.HiddenInput()
            if type(v) == list:
                self.fields[k] = forms.ChoiceField(
                    label=k,
                    choices=[(c, c) for c in v],
                    required=False
                )

    def clean(self):
        sep = '/'
        cleaned_data = super(DynamicForm, self).clean()
        grouped = {}
        for k, v in cleaned_data.items():
            if sep in k:
                l = k.split(sep)
                assert len(l) == 2
                if l[0] in grouped:
                    grouped[l[0]][l[1]] = v
                else:
                    grouped[l[0]] = {l[1]: v}
            else:
                grouped[k] = v
        self.cleaned_data = grouped
        return grouped

def report(request, slug):
    '''
    Present the user with a form to fill in the parameters for the
    report.
    '''
    fields = REPORTS[slug]

    if request.method == 'POST':
        form = DynamicForm(request.POST, fields=fields)
        if form.is_valid():
            config = form.cleaned_data
            config['template'] = slug
            return _compile(config)
    else:
        form = DynamicForm(fields=fields)
    return render(request, 'form.html', {'form': form})

def _compile(config):
    ## Save config to temporary json file.
    config_json = tempfile.NamedTemporaryFile(delete=False)
    json.dump(config, config_json)
    config_json.close()

    ## Create temporary file for saving compiled report.
    report_html = tempfile.NamedTemporaryFile(delete=False)

    ## Call the compiler.
    cmd = ' '.join(['Rscript ../compiler/compiler.R', config_json.name, report_html.name])
    subprocess.call(cmd, shell=True, cwd='../compiler/')
    
    ## Pull the text out of the compiled report.
    with open(report_html.name) as f:
        text = f.read()

    ## Clean up temporary files.
    os.remove(config_json.name)
    os.remove(report_html.name)

    return HttpResponse(text)
