from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Seat(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="seats")
    number = models.PositiveIntegerField()  # 1..120

    class Meta:
        unique_together = ("venue", "number")
        ordering = ["number"]

    def __str__(self):
        return f"{self.venue.name} - Asiento {self.number}"


# Create your models here.
