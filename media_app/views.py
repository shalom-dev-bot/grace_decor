from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Media
from .serializers import MediaSerializer

# Liste tous les médias
class MediaListAPIView(generics.ListAPIView):
    queryset = Media.objects.all().order_by('-uploaded_at')
    serializer_class = MediaSerializer

# Détails d’un média
class MediaDetailAPIView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
