from django.db import models
from django.conf import settings
from django.utils import timezone
from venues.models import Seat


class Event(models.Model):
    title = models.CharField("Título", max_length=120)
    description = models.TextField("Descripcion", blank=True)
    is_active = models.BooleanField("Activo", default=True)
    
    def __str__(self):
        return self.title
    

class Show(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="shows")
    start_at = models.DateTimeField("Fecha y hora")
    venue_name = models.CharField("Foro", max_length=120, default="La Caja Negra")
    is_active = models.BooleanField("Activo", default=True)

    def __str__(self):
        return f"{self.event.title} - {self.start_at:%Y-%m-%d %H:%M}"

class ShowSeat(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Disponible"
        HELD = "HELD", "Apartado"
        SOLD = "SOLD", "Vendido"

    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name="show_seats"
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name="show_seats"
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    held_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    held_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("show", "seat")
        ordering = ["seat__number"]

    def __str__(self):
        return f"{self.show} | Asiento {self.seat.number} ({self.status})"

    def is_hold_expired(self):
        return (
            self.status == self.Status.HELD
            and self.held_until
            and self.held_until <= timezone.now()
        )


# Create your models here.
