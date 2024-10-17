from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostBookViewSet
from apps.book.views import ExchageTypeView, CategoryView

router = DefaultRouter()
router.register(r'post-book', PostBookViewSet, basename='post-book')
router.register(r'category', CategoryView, basename='category')
router.register(r'type', ExchageTypeView, basename='type')

urlpatterns = [
    path('', include(router.urls)),
]