import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from models import Template, Rendering
from rest_framework import generics, serializers, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    if request.user.is_authenticated():
        renderings = Rendering.objects.filter(user=request.user)
    extensions = ['html', 'pdf', 'docx']
    return render(request, 'index.html', dictionary=locals())

@api_view(['GET'])
def current_user(request):
    user = request.user
    if user.is_anonymous():
        return Response({'message': 'user is not logged in'})
    else:
        return Response({'username': user.username,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'email': user.email,
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


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'slug', 'rmd')


class RenderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rendering
        fields = ('id', 'template', 'url', 'api_token')


# API endpoints for templates
class TemplateListCreate(generics.ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Template.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TemplateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (IsOwner, )


# API endpoints for renderings
class RenderingListCreate(generics.ListCreateAPIView):
    queryset = Rendering.objects.all()
    serializer_class = RenderingSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Rendering.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RenderingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rendering.objects.all()
    serializer_class = RenderingSerializer
    permission_classes = (IsOwner, )
