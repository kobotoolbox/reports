from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url('^admin/', include(admin.site.urls)),
    url('', include('reporter.urls')),
    url('^equitytool/', include('equitytool.urls')),
)
