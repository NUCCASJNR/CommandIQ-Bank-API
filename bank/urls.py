#!/usr/bin/env python3

"""Contains urls for the bank app"""

from django.urls import path
from bank.views.signup import UserRegistrationView, UserVerificationView
from bank.views.login import LoginViewSet

urlpatterns = [
    path('auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('auth/verify_email/', UserVerificationView.as_view(), name='verify_email'),
    path('auth/login/', LoginViewSet.as_view({'post': 'login'}), name='login')
]

