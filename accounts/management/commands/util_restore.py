from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

User = get_user_model()


class Command(BaseCommand):
    help = "Restore local environment and install minimal items"

    def handle(self, *args, **options):
        call_command("reset_db", "--noinput")
        call_command("migrate")
        call_command("create_dev_su")
        self.stdout.write(self.style.SUCCESS("Restore Completed!!!"))
