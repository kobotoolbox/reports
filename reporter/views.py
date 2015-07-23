from django.shortcuts import render
from django.http import HttpResponse
from models import Rendering


def index(request):
    renderings = Rendering.objects.all()
    return render(request, 'index.html', dictionary=locals())


def rendering(request, id):
    r = Rendering.objects.get(id=id)
    # To start, every time a report is requested let's recompile it.
    r.render()
    return HttpResponse(r.html)
