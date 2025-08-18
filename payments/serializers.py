from rest_framework import serializers
from .models import Payment
from bookings.serializers import BookingSerializer
from core.serializers import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    booking_id = serializers.IntegerField(write_only=True)
    
    # Champs calculés
    is_paid = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    is_failed = serializers.ReadOnlyField()
    
    # Formatage des dates
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    paid_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'booking_id', 'client', 'amount', 'currency',
            'payment_method', 'status', 'transaction_id', 'payment_intent_id',
            'billing_name', 'billing_email', 'billing_phone', 'description',
            'metadata', 'created_at', 'updated_at', 'paid_at',
            'is_paid', 'is_pending', 'is_failed'
        ]
        read_only_fields = ['id', 'client', 'transaction_id', 'payment_intent_id', 
                           'created_at', 'updated_at', 'paid_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être supérieur à 0")
        return value

    def validate(self, data):
        # Vérifier que l'utilisateur est connecté
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            data['client'] = request.user
        
        return data

class PaymentCreateSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField()
    
    class Meta:
        model = Payment
        fields = [
            'booking_id', 'amount', 'currency', 'payment_method',
            'billing_name', 'billing_email', 'billing_phone', 'description'
        ]

    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Vous devez être connecté pour effectuer un paiement")
        
        data['client'] = request.user
        return data

class PaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status', 'transaction_id', 'payment_intent_id']
        read_only_fields = ['transaction_id', 'payment_intent_id']
