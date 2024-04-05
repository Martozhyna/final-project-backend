from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.services.email_service import EmailService

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    # confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserModel
        fields = (
            'id', 'email', 'password', 'name', 'surname', 'is_active', 'is_staff', 'is_superuser', 'last_login',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at', 'updated_at')

    # def validate(self, data):
    #     if data.get('password') != data.get('confirm'):
    #         raise serializers.ValidationError("Passwords do not match")
    #     return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserModel.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        EmailService.register_email(user)
        return user
