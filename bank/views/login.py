#!/usr/bin/env python3

"""Contains Login view"""

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from bank.models.user import User
from bank.serializers.login import AuthTokenSerializer, ResetPasswordSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from bank.utils.email_utils import EmailUtils
from django.core.exceptions import ObjectDoesNotExist


class LoginView(APIView):
    """API View for login"""

    def post(self, request, *args, **kwargs):
        """
        Handles Post request for login
        """
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.verified:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Login successful',
                    'token': token.key,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Account not verified'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Logout view to invalidate the user's authentication token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles POST request for user logout.
        """
        # Get the user's authentication token
        auth_token = request.auth

        if auth_token:
            # Delete the user's authentication token
            auth_token.delete()
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordView(APIView):
    """
    Reset password View for sending reset token to user
    """
    def post(self, request, *args, **kwargs):
        """
        Handles POST request for sending reset token to user
        :param request: Request obj
        :param args: AArgument
        :param kwargs: Optional keyword arguments
        :return: Nothing
        """
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        try:
            if '@' in username:
                user = User.custom_get(**{'email': username})
            else:
                user = User.custom_get(**{'username': username})
            verification_code = EmailUtils.generate_verification_code()
            user_email = User.to_dict(user)['email']
            # Send Email to user
            EmailUtils.send_password_reset_email(user, verification_code, user_email)
            response_data = {
                "message": "Reset password token successfully sent",
                "email": User.to_dict(user)['email']
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": 'Incorrect Email Address or Username'}, status=status.HTTP_400_BAD_REQUEST)
