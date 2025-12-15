from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.utlis.responses import standard_response
from core.tokens import validate_email_token, make_confirmation_token
from core.email import send_confirmation_email as send_mail

Account = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")
        password = request.data.get("password") 

        if not email or not password:
            return standard_response(
                success=False,
                msg="",
                error_english="Email and password are required.",
                error={},
                status_code=400
            )

        if Account.objects.filter(email=email).exists():
            return standard_response(
                success=False,
                msg="",
                error_english="A user with this email already exists.",
                error={"email": "A user with this email already exists."},
                status_code=400
            )
        
        account = Account.objects.create_user(email=email, name=name, password=password)

        token = make_confirmation_token(str(account.id))
        url = reverse('accounts:confirm-email', args=[token])
        confirm_url = f"{settings.SITE_URL}{url}"
        send_mail(email=account.email, confirm_url=confirm_url)

        refresh = RefreshToken.for_user(account)
        data = {
            "account":{
                "id": str(account.id),
                "email": account.email,
                "name": account.name,
                "is_email_verified": account.is_email_verified,
            },
            "tokens":{
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "confirm_url": confirm_url
        }
        return standard_response(
            success=True,
            msg="User registered successfully. Please check your email to confirm your address.",
            data=data,
            status_code=201
        )

class ConfirmEmailView(APIView): 
    def get(self, request, token: str):
        uid = validate_email_token(token)
        if not uid:
            return standard_response(
                success=False,
                msg="",
                error_english="Invalid or expired token.",
                error={},
                status_code=400
            )
        try:
            user = Account.objects.get(id=uid)
        except Account.DoesNotExist:
            return standard_response(
                success=False,
                msg="",
                error_english="User not found.",
                error={},
                status_code=404
            )
        if user.is_email_verified:
            return standard_response(
                success=True,
                msg="Email is already verified.",
                data={},
                status_code=200
            )

            
        user.is_email_verified = True
        user.save(update_fields=['is_email_verified'])

        return standard_response(
            success=True,
            msg="Email verified successfully.",
            data={
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "name": user.name,
                    "is_email_verified": user.is_email_verified,
                }
            },
            status_code=200
        )
    
class ResendEmailConfirmation(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return standard_response(
                success=False,
                msg="",
                error_english="Email is required.",
                error={"email": "Email is required"},
                status_code=400
            )
        
        try: 
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return standard_response(
                success=False,
                msg="",
                error_english="User not found.",
                error={"email":"No Emaill address register."},
                status_code=404
            )
        
        if user.is_email_verified:
            return standard_response(
                success=True,
                msg="Email Address is already verified.",
                data={},
                status_code=200
            )
        
        token = make_confirmation_token(str(user.id))
        url = reverse('accounts:confirm-email', args=[token])
        confirm_url = f"{settings.SITE_URL}{url}"
        send_mail(email=user.email, confirm_url=confirm_url)

        return standard_response(
            success=True,
            msg="A new confirmation email has been sent.",
            data={"confirm_url": confirm_url},
            status_code=200
        )