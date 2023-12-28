#!/usr/bin/env python3

"""
Handles all utils relating to sending emails and also generating tokens
"""

from django.conf import settings
from django.core.mail import send_mail
import os
from bank.utils.redis_utils import RedisClient

API_KEY = os.getenv("ELASTIC_EMAIL_API_KEY")

