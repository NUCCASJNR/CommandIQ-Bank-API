#!/usr/bin/env python3

"""
Handles all utils relating to sending emails and also generating tokens
"""

from django.conf import settings
from os import getenv
from bank.utils.redis_utils import RedisClient
from bank.models.user import User
import random
import string
import requests


API_KEY = getenv("ELASTIC_EMAIL_API_KEY")


class EmailUtils:
    @staticmethod
    def generate_verification_code():
        """
        Generates a random verification code
        """
        verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        return verification_code

    @staticmethod
    def send_verification_email(user: User):
        """
        Sends a verification email to the user
        """
        verification_code = EmailUtils.generate_verification_code()
        redis_client = RedisClient()
        key = f'user:{user.id}:{verification_code}'
        redis_client.set_key(key, verification_code, expiry=30)
        user.verified = False
        user.verification_code = verification_code
        url = "https://api.elasticemail.com/v2/email/send"
        payload = {
            "apikey": API_KEY,
            "subject": "Verify your account",
            "from": "community-catalyst@polyglotte.tech",
            "to": user.email,
            "bodyHtml": f"Hello {user.username},<br> Your verification code is {verification_code}",
            "isTransactional": False
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print(f'Verification email sent to {user.email}')
                return True
            else:
                print(f'Error sending verification email to {user.email}')
                return False
        except Exception as e:
            print(f'Error sending verification email to {user.email}: {e}')
            return False
