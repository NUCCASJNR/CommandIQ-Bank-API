from rest_framework import serializers
from bank.models.user import User
from bank.utils.redis_utils import RedisClient


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for Handling resetting a user password
    """
    username = serializers.CharField()

    # class Meta:
    #     model = User
    #     fields = ['username']
    #     read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        """
        Validate a username or email first before sending the reset password token to the user
        email address
        :param data: username or email provided
        :return: The user obj
        """
        username = data['username']
        try:
            if '@' in username:
                user = User.find_obj_by(email=username)
            else:
                user = User.find_obj_by(username=username)
            if user:
                return data
        except ObjectDoesNotExist:
            raise serializers.ValidationError('User not found')
        return data


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming the reset password token
    """
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['token', 'new_password']

    # def validate(self, data):
    #     """
    #     Validate the reset password token and new password
    #     """
    #     token = data['token']
    #     new_password = data['new_password']
    #     if token and new_password:
    #         try:
    #             redis_client = RedisClient()
    #             key = f'reset_token:{user.id}:{reset_code}'
    #     return data