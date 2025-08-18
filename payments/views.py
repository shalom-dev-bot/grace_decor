from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer, PaymentStatusUpdateSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'agency']:
            return Payment.objects.all()
        return Payment.objects.filter(client=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        elif self.action in ['update_status', 'partial_update']:
            return PaymentStatusUpdateSerializer
        return PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        
        # Mettre à jour le statut de la réservation
        booking = payment.booking
        if payment.amount >= booking.amount_paid or booking.amount_paid is None:
            booking.amount_paid = payment.amount
            if payment.status == 'completed':
                booking.status = 'confirmed'
            booking.save()

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        payment = self.get_object()
        serializer = self.get_serializer(payment, data=request.data, partial=True)
        
        if serializer.is_valid():
            old_status = payment.status
            payment = serializer.save()
            
            # Si le paiement est complété, mettre à jour la date de paiement
            if payment.status == 'completed' and old_status != 'completed':
                payment.paid_at = timezone.now()
                payment.save()
                
                # Mettre à jour le statut de la réservation
                booking = payment.booking
                booking.status = 'confirmed'
                booking.save()
            
            return Response(PaymentSerializer(payment).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        payments = self.get_queryset().filter(client=request.user)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_payments(self, request):
        payments = self.get_queryset().filter(status__in=['pending', 'processing'])
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed_payments(self, request):
        payments = self.get_queryset().filter(status='completed')
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def payment_stats(self, request):
        user = request.user
        queryset = Payment.objects.filter(client=user) if user.role not in ['admin', 'agency'] else Payment.objects.all()
        
        stats = {
            'total_payments': queryset.count(),
            'total_amount': sum(payment.amount for payment in queryset if payment.status == 'completed'),
            'pending_payments': queryset.filter(status__in=['pending', 'processing']).count(),
            'completed_payments': queryset.filter(status='completed').count(),
            'failed_payments': queryset.filter(status__in=['failed', 'cancelled']).count(),
        }
        
        return Response(stats)

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        payment = self.get_object()
        
        # Simulation de traitement de paiement
        # Dans un vrai projet, vous intégreriez Stripe, PayPal, etc.
        
        payment.status = 'processing'
        payment.save()
        
        # Simuler un délai de traitement
        import time
        time.sleep(1)
        
        # Simuler un succès (90% de chance)
        import random
        if random.random() > 0.1:  # 90% de succès
            payment.status = 'completed'
            payment.paid_at = timezone.now()
            payment.transaction_id = f"TXN_{payment.id}_{int(timezone.now().timestamp())}"
            payment.save()
            
            # Mettre à jour la réservation
            booking = payment.booking
            booking.status = 'confirmed'
            booking.save()
            
            return Response({
                'success': True,
                'message': 'Paiement traité avec succès',
                'payment': PaymentSerializer(payment).data
            })
        else:
            payment.status = 'failed'
            payment.save()
            
            return Response({
                'success': False,
                'message': 'Échec du traitement du paiement',
                'payment': PaymentSerializer(payment).data
            }, status=status.HTTP_400_BAD_REQUEST)
