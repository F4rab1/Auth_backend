from rest_framework import serializers
from .models import User


class RegistrationEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username', '')

        if username is '':
            username = email.split('@')[0]
            validated_data['username'] = username

        user = User.objects.create_user(**validated_data)
        return user


class RegistrationVerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ['token']