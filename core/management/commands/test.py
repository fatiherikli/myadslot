from pprint import pprint
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models.aggregates import Count
from adserver.models import AdSlot, Advertisement, Visitor
from adserver.utils import build_statistic_data, stats_browser


class Command(BaseCommand):

    def handle(self, *args, **options):

        print stats_browser(user_id=1)