from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
import views

router = DefaultRouter()
router.register(r'templates', views.TemplateView)

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^rendering/(?P<id>[^\.]+).(?P<extension>[^\.]+)$', views.rendering, name='rendering'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^renderings/$', views.RenderingListCreate.as_view(), name='renderings'),
    url(r'^renderings/(?P<pk>[0-9]+)/$', views.RenderingRetrieveUpdateDestroy.as_view()),
    url(r'^', include(router.urls)),
)
