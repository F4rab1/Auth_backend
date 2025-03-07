from django.urls import path
from .views import registration_email_view, registration_email_verify_view

urlpatterns = [
    path('registration/email/', registration_email_view, name='registration-email'),
    path('registration/email-verify/', registration_email_verify_view, name='email-verify'),
]