from django.db import models

from django.conf import settings

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("PARTICIPANT", "Participante"),
        ("BUYER", "Comprador / Asistente"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
