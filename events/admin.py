from django.contrib import admin
from .models import Event, Show, ShowSeat

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ("event", "start_at", "venue_name", "is_active")
    list_filter = ("event", "is_active")
    search_fields = ("event__title", "venue_name")

@admin.register(ShowSeat)
class ShowSeatAdmin(admin.ModelAdmin):
    list_display = ("show", "seat", "status", "held_until", "held_by")
    list_filter = ("status", "show")
    ordering = ("show", "seat__number")
