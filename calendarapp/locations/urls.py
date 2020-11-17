from django.urls import path

from .apiviews import ConferenceRoomListView


app_name = 'locations'

urlpatterns = [
    path('location/', ConferenceRoomListView.as_view(), name='location_list'),
]
