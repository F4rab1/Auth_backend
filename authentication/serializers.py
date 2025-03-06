from rest_framework import serializers
from .models import User


class RegistrationEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']