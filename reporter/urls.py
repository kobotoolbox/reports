from django.urls import include, path
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('templates', views.TemplateView)
router.register('renderings', views.RenderingViewSet)

urlpatterns = [
    path('', views.demo, name='demo'),
    path('me/', views.current_user, name='current_user'),
    path('reports/', views.index, name='index'),
    path('rendering/<int:id>.<slug:extension>', views.rendering, name='rendering'),
    path('api-auth/logout/', LogoutView.as_view(), {
        'next_page': 'https://www.equitytool.org/'
    }),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.proxy_create_user),
    path('', include(router.urls)),
]
