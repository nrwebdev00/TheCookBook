from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

signer = TimestampSigner(salt="email-confirmation")

def make_confirmation_token(user_id: str) -> str:
    return signer.sign(user_id)

def validate_email_token(token: str, max_age_seconds: int = 60*60*24) -> str:
    try:
        return signer.unsign(token, max_age=max_age_seconds)
    except SignatureExpired:
        raise SignatureExpired("The confirmation token has expired.")
    except BadSignature:
        raise BadSignature("The confirmation token is invalid.")