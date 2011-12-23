from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from adserver.models import AdSlot, Advertisement


class Command(BaseCommand):

    def handle(self, *args, **options):

        ads = Advertisement.objects.get(id=1)
        print ads.visitor_set.last_month_visits()