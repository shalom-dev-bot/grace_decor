from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.core.mail import send_mail

def generate_activation_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_activation_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except:
        return None
    return email

def send_activation_email(user_email, token):
    activation_link = f"http://127.0.0.1:8000/api/core/activate/{token}/"
    subject = "Activate your Glow Gracious Events account"
    message = f"Click the link to activate your account: {activation_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
