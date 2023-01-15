from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterUserAPIView, EmailVerifyAPIView, LogoutAPIView

urlpatterns = [
    path('signup/', RegisterUserAPIView.as_view(), name='signup'),
    path('email-verify/', EmailVerifyAPIView.as_view(), name='email-verify'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout')
]
