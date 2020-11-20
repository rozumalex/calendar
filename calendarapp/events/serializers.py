from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import ValidationError

import uuid

from .models import Meeting, Participant
from locations.models import ConferenceRoom
from locations.serializers import ConferenceRoomSerializer
from accounts.models import User


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, value):
        return value.email


class MeetingSerializer(serializers.ModelSerializer):
    owner_id = serializers.UUIDField()
    start = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    participant_list = serializers.SlugRelatedField(many=True,
                                                    source='participants',
                                                    slug_field='email',
                                                    queryset=User.objects.all())

    class Meta:
        model = Meeting
        fields = ('owner_id',
                  'event_name',
                  'meeting_agenda',
                  'start',
                  'end',
                  'participant_list',
                  'location',)


class MeetingReadSerializer(MeetingSerializer):
    location = ConferenceRoomSerializer(read_only=True)
    participant_list = ParticipantSerializer(many=True,
                                             read_only=True,
                                             source='participants')


class MeetingWriteSerializer(MeetingSerializer):
    location = serializers.IntegerField(required=False,
                                        allow_null=True,
                                        write_only=True)
    participant_list = serializers.ListField(required=True,
                                             write_only=True)

    def validate_location(self, location=None):
        if location:
            if not isinstance(location, int):
                raise ValidationError("Invalid location data type. Need int.")
            if not ConferenceRoom.objects.filter(id=location).exists():
                raise ValidationError("No such conference room.")
            return location

    def validate_participant_list(self, participant_list=list()):
        if not isinstance(participant_list, list):
            raise ValidationError("Invalid participant_list data type. "
                                  "Need list.")
        for email in participant_list:
            if not User.objects.filter(email=email).exists():
                raise ValidationError(f"No user with email {email} exists.")

    def validate(self, data):
        if 'participant_list' in data:
            data.pop('participant_list')
        instance = Meeting(**data)
        instance.clean()
        return data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user

        participant_list_data = []
        if 'participant_list' in validated_data:
            participant_list_data = validated_data.pop('participant_list')

        location_data = None
        if 'location' in validated_data:
            location_data = validated_data.pop('location')

        meeting = Meeting(**validated_data)
        meeting.owner_id = self.context['request'].user.id

        if location_data:
            meeting.location = ConferenceRoom.objects.get(id=location_data)
        meeting.save()

        if participant_list_data:
            for email in participant_list_data:
                participant = User.objects.get(email=email)
                meeting.participants.add(participant)

        if user not in meeting.participants.all():
            meeting.participants.add(user)

        return meeting

    def to_representation(self, instance):
        # TODO: Refactor representation in more simple way
        representation = super().to_representation(instance)

        participant_list = []
        for user in instance.participants.all():
            participant_list.append(user.email)
        representation['participant_list'] = participant_list

        if instance.location:
            location = dict()
            location['manager_id'] = instance.location.manager_id
            location['name'] = instance.location.name
            location['address'] = instance.location.address
            representation['location'] = location
        else:
            representation['location'] = None

        return representation
