from datetime import timedelta
from decimal import Decimal

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .admin import BookingAdmin, EscapeRoomAdmin
from .models import Booking, EscapeRoom


class BookingModelTests(TestCase):
    def setUp(self):
        self.room = EscapeRoom.objects.create(
            name="Skarbiec",
            slug="skarbiec",
            description="Pokój testowy",
            capacity=5,
            duration_minutes=60,
            price_per_person=Decimal("80.00"),
        )

    def test_booking_rejects_more_players_than_room_capacity(self):
        booking = Booking(
            room=self.room,
            customer_name="Jan Kowalski",
            customer_email="jan@example.com",
            starts_at=timezone.now() + timedelta(days=1),
            players=6,
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_models_are_registered_in_admin(self):
        self.assertIsInstance(admin.site._registry[EscapeRoom], EscapeRoomAdmin)
        self.assertIsInstance(admin.site._registry[Booking], BookingAdmin)
