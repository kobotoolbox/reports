from django.conf.urls import patterns, url, include
import views


urlpatterns = patterns(
    '',
    url(r'^$', views.demo, name='demo'),
    url(r'^me/$', views.current_user, name='current_user'),
    url(r'^reports/$', views.index, name='index'),
    url(r'^rendering/(?P<id>[^\.]+).(?P<extension>[^\.]+)$', views.rendering, name='rendering'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^templates/$', views.TemplateListCreate.as_view(), name='templates'),
    url(r'^templates/(?P<pk>[0-9]+)/$', views.TemplateRetrieveUpdateDestroy.as_view()),
    url(r'^renderings/$', views.RenderingListCreate.as_view(), name='renderings'),
    url(r'^renderings/(?P<pk>[0-9]+)/$', views.RenderingRetrieveUpdateDestroy.as_view()),
)
