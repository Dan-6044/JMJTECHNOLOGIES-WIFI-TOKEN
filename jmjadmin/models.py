from django.db import models

class Station(models.Model):
    STATION_TYPES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    station_id = models.CharField(max_length=20, unique=True)
    station_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    station_type = models.CharField(max_length=10, choices=STATION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.station_name} ({self.station_id})"
