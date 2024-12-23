from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


from .views import (
    UserCreateAPI,
    OTPSendAPI,
    OTPVerifyAPI,
    UserAPI,
    UserUpdateAPI,
    UserDeleteAPI
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('create/', UserCreateAPI.as_view()),
    path('otp-send/', OTPSendAPI.as_view()),
    path('otp-verify/', OTPVerifyAPI.as_view()),
    path('<int:id>/', UserAPI.as_view()),
    path('<int:id>/update/', UserUpdateAPI.as_view()),
    path('<int:id>/delete/', UserDeleteAPI.as_view()),
]