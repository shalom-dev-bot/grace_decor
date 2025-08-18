
from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserProfileView, 
    UserProfileImageView, activate_account, change_password, 
    resend_activation_email
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/upload-image/', UserProfileImageView.as_view(), name='profile-upload-image'),
    path('activate/<str:token>/', activate_account, name='activate'),
    path('change-password/', change_password, name='change-password'),
    path('resend-activation/', resend_activation_email, name='resend-activation'),
]
