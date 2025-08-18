
# Create your models here.
from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)  # URL vers la vidéo
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
