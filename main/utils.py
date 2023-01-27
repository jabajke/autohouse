from datetime import timedelta

from django.utils import timezone


class Util:

    @staticmethod
    def default_end_date():
        now = timezone.now()
        return now + timedelta(days=7)
