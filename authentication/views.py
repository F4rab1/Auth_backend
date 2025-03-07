from rest_framework import generics, status
from rest_framework.response import Response
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import jwt
from .serializers import RegistrationEmailSerializer
from .models import User


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def registration_email_view(request):
    if request.method == 'GET':
        return Response({"ok"})
    elif request.method == 'POST':
        serializer = RegistrationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('verify-email')
        absolute_link = f"http://{current_site}{relative_link}?token={token}"

        return Response({"email": user.email, "verification_link": absolute_link}, status=status.HTTP_201_CREATED)


class VerifyEmailView(generics.CreateAPIView):
    print("Hello yeiuf")

    def get_serializer_class(self):
        return RegistrationEmailSerializer

    def get(self, request, *args, **kwargs):
        return Response({"ok"})
    # permission_classes = [AllowAny]  # Allow unauthenticated access
    #
    # def get(self, request, *args, **kwargs):
    #     token = request.GET.get("token")
    #     if not token:
    #         return Response({"error": "Token is missing."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     try:
    #         # Decode the token using the project's SECRET_KEY and the HS256 algorithm.
    #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    #         user = User.objects.get(id=payload["user_id"])
    #
    #         # If the user isn't verified yet, mark them as verified.
    #         if not user.is_verified:
    #             user.is_verified = True
    #             user.save()
    #
    #         return Response({"detail": "Email successfully activated"}, status=status.HTTP_200_OK)
    #
    #     except jwt.ExpiredSignatureError:
    #         return Response({"error": "Activation link expired"}, status=status.HTTP_400_BAD_REQUEST)
    #     except jwt.exceptions.DecodeError:
    #         return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)