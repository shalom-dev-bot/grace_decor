from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('decoration', 'Decoration'),
        ('catering', 'Catering'),
        ('cake', 'Cake'),
        ('wedding_dress', 'Wedding Dress'),
        ('photography', 'Photography'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.name
