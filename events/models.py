from django.db import models
from packages.models import Package
from core.models import CustomUser

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('vip', 'VIP'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    date = models.DateField()
    location = models.CharField(max_length=255)
    images = models.ImageField(upload_to='event_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    internal_notes = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.client.username}"
