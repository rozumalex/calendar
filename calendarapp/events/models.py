from django.db import models
from django.utils import timezone

from rest_framework.validators import ValidationError

from accounts.models import User
from locations.models import ConferenceRoom


class Event(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              editable=False)
    event_name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.ForeignKey(ConferenceRoom,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)

    class Meta:
        unique_together = ('owner', 'event_name', 'start',)

    def clean(self, *args, **kwargs):
        if self.end < self.start:
            raise ValidationError({'end': ["The meeting cannot end before it "
                                           "was started."]})
        if self.end - self.start > timezone.timedelta(hours=8):
            raise ValidationError({'end': ["The meeting cannot be longer than "
                                           "8 hours."]})
        super(Event, self).clean(*args, **kwargs)

    def __str__(self):
        return self.event_name


class Meeting(Event):
    meeting_agenda = models.CharField(max_length=255)
    participants = models.ManyToManyField(User,
                                          through='Participant',
                                          blank=True)


class Participant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('meeting', 'participant',)
