from django.urls import path
from .views import registration_email_view, registration_email_verify_view, password_registration_view, login_view

urlpatterns = [
    path('registration/email/', registration_email_view, name='registration-email'),
    path('registration/email-verify/', registration_email_verify_view, name='email-verify'),
    path('registration/password/', password_registration_view, name='registration-password'),
    path('login/', login_view, name='login'),
]