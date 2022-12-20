from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create a SuperUser"

    def create_superuser(self):
        User.objects.create_superuser(
            settings.DEV_EMAIL,
            settings.DEV_PASSWORD,
            full_name=settings.DEV_FULL_NAME,
        )

    def handle(self, *args, **options):
        exists = User.objects.filter(email__iexact=settings.DEV_EMAIL.lower()).exists()
        if not exists:
            self.create_superuser()

            self.stdout.write(
                self.style.SUCCESS(
                    f"SuperUser created with \n"
                    f"\tEmail: {settings.DEV_EMAIL}\n"
                    f"\tPassword: {settings.DEV_PASSWORD}",
                ),
            )
