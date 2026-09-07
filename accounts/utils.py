import random
from django.core.mail import send_mail
from django.conf import settings



class EmailService:
    def __init__(self, sender):
        self.sender = sender
        
    def generate_otp(self):
        return str(random.randint(100000, 999999))
    
    def send_otp_mail(self, email, otp):
        
        print("========== EMAIL DEBUG ==========")
        print("EMAIL HOST:", settings.EMAIL_HOST)
        print("EMAIL PORT:", settings.EMAIL_PORT)
        print("EMAIL TLS:", settings.EMAIL_USE_TLS)
        print("EMAIL USER:", settings.EMAIL_HOST_USER)
        print("PASSWORD LENGTH:", len(settings.EMAIL_HOST_PASSWORD))
        print("SENDER:", self.sender)
        print("RECIPIENT:", email)
        print("=================================")

        
        send_mail(
            subject = "Email Verification OTP",
            message = f"Your OTP for email verification is: {otp}",
            from_email = self.sender,
            recipient_list = [email],
            fail_silently = False
            
        )
    