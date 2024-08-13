from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import CustomUser

class Command(BaseCommand):
    help = 'Update commission1 with commission2 value and reset commission2 to 0.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        users = CustomUser.objects.all()
        for user in users:
            user.commission1 = user.commission2
            user.commission2 = 0
            user.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully updated commissions for {users.count()} users.'))


# python manage.py update_commissions
