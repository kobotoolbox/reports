import datetime
import json
import requests
import logging
from urllib.parse import urlparse
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import authenticate
from .models import Template, Rendering
from rest_framework import serializers, permissions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from equitytool.models import Form


@api_view(['GET'])
def current_user(request):
    user = request.user
    countries = Form.objects.all().values(
        'id', 'name', 'parent'
    ).order_by('name')
    if user.is_anonymous:
        return Response({'message': 'user is not logged in'})
    else:
        return Response({'username': user.username,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'email': user.email,
                         'countries': countries,
                         'server_time': str(datetime.datetime.utcnow()),
                         'is_superuser': user.is_superuser,
                         'is_staff': user.is_staff,
                         'last_login': user.last_login,
                         })

def root(request):
    return render(request, 'root.html')

def rendering(request, id, extension):
    r = Rendering.objects.get(id=id)
    if request.user != r.user:
        return render(request, 'not_owner.html')
    result = r.render(extension, request)
    response = HttpResponse(result)
    if extension != 'html':
        EXTENSIONS_TO_MIME_TYPES = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        }
        filename = '%(id)s.%(extension)s' % locals()
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        try:
            response['Content-Type'] = EXTENSIONS_TO_MIME_TYPES[extension]
        except IndexError:
            pass
    return response


class IsOwner(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'slug', 'rmd')


class RenderingSerializer(serializers.ModelSerializer):
    template__name = serializers.ReadOnlyField(source='template.name')
    form = serializers.ReadOnlyField(source='form_pk')
    form__name = serializers.ReadOnlyField(source='form_name')
    class Meta:
        model = Rendering
        fields = (
            'id',
            'template',
            'template__name',
            'form',
            'form__name',
            'url',
            'name',
            'created',
            'modified',
            'submission_count',
            'enter_data_link',
            'edit_link',
        )


# API endpoints for templates
class TemplateView(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (permissions.DjangoModelPermissions, )


# API endpoints for renderings
class RenderingViewSet(viewsets.ModelViewSet):
    queryset = Rendering.objects.none()
    serializer_class = RenderingSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Rendering.objects.none()
        return Rendering.objects.filter(user=user).order_by('-pk')

    def perform_destroy(self, instance):
        instance.delete_from_kobo()
        return super(RenderingViewSet, self).perform_destroy(instance)


def proxy_create_user(request):
    url = '{}authorized_application/users/'.format(
        settings.KPI_URL)
    headers = {'Authorization': 'Token {}'.format(settings.KPI_API_KEY)}
    response = requests.post(url, data=request.POST, headers=headers)
    content_type = response.headers.get('content-type')
    return HttpResponse(
        response.content,
        content_type=content_type,
        status=response.status_code
    )
