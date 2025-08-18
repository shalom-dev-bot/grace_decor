# bookings/serializers.py
from rest_framework import serializers
from .models import Booking
from events.serializers import EventSerializer
from core.serializers import UserSerializer
from events.models import Event
from core.models import CustomUser

class BookingSerializer(serializers.ModelSerializer):
    # Affichage complet pour GET
    event = EventSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    # Champs pour POST/PUT
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source='event',
        write_only=True
    )
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='client',
        write_only=True
    )

    class Meta:
        model = Booking
        fields = '__all__'
