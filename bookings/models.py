from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class EscapeRoom(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Nazwa")
    slug = models.SlugField(max_length=140, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Opis")
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Maksymalna liczba graczy",
    )
    duration_minutes = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Czas gry (minuty)",
    )
    price_per_person = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Cena za osobę (PLN)",
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktywny")

    class Meta:
        ordering = ["name"]
        verbose_name = "Pokój zagadek"
        verbose_name_plural = "Pokoje zagadek"

    def __str__(self):
        return self.name


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Oczekująca"
        CONFIRMED = "confirmed", "Potwierdzona"
        CANCELLED = "cancelled", "Anulowana"

    room = models.ForeignKey(
        EscapeRoom,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Pokój zagadek",
    )
    customer_name = models.CharField(max_length=150, verbose_name="Imię i nazwisko")
    customer_email = models.EmailField(verbose_name="Adres e-mail")
    starts_at = models.DateTimeField(verbose_name="Termin rezerwacji")
    players = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Liczba graczy",
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    class Meta:
        ordering = ["starts_at"]
        verbose_name = "Rezerwacja"
        verbose_name_plural = "Rezerwacje"

    def clean(self):
        super().clean()
        if self.room_id and self.players > self.room.capacity:
            raise ValidationError(
                {"players": "Liczba graczy nie może przekraczać pojemności pokoju."}
            )

    def __str__(self):
        return f"{self.customer_name} — {self.room} ({self.starts_at:%Y-%m-%d %H:%M})"
