from django.http import HttpResponse
from django.shortcuts import render
from models import Template, Rendering
from rest_framework import generics, serializers, permissions


def index(request):
    if request.user.is_authenticated():
        renderings = Rendering.objects.filter(user=request.user)
    extensions = ['html', 'pdf', 'docx']
    return render(request, 'index.html', dictionary=locals())


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
