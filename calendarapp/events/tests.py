from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

import json
import pytz

from events.models import Meeting
from locations.models import ConferenceRoom
from accounts. models import User


class MeetingListCreateAPIViewTestCase(APITestCase):
    url = reverse("events:events_list")

    def setUp(self):
        self.username = "alex"
        self.email = "alex@tango.agency"
        self.password = "ireallywantthatjob"
        self.user = User.objects.create_user(
            self.username,
            self.email,
            self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        tz = pytz.timezone(settings.TIME_ZONE)

        john = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='password',
            timezone='Canada/Central')

        james = User.objects.create_user(
            username='james',
            email='james@example.com',
            password='password',
            timezone='Europe/Berlin')

        anna = User.objects.create_user(
            username='anna',
            email='anna@example.com',
            password='password')

        manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password')

        room = ConferenceRoom.objects.create(
            name='Room 5C',
            address='Berlin',
            manager=manager)

        daily_meeting = Meeting.objects.create(
            owner=john,
            event_name="Daily Meeting",
            meeting_agenda="Discuss new features",
            start=timezone.datetime(2020, 11, 23, 9, tzinfo=tz),
            end=timezone.datetime(2020, 11, 23, 10, tzinfo=tz))

        daily_meeting.participants.add(john, james, self.user)

        base_meet = Meeting.objects.create(
            owner=anna,
            event_name="Base Meeting",
            meeting_agenda="Discuss future",
            start=timezone.datetime(2020, 11, 23, 11, tzinfo=tz),
            end=timezone.datetime(2020, 11, 23, 14, tzinfo=tz),
            location=room)

        base_meet.participants.add(anna, james, self.user)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_meeting(self):
        response = self.client.post(
            self.url,
            {"event_name": "Job Interview",
             "meeting_agenda": "Welcome to Tango",
             "start": "2020-11-19 13:00",
             "end": "2020-11-19 14:00",
             "participant_list": []
             })

        self.assertEqual(201, response.status_code)

    def test_day_filter_meeting(self):
        response = self.client.get(self.url, data={'day': '2020-11-23'})
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_location_filter_meeting(self):
        response = self.client.get(
            self.url,
            data={'location_id': ConferenceRoom.objects.get(
                address='Berlin').id})
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_search_meeting(self):
        response = self.client.get(self.url, data={'query': 'dail'})
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_user_meetings(self):
        user = self.user
        tz = pytz.timezone(user.timezone)
        meeting = Meeting.objects.create(
            owner=user,
            event_name="New Year's Eve",
            meeting_agenda="Celebrating",
            start=timezone.datetime(2020, 12, 31, 21, tzinfo=tz),
            end=timezone.datetime(2021, 1, 1, 3, tzinfo=tz))
        meeting.participants.add(user)
        response = self.client.get(self.url)
        self.assertEqual(len(json.loads(response.content)),
                         Meeting.objects.count())
