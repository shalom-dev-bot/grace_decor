from rest_framework import serializers
from .models import Testimonial
from core.serializers import UserSerializer

class TestimonialSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    stars = serializers.ReadOnlyField()
    is_approved = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    is_rejected = serializers.ReadOnlyField()
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    approved_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = Testimonial
        fields = [
            'id', 'client', 'title', 'content', 'rating', 'stars',
            'event_type', 'event_date', 'location', 'client_image',
            'is_featured', 'status', 'admin_notes', 'created_at',
            'updated_at', 'approved_at', 'approved_by',
            'is_approved', 'is_pending', 'is_rejected'
        ]
        read_only_fields = ['id', 'client', 'created_at', 'updated_at', 
                           'approved_at', 'approved_by', 'is_approved', 
                           'is_pending', 'is_rejected']

class TestimonialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'title', 'content', 'rating', 'event_type', 'event_date',
            'location', 'client_image'
        ]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit être entre 1 et 5")
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            data['client'] = request.user
        return data

class TestimonialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'title', 'content', 'rating', 'event_type', 'event_date',
            'location', 'client_image'
        ]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit être entre 1 et 5")
        return value

class TestimonialAdminSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)

    class Meta:
        model = Testimonial
        fields = [
            'id', 'client', 'title', 'content', 'rating', 'stars',
            'event_type', 'event_date', 'location', 'client_image',
            'is_featured', 'status', 'admin_notes', 'created_at',
            'updated_at', 'approved_at', 'approved_by',
            'is_approved', 'is_pending', 'is_rejected'
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if 'status' in data and data['status'] == 'approved':
                data['approved_by'] = request.user
        return data
