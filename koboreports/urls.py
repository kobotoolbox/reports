from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url('^admin/', include(admin.site.urls)),
    url('', include('reporter.urls')),
    url('^equitytool/', include('equitytool.urls')),
]
