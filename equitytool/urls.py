from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='equity-tool'),
    url(r'^create$', views.create, name='create-project'),
    url(r'^sync/(?P<pk>[0-9]+)/$', views.sync, name='sync'),
)
