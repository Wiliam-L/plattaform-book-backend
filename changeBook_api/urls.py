
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.authentication.views import UserCreateView, getUser, LoginView, VeryEmailApiView, getEmailVerification, getIcon
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', getUser, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('apps.book.urls')),
    path('ad/', include('apps.administrator.urls')),
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='tokenrefresh'),
    path('email-verification/', VeryEmailApiView.as_view(), name='email-verification'),
    path('showEmailVerification/', getEmailVerification.as_view(), name='showEmail'),
    path('showicon/', getIcon.as_view(), name='showicon')
]


