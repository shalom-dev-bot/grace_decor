# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    ROLE_CHOICES = (
        ('client', _('Client')),
        ('admin', _('Admin')),
        ('agency', _('Agency')),
    )
    
    LANGUAGE_CHOICES = (
        ('fr', _('Français')),
        ('en', _('English')),
        ('es', _('Español')),
        ('de', _('Deutsch')),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=False)  # inactif jusqu'à validation email
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    activation_token = models.CharField(max_length=128, blank=True, null=True)  # Ajout pour l'activation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
# ...existing code...
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    activation_token = models.CharField(max_length=128, blank=True, null=True)  # Ajout pour l'activation
    created_at = models.DateTimeField(auto_now_add=True)
# ...existing code...
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def display_name(self):
        return self.full_name or self.email

    @property
    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        return None

    def get_role_display_name(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    def get_language_display_name(self):
        return dict(self.LANGUAGE_CHOICES).get(self.language, self.language)

