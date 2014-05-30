from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'portal.views.index', name='index'),
    url(r'(?P<slug>[^/]+)/$', 'portal.views.report', name='report'),
    # url(r'^blog/', include('blog.urls')),
)
