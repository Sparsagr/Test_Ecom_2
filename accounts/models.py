# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from core.emails import send_account_activation_email
# from django.contrib.auth.models import User
# import uuid

# # Create your models here.



# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     forgot_password_token = models.CharField(max_length=100, null=True, blank=True)
#     is_email_verified = models.BooleanField(default=False)
#     email_token = models.CharField(max_length=100, null=True, blank=True)
#     is_cv_uploaded = models.BooleanField(default=False)

#     def __str__(self) -> str:
#         return self.user.username + " - " + (lambda: "Not Verified", lambda: "Verified User")[self.is_email_verified]()

# @receiver(post_save, sender=User)
# def send_email_token(sender, instance, created, **kwargs):
#     try:
#         if created:
#             email_token = str(uuid.uuid4())
#             Profile.objects.create(user=instance, email_token=email_token)
#             email = instance.email
#             send_account_activation_email(email, email_token)
#     except Exception as e:
#         print(e)