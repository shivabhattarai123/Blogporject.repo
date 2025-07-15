from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom User model


class User(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=True)
    
    USERNAME_FIELD = "phone_number" # phone number magaxa login garni bela ma username ko sata
    REQUIRED_FIELDS = ['username', 'email']

# Profile model linked to custom user
class UserProfile(models.Model): #Defines a UserProfile linked to each user, with a role field (author or reader)
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('reader', 'Reader'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link each profile to exactly one user (one-to-one relationship)  
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)     # Role assigned to the user (either 'author' or 'reader')
    bio = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} - {self.role}'

# Signals: connect to custom user model via settings.AUTH_USER_MODEL
@receiver(post_save, sender=settings.AUTH_USER_MODEL)  #Automatically creates a UserProfile when a new user is registered.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='reader')   # Assigns 'reader' as default role when creating new user

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):    # Check if user has an attached profile before saving
        instance.userprofile.save()
