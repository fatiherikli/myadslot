from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from adserver.models import AdSlot, Advertisement


class Command(BaseCommand):

    def handle(self, *args, **options):

        fatih = User.objects.get(username="fatih")

        slot = AdSlot(user=fatih, title="slot", slot="test", sizes="300x250")
        slot.save()

        ads = Advertisement(adslot=slot, title="test", user=fatih)
        ads.save()
        print ads.start_date