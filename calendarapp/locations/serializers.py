from rest_framework import serializers

from .models import ConferenceRoom


class ConferenceRoomSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ConferenceRoom
        fields = ('manager_id', 'name', 'address',)
