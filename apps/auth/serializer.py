# from django.contrib.auth import get_user_model
#
# from apps.users.models import UserModel as User
#
# from django.contrib.auth import authenticate
#
# from rest_framework import serializers
#
#
# class LoginSerializer(serializers.Serializer):
#     """
#     This serializer defines two fields for authentication:
#       * username
#       * password.
#     It will try to authenticate the user with when validated.
#     """
#     email = serializers.EmailField(
#         label="Email",
#         write_only=True
#     )
#     password = serializers.CharField(
#         label="Password",
#         # This will be used when the DRF browsable API is enabled
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         write_only=True
#     )
#
#     def validate(self, attrs):
#         # Take username and password from request
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         if email and password:
#             # Try to authenticate the user using Django auth framework.
#             user = authenticate(request=self.context.get('request'),
#                                 email=email, password=password)
#             if not user:
#                 # If we don't have a regular user, raise a ValidationError
#                 msg = 'Access denied: wrong username or password.'
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = 'Both "email" and "password" are required.'
#             raise serializers.ValidationError(msg, code='authorization')
#         # We have a valid user, put it in the serializer's validated_data.
#         # It will be used in the view.
#         attrs['user'] = user
#         return attrs
#
#
# UserModel: User = get_user_model()
#
#
# class EmailSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#
#
# class PasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ('password',)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..users.serializers import UserSerializer


class TokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data




