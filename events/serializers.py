# events/serializers.py
from rest_framework import serializers
from .models import Event
from packages.serializers import PackageSerializer
from packages.models import Package

class EventSerializer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)  # Affiche les infos complètes du package
    package_id = serializers.PrimaryKeyRelatedField(
        queryset=Package.objects.all(),
        source='package',
        write_only=True
    )

    class Meta:
        model = Event
        fields = '__all__'
