#!/usr/bin/env python3

"""Contains Login view"""

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from bank.models.user import User
from bank.serializers.login import AuthTokenSerializer


class LoginView(APIView):
    """API View for login"""
    
    def post(self, request, *args, **kwargs):
        """
        Handles Post request for login
        """
        serializer = AuthTokenSerializer(data=request.data)
        # if not serializer.is_valid():
        #     print(f"Manual Validation Errors: {serializer.errors}")

        print(request.data)
        print(f'Password:', serializer.initial_data['password'])
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        print(f'Username: {username}')

        user = authenticate(username=username, password=password)
        print(f'user: {user}')
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


# #!/usr/bin/env python3

# """Contains Login view"""

# from rest_framework import status, viewsets
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import action
# from django.contrib.auth import authenticate
# from bank.models.user import User
# from bank.serializers.login import AuthTokenSerializer


# class LoginViewSet(viewsets.ModelViewSet):
#     """
#     Viewset for user login
#     """
#     queryset = User.objects.all()
#     serializer_class = AuthTokenSerializer

#     @action(methods=['POST'], detail=False)
#     def login(self, request):
#         """
#         Login user
#         """
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(request.data)
#         if not serializer.is_valid():
#             user = authenticate(
#                 username=serializer.validated_data['username'],
#                 password=serializer.validated_data['password']
#             )
#             print(User.to_dict(user))
#             if user:
#                 token, created = Token.objects.get_or_create(user=user)
#                 return Response({
#                     'message': 'Login successful',
#                     'token': token.key,
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({
#                     'message': 'Invalid credentials'
#                 }, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({
#                 'message': 'Invalid serializers'
#             }, status=status.HTTP_400_BAD_REQUEST)