
# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import CustomUser

class Testimonial(models.Model):
    RATING_CHOICES = [
        (1, _('1 étoile')),
        (2, _('2 étoiles')),
        (3, _('3 étoiles')),
        (4, _('4 étoiles')),
        (5, _('5 étoiles')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('approved', _('Approuvé')),
        ('rejected', _('Rejeté')),
    ]
    
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='testimonials')
    title = models.CharField(max_length=200, verbose_name=_('Titre'))
    content = models.TextField(verbose_name=_('Contenu'))
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name=_('Note'))
    event_type = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Type d\'événement'))
    event_date = models.DateField(blank=True, null=True, verbose_name=_('Date de l\'événement'))
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Lieu'))
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name=_('Photo du client'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Mis en avant'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Statut'))
    admin_notes = models.TextField(blank=True, null=True, verbose_name=_('Notes administrateur'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Date de modification'))
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Date d\'approbation'))
    approved_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='approved_testimonials',
        verbose_name=_('Approuvé par')
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Témoignage')
        verbose_name_plural = _('Témoignages')

    def __str__(self):
        return f"Témoignage de {self.client.username} - {self.title}"

    @property
    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

    @property
    def is_approved(self):
        return self.status == 'approved'

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_rejected(self):
        return self.status == 'rejected'
