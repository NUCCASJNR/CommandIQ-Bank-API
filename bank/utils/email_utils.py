#!/usr/bin/env python3

"""
Handles all utils relating to sending emails and also generating tokens
"""

from django.conf import settings
from os import getenv
from bank.utils.redis_utils import RedisClient
from bank.models.user import User
import secrets
import random
import requests


API_KEY = getenv("ELASTIC_EMAIL_KEY")


class EmailUtils:
    @staticmethod
    def generate_verification_code(length=6):
        """
        Generate a random verification code.
        :param length: Length of the verification code (default is 6)
        :return: Random verification code
        """
        charset = "0123456789"  # You can customize this to include letters or other characters if needed
        verification_code = ''.join(secrets.choice(charset) for _ in range(length))
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
        request_payload = {
            "apikey": API_KEY,
            "from": "alareefadegbite@gmail.com",
            "to": user.email,
            "subject": "Verify your account",
            "bodyHtml": f"Hello {user.username},<br> Your verification code is {verification_code}",
            "isTransactional": False
        }
        try:
            response = requests.post(url, data=request_payload)
            if response.status_code == 200:
                print(response.json())
                return True
            else:
                print(f'Error sending verification email to {user.email}')
                return False
        except Exception as e:
            print(f'Error sending verification email to {user.email}: {e}')
            return False
