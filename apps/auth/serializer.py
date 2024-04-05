from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import UserModel as User

from ..users.serializers import UserSerializer

UserModel: User = get_user_model()

class TokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data



class AuthPasswordSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('password',)



