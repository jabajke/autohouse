from datetime import timedelta

from django.utils import timezone


class Util:

    @staticmethod
    def default_end_date():
        now = timezone.now()
        return now + timedelta(days=7)

    @staticmethod
    def current_year():
        now = timezone.now()
        return now.year
