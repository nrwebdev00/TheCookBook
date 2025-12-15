from django.core.mail import send_mail as django_send_mail
from django.conf import settings

def send_confirmation_email(email: str, confirm_url: str):
    subject = "Confirm your email"
    message = f"Please confirm your email by clicking the following link: {confirm_url}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    django_send_mail(subject, message, from_email, recipient_list)
