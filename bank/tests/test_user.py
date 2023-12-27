#!/usr/bin/env python3

from django.test import TestCase
from bank.models.user import User


class CreateUserTest(TestCase):
    def test_create_user(self):
        """
        test case
        """
        user_dict = {
            'username': 'Al-Areef',
            'email': 'alareefadegbite@gmail.com',
            'first_name': 'Al-Areef',
            'last_name': 'Adegbite',
            'password': 'password123'
        }
        user = User.custom_save(**user_dict)
        self.assertEqual(user.username, user_dict['username'])
        self.assertEqual(user.email, user_dict['email'])