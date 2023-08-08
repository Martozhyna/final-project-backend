from apps.users.serializers import UserSerializer


class SwaggerUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at',
            'updated_at', 'profile'
        )