from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('templates', views.TemplateView)
router.register('renderings', views.RenderingViewSet)

urlpatterns = [
    path('', views.root, name='root'),
    # Confirms authentication
    path('me/', views.current_user, name='current_user'),
    # Serves the results in HTML, PDF, or DOCX format
    path('rendering/<int:id>.<slug:extension>', views.rendering, name='rendering'),
    # Exposes the DRF login page with a custom template; not part of the SPA
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Creates a new KoBoToolbox user via a privileged endpoint there
    # See https://github.com/kobotoolbox/kpi/pull/368
    path('register/', views.proxy_create_user),
    path('', include(router.urls)),
]
