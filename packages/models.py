from django.db import models
from services.models import Service

class Package(models.Model):
    SERVICE_TYPES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('vip', 'VIP'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    services = models.ManyToManyField(Service, related_name='packages')
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPES, default='classic')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='packages/', blank=True, null=True)  # optionnel pour photo du package

    def __str__(self):
        return self.name
