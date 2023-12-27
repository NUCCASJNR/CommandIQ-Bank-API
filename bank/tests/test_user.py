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
        print(User.find_obj_by(**{'username': 'Al-Areef'}))

    def test_update_user(self):
        user = User.find_obj_by(**{'username': 'Al-Areef'})
        try:
            User.custom_update(**{'username': user},  **{'password': 'idanre123@', 'email': 'al@gmail.com'})
            print(user)
        except Exception as e:
            print(str(e))
        self.assertEqual(User.to_dict(user)['email'], 'al@gmail.com')

    def test_delete_user(self):
        try:
            user = User.find_obj_by(**{'username': 'Al-Areef'})
            self.assertNotIsInstance(user, User)
            User.custom_delete(**{'username': user})
        except Exception as e:
            print(str(e))
        self.assertNotIsInstance(user, User)
