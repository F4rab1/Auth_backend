from django.urls import path
from .views import registration_email_view, VerifyEmailView

urlpatterns = [
    path('registration/email/', registration_email_view, name='registration-email'),
    path('registration/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]