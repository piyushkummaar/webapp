from django.urls import path
from accounts.views import (
    RegisterView, LoginView, LogoutView,
    ProfileView, ChangePasswordView,
    PasswordResetView, PasswordResetConfirmView
)


app_name = "accounts"


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', PasswordResetView.as_view(),
         name='password_reset'),
    path('reset/<str:random_str>/<uuid:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')


]
