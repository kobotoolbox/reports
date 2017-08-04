import datetime
import requests
import logging
from urlparse import urlparse
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import authenticate
from models import Template, Rendering
from rest_framework import serializers, permissions, viewsets, status
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from equitytool.models import Form


def index(request):
    if request.user.is_authenticated():
        renderings = Rendering.objects.filter(user=request.user)
    extensions = ['html', 'pdf', 'docx']
    return render(request, 'index.html', dictionary=locals())

@api_view(['GET'])
def current_user(request):
    user = request.user
    countries = Form.objects.all().values('id', 'name').order_by('name')
    if user.is_anonymous():
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

def demo(request):
    context = RequestContext(request)
    return render(request, 'demo.html', context_instance=context)

def rendering(request, id, extension):
    r = Rendering.objects.get(id=id)
    if request.user != r.user:
        return render(request, 'not_owner.html')
    result = r.render(extension)
    response = HttpResponse(result)
    if extension != 'html':
        filename = '%(id)s.%(extension)s' % locals()
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
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
        if user.is_anonymous():
            return Rendering.objects.none()
        return Rendering.objects.filter(user=user).order_by('-pk')

    def perform_destroy(self, instance):
        instance.delete_from_kc_and_kpi()
        return super(RenderingViewSet, self).perform_destroy(instance)

    @detail_route(methods=['get'])
    def one_time_form_builder_access(self, request, pk=None):
        rendering = self.get_object()
        # The client will have to POST a one-time key to this URL in order to
        # authenticate the user to KPI and load the form builder for this
        # rendering
        form_builder_access = {
            'url': u'{kpi_url}{auth_shim}#/forms/{uid}/edit'.format(
                kpi_url=settings.KPI_URL,
                auth_shim='authorized_application/one_time_login/',
                uid=rendering.find_in_form_builder()
            )
        }
        # Using our trusted application status, command KPI to create a
        # one-time key for the currently logged in user
        url = '{}authorized_application/one_time_authentication_keys/'.format(
            settings.KPI_URL)
        headers = {'Authorization': 'Token {}'.format(settings.KPI_API_KEY)}
        data = {'username': request.user.username}
        response = requests.post(url, headers=headers, data=data)
        form_builder_access['one_time_key'] = response.json()['key']
        return Response(form_builder_access)


def proxy_create_user(request):
    url = '{}authorized_application/users/'.format(
        settings.KPI_URL)
    headers = {'Authorization': 'Token {}'.format(settings.KPI_API_KEY)}
    response = requests.post(url, data=request.POST, headers=headers)
    content_type = response.headers.get('content-type')
    # Store the user's organization in KC if the creation was successful
    organization = request.POST.get('organization', False)
    if organization and response.status_code == status.HTTP_201_CREATED:
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        # Could maybe call login() after authenticate() to automatically login
        # new users upon registration; see
        # https://docs.djangoproject.com/en/1.9/topics/auth/default/#how-to-log-a-user-in
        user = authenticate(username=username, password=password)
        # Should now have user.external_api_token from KoboApiAuthBackend
        profile_url = '{}/api/v1/profiles/{}'.format(settings.KC_URL, username)
        profile_headers = {
            'Authorization': 'Token {}'.format(user.external_api_token.key)
        }
        # Patch the user's KC profile to set the organization
        profile_response = requests.patch(
            profile_url,
            data={'organization': organization},
            headers=profile_headers
        )
        if profile_response.status_code != status.HTTP_200_OK:
            # The user has already been created, so it doesn't make sense to
            # fail completely at this point. We should log the error, though
            logging.error((
                'Unable to set organization to "{}" for user "{}". KC '
                'returned HTTP {}.'
            ).format(organization, username, profile_response.status_code))

    return HttpResponse(
        response.content,
        content_type=content_type,
        status=response.status_code
    )
