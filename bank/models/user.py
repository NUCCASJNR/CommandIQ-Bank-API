#!/usr/bin/env python3

"""Contains user model."""

from bank.models.base_model import BaseModel, models
from django.contrib.auth.models import AbstractUser, Group, Permission


def user_profile_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_images/<user_id>/<filename>
    return f'profile_images/{instance.id}/{filename}'


class User(AbstractUser, BaseModel):
    """User class"""

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(max_length=255, null=True, upload_to=user_profile_image_path)
    verification_code = models.CharField(max_length=50, blank=True, null=True)
    verified = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=16, blank=True)

    groups = models.ManyToManyField(Group, blank=True, related_name='bank_user_groups')

    # Add related_name to resolve clashes with auth.User.user_permissions
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='bank_user_permissions')

    class Meta:
        """Meta class"""
        db_table = 'users'

    def save(self, *args, **kwargs):
        """
        Save The hash password
        :param args: Optional Arg
        :param kwargs: Keyword argument
        :return: user obj
        """
        self.set_password(self.password)
        super(User, self).save(*args, **kwargs)
