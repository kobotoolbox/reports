from django.shortcuts import render
from django.http import HttpResponse
from models import Rendering


def index(request):
    renderings = Rendering.objects.all()
    extensions = ['html', 'pdf', 'docx']
    return render(request, 'index.html', dictionary=locals())


def rendering(request, id, extension):
    r = Rendering.objects.get(id=id)
    results = r.render()
    response = HttpResponse(results[extension])
    if extension != 'html':
        filename = '%(id)s.%(extension)s' % locals()
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
