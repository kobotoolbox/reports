from django.urls import include, path
from . import views
import private_storage.urls


urlpatterns = [
    # Creates a new reporter.Rendering instance and a corresponding form on
    # KoBoToolbox
    path('create/', views.create, name='create-project'),
    # Retrieves data from KoBoToolbox
    path('sync/<int:pk>/', views.sync, name='sync'),
    # Generates zipped CSV about user activity for administrators
    path('superuser_stats/', views.superuser_stats),
    # Stores administrator-uploaded XLSForms
    path('private-media/', include(private_storage.urls)),
]
