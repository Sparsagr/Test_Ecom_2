from django.core.mail import send_mail
import uuid
from django.conf import settings

def send_Account_Activation_mail(email, token):
    subject = "Activate your account"
    message = f"Hi {email},\nPlease click on the link below to activate your account\nhttp://127.0.0.1:8000/accounts/activate/{token}/"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print("Sending Email")
    send_mail(subject, message, from_email, recipient_list)
