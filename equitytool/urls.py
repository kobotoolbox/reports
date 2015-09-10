from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='equity-tool'),
    url(r'^create$', views.create, name='create-project'),
)
