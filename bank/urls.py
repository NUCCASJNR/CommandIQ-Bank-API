#!/usr/bin/env python3

"""Contains urls for the bank app"""

from django.urls import path
from bank.views.signup import UserRegistrationView

urlpatterns = [
    path('auth/signup/', UserRegistrationView.as_view(), name='signup'),
]

