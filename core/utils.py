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

def send_activation_email(user):
    # Generate and persist activation token on the user
    token = generate_activation_token(user.email)
    user.activation_token = token
    user.is_active = False
    user.email_verified = False
    user.save()

    frontend_base = getattr(settings, 'FRONTEND_BASE_URL', 'http://localhost:5173')
    activation_link = f"{frontend_base}/activate/{token}"
    subject = "Activez votre compte Glow Gracious Events"
    message = f"Cliquez sur le lien pour activer votre compte : {activation_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
