from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.conf import settings


class TimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            tz = request.user.timezone
        else:
            # TODO: detect anonymous user's timezone automatically
            #  (for ex using ip)
            tz = settings.TIME_ZONE
        timezone.activate(tz)
