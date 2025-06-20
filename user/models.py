from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=True)
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['username', 'email']
# Profile model linked to custom user
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('reader', 'Reader'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.role}'

# Signals: connect to custom user model via settings.AUTH_USER_MODEL
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='reader')

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
