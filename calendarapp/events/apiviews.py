from django.db.models import Q
from django.utils import timezone
from rest_framework import generics

from functools import reduce

from .models import Meeting
from .serializers import MeetingWriteSerializer, MeetingReadSerializer, \
    MeetingSerializer


class MeetingListView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    # read_serializer_class = MeetingReadSerializer
    # write_serializer_class = MeetingWriteSerializer
    queryset = Meeting.objects.all()

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return self.read_serializer_class
    #     else:
    #         return self.write_serializer_class

    def get_queryset(self):
        user = self.request.user
        day = self.request.query_params.get('day', None)
        location_id = self.request.query_params.get('location_id', None)
        query = self.request.query_params.get('query', None)

        participant_set = user.participant_set.all()

        queryset = Meeting.objects.filter(Q(participant__in=participant_set) |
                                          Q(location__manager=user),
                                          Q(start__gte=timezone.now())
                                          ).distinct()

        if day:
            queryset = queryset.filter(start__date=day)

        if location_id:
            queryset = queryset.filter(location__id=location_id)

        if query:
            query = query.split(' ')
            queryset = queryset.filter(
                reduce(lambda x, y: x | y,
                       [Q(event_name__icontains=word) |
                        Q(meeting_agenda__icontains=word) for word in query]))

        return queryset
