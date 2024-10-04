from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostBookViewSet, UploadView

router = DefaultRouter()
router.register(r'postbook', PostBookViewSet, basename='postbook')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', UploadView.as_view(), name="upload_image")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

