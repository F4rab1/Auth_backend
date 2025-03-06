from django.urls import path
from .views import RegistrationEmailView, VerifyEmailView

urlpatterns = [
    path('registration/email/', RegistrationEmailView.as_view(), name='registration-email'),
    path('registration/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]