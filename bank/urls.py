#!/usr/bin/env python3

"""Contains urls for the bank app"""

from django.urls import path
from bank.views.signup import UserRegistrationView, UserVerificationView
from bank.views.login import LoginView, LogoutView
from bank.views.reset_password import ResetPasswordView, ResetPasswordConfirmView

urlpatterns = [
    path('auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('auth/verify_email/', UserVerificationView.as_view(), name='verify_email'),
    # path('auth/login/', LoginViewSet.as_view({'post': 'login'}), name='login'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/password_reset/', ResetPasswordView.as_view(), name='reset_password'),
    path('auth/confirm_reset_token/', ResetPasswordConfirmView.as_view(), name='confirm_reset_token')
]