from django.db import models

from accounts.models import User


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'address',)

    def __str__(self):
        return self.name


class ConferenceRoom(Location):
    manager = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
