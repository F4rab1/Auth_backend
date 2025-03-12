from rest_framework import generics, status
from rest_framework.response import Response
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import jwt
from .serializers import RegistrationEmailSerializer, PasswordRegistrationSerializer
from .models import User
from django.conf import settings


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def registration_email_view(request):
    if request.method == 'GET':
        return Response({"ok"})
    elif request.method == 'POST':
        try:
            user = User.objects.get(email=request.data['email'])
            if user.is_verified:
                return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            serializer = RegistrationEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absolute_link = f"http://{current_site}{relative_link}?token={token}"

        return Response({"email": user.email, "verification_link": absolute_link}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def registration_email_verify_view(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        if not token:
            return Response({"error": "Token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"email": user.email, "verified": True})
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"error": "Token is expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidTokenError:
            return Response({"error": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([AllowAny])
def password_registration_view(request):
    email = request.query_params.get('email')
    if not email:
        return Response({"error": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PasswordRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    new_password = serializer.validated_data['password']
    user.set_password(new_password)
    user.save()

    return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
