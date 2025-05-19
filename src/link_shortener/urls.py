from rest_framework import routers
from django.urls import include, path
from django.contrib import admin
from links import views

router = routers.DefaultRouter()
router.register(r'links', views.LinkViewSet)
router.register(r'hits', views.LinkHitViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('<str:link_hash>', views.redirect_view),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
