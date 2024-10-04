from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostBookViewSet

router = DefaultRouter()
router.register(r'post-book', PostBookViewSet, basename='post-book')

urlpatterns = [
    path('', include(router.urls)),
]