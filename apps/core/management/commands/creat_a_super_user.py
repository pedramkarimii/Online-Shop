from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Management command to create a superuser with specified credentials.
    """
    help = 'Creates a superuser with specified credentials'

    def add_arguments(self, parser):
        """
        Adds arguments to the command parser to accept username, email, phone number, and password.
        """
        parser.add_argument('--username', type=str, help='Specifies the username for the superuser', required=True)
        parser.add_argument('--email', type=str, help='Specifies the email address for the superuser', required=True)
        parser.add_argument('--phone_number', type=str, help='Specifies the phone number for the superuser',
                            required=True)
        parser.add_argument('--password', type=str, help='Specifies the password for the superuser', required=True)

    def handle(self, *args, **options):
        """
        Handles the command execution.
        Creates a superuser if one does not already exist with the provided username.
        """
        User = get_user_model()
        phone_number = '09128355747'
        username = 'pedramkarimi'
        email = 'pedram.9060@gmail.com'
        password = 'qwertyQ@1'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password, phone_number=phone_number)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
