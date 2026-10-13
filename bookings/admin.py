from django.contrib import admin

from .models import Booking, EscapeRoom


@admin.register(EscapeRoom)
class EscapeRoomAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "duration_minutes", "price_per_person", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "room", "starts_at", "players", "status")
    list_filter = ("status", "starts_at", "room")
    search_fields = ("customer_name", "customer_email", "room__name")
    date_hierarchy = "starts_at"
    autocomplete_fields = ("room",)
    readonly_fields = ("created_at",)
