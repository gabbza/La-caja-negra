from django.contrib import admin
from .models import Venue, Seat

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("venue", "number")
    list_filter = ("venue",)
    ordering = ("venue", "number")


# Register your models here.
