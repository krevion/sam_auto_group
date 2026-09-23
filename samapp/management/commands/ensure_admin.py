from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ensure the default admin accounts exist with the configured credentials.'

    def handle(self, *args, **options):
        User = get_user_model()
        accounts = [
            ('sam@imports', '685425'),
            ('sam', '685425'),
        ]

        for username, password in accounts:
            user, created = User.objects.get_or_create(username=username)
            user.email = username if '@' in username else 'sam@example.com'
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} admin user: {username}"
                )
            )
