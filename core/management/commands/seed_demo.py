from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from services.models import Service
from packages.models import Package
from announcements.models import Announcement
from events.models import Event
from testimonials.models import Testimonial
from bookings.models import Booking
from payments.models import Payment


class Command(BaseCommand):
    help = "Seed demo data for Grace Events"

    def handle(self, *args, **options):
        User = get_user_model()

        admin, _ = User.objects.get_or_create(
            email='admin@grace.local',
            defaults={
                'username': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'role': 'admin',
            }
        )
        client, _ = User.objects.get_or_create(
            email='client@grace.local',
            defaults={
                'username': 'client',
                'is_active': True,
                'role': 'client',
            }
        )
        if not client.has_usable_password():
            client.set_password('Client#1234')
            client.save()

        # Services
        svc_specs = [
            ("Décoration florale", "Décorations florales élégantes", 500, 'decoration'),
            ("Traiteur gourmet", "Buffet et service traiteur", 1500, 'catering'),
            ("Wedding cake", "Gâteau de mariage sur mesure", 300, 'cake'),
            ("Robe de mariée", "Sélection de robes de mariée", 1200, 'wedding_dress'),
            ("Photographie", "Pack photo professionnel", 800, 'photography'),
        ]
        services = []
        for name, desc, price, cat in svc_specs:
            svc, _ = Service.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'price': price,
                    'category': cat,
                }
            )
            services.append(svc)

        # Packages
        classic, _ = Package.objects.get_or_create(
            name='Classique',
            defaults={
                'description': "Forfait classique pour événements familiaux",
                'price': 2500,
                'service_type': 'classic',
            }
        )
        classic.services.set(services[:3])

        modern, _ = Package.objects.get_or_create(
            name='Moderne',
            defaults={
                'description': "Forfait moderne pour entreprises",
                'price': 4000,
                'service_type': 'modern',
            }
        )
        modern.services.set(services[1:])

        vip, _ = Package.objects.get_or_create(
            name='VIP',
            defaults={
                'description': "Forfait premium VIP",
                'price': 8000,
                'service_type': 'vip',
            }
        )
        vip.services.set(services)

        # Announcements
        Announcement.objects.get_or_create(
            title="Nouveaux packages 2025",
            defaults={
                'description': "Découvrez nos offres 2025 pour vos événements.",
                'video_url': None,
            }
        )

        # Events
        event1, _ = Event.objects.get_or_create(
            title='Mariage Élégant',
            client=client,
            defaults={
                'description': 'Cérémonie et réception dans un cadre idyllique',
                'package': classic,
                'event_type': 'classic',
                'date': timezone.now().date(),
                'location': 'Paris',
                'status': 'planned',
                'total_price': 3000,
            }
        )

        event2, _ = Event.objects.get_or_create(
            title='Lancement Produit',
            client=client,
            defaults={
                'description': 'Événement entreprise moderne',
                'package': modern,
                'event_type': 'modern',
                'date': timezone.now().date(),
                'location': 'Lyon',
                'status': 'planned',
                'total_price': 5000,
            }
        )

        # Testimonials
        Testimonial.objects.get_or_create(
            client=client,
            title='Service exceptionnel',
            defaults={
                'content': 'Organisation parfaite, équipe très professionnelle.',
                'rating': 5,
                'is_featured': True,
                'status': 'approved',
            }
        )

        # Bookings
        booking1, _ = Booking.objects.get_or_create(
            event=event1,
            client=client,
            defaults={
                'status': 'pending',
                'amount_paid': 0,
            }
        )

        # Payments
        Payment.objects.get_or_create(
            booking=booking1,
            client=client,
            amount=500,
            currency='EUR',
            payment_method='card',
            defaults={
                'status': 'completed',
                'transaction_id': f'TXN_{timezone.now().timestamp()}',
                'billing_name': 'Client Démo',
                'billing_email': client.email,
            }
        )

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))


