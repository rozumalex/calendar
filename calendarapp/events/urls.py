from django.urls import path

from .apiviews import MeetingListView


app_name = 'events'

urlpatterns = [
    path('meeting/', MeetingListView.as_view(), name='events_list'),
]
