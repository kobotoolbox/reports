from django.http import HttpResponseRedirect
from django.urls import include, path
from . import views
import private_storage.urls


urlpatterns = [
    # Creates a new reporter.Rendering instance and a corresponding form on
    # KoBoToolbox
    path('create/', views.create, name='create-project'),
    # Retrieves data from KoBoToolbox
    path('sync/<int:pk>/', views.sync, name='sync'),
    # Stores administrator-uploaded XLSForms
    path('private-media/', include(private_storage.urls)),
    # Redirect from old endpoint to admin interface for convenience
    path(
        'superuser_stats/',
        lambda r: HttpResponseRedirect(
            '/admin/equitytool/adminstatsreporttask/add/'
        ),
    ),
]
