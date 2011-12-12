from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


def profile(username, email):
    u, c = User.objects.get_or_create(username = username, email = email, is_active=True, is_staff=True)
    u.set_password('123456')
    u.save()
    return u


class Command(BaseCommand):

    def handle(self, *args, **options):

        call_command('syncdb', interactive=False)

        fatih = profile('fatih', 'fatih1@live.com')
        fatih.is_superuser = True
        fatih.save()



