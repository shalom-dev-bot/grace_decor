from rest_framework import serializers
from .models import Package
from services.serializers import ServiceSerializer

class PackageSerializer(serializers.ModelSerializer):
    # Sérialisation complète des services liés
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        # Tous les champs du Package, y compris les nouveaux
        fields = ['id', 'name', 'description', 'price', 'services', 'service_type', 'created_at', 'updated_at', 'image']
