from django.urls import include, path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reporter.urls')),
    path('equitytool/', include('equitytool.urls')),
]
