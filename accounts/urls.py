from django.urls import path
from .views import RegisterView, ConfirmEmailView, ResendEmailConfirmation

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/<str:token>', ConfirmEmailView.as_view(), name='confirm-email'),  
    path('resend-email-token/', ResendEmailConfirmation.as_view(), name='resend-email-token'),
]