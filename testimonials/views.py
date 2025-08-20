from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Testimonial
from .serializers import (
    TestimonialSerializer, TestimonialCreateSerializer, 
    TestimonialUpdateSerializer, TestimonialAdminSerializer
)
from django.db import models

class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agency']:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(client=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return TestimonialCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TestimonialUpdateSerializer
        elif self.action in ['admin_update', 'approve', 'reject']:
            return TestimonialAdminSerializer
        return TestimonialSerializer

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request):
        """Récupérer les témoignages publics (approuvés)"""
        testimonials = Testimonial.objects.filter(status='approved').order_by('-is_featured', '-created_at')
        serializer = self.get_serializer(testimonials, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def featured(self, request):
        """Récupérer les témoignages mis en avant"""
        testimonials = Testimonial.objects.filter(status='approved', is_featured=True).order_by('-created_at')
        serializer = self.get_serializer(testimonials, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Récupérer les témoignages en attente (admin seulement)"""
        if self.request.user.role not in ['admin', 'agency']:
            return Response({"error": "Accès non autorisé"}, status=status.HTTP_403_FORBIDDEN)
        
        testimonials = Testimonial.objects.filter(status='pending').order_by('-created_at')
        serializer = TestimonialAdminSerializer(testimonials, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approuver un témoignage (admin seulement)"""
        if self.request.user.role not in ['admin', 'agency']:
            return Response({"error": "Accès non autorisé"}, status=status.HTTP_403_FORBIDDEN)
        
        testimonial = self.get_object()
        testimonial.status = 'approved'
        testimonial.approved_at = timezone.now()
        testimonial.approved_by = request.user
        testimonial.save()
        
        serializer = TestimonialAdminSerializer(testimonial)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Rejeter un témoignage (admin seulement)"""
        if self.request.user.role not in ['admin', 'agency']:
            return Response({"error": "Accès non autorisé"}, status=status.HTTP_403_FORBIDDEN)
        
        testimonial = self.get_object()
        testimonial.status = 'rejected'
        testimonial.admin_notes = request.data.get('admin_notes', '')
        testimonial.save()
        
        serializer = TestimonialAdminSerializer(testimonial)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_featured(self, request, pk=None):
        """Basculer le statut mis en avant (admin seulement)"""
        if self.request.user.role not in ['admin', 'agency']:
            return Response({"error": "Accès non autorisé"}, status=status.HTTP_403_FORBIDDEN)
        
        testimonial = self.get_object()
        testimonial.is_featured = not testimonial.is_featured
        testimonial.save()
        
        serializer = TestimonialAdminSerializer(testimonial)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_testimonials(self, request):
        """Récupérer les témoignages de l'utilisateur connecté"""
        testimonials = Testimonial.objects.filter(client=request.user).order_by('-created_at')
        serializer = self.get_serializer(testimonials, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des témoignages"""
        user = request.user
        queryset = Testimonial.objects.all() if user.role in ['admin', 'agency'] else Testimonial.objects.filter(client=user)
        
        stats = {
            'total': queryset.count(),
            'approved': queryset.filter(status='approved').count(),
            'pending': queryset.filter(status='pending').count(),
            'rejected': queryset.filter(status='rejected').count(),
            'featured': queryset.filter(is_featured=True).count(),
            'average_rating': queryset.filter(status='approved').aggregate(
                avg_rating=models.Avg('rating')
            )['avg_rating'] or 0
        }
        
        return Response(stats)
