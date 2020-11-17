from rest_framework import generics

from .models import ConferenceRoom
from .serializers import ConferenceRoomSerializer


class ConferenceRoomListView(generics.ListCreateAPIView):
    serializer_class = ConferenceRoomSerializer
    queryset = ConferenceRoom.objects.all()
