from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.conf import settings


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            tz = request.user.timezone
        else:
            tz = settings.TIME_ZONE
        timezone.activate(tz)
