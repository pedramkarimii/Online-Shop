from decouple import config # noqa
from time import sleep
from redis import Redis
from redis.exceptions import ConnectionError, BusyLoadingError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Django command to pause execution until Redis is available.
    This command is useful in scenarios where Redis is a critical service
    and the application needs to ensure Redis is up before proceeding.
    """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for redis ...')

        if not config("DEBUG"):
            redis_connection = Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'))

            while True:
                try:
                    redis_connection.client_list()
                except (ConnectionError, BusyLoadingError):
                    self.stdout.write('Redis unavailable, Retrying ...')
                    sleep(1)
                else:
                    break

            self.stdout.write(self.style.SUCCESS('Redis available'))
        else:
            self.stdout.write(self.style.MIGRATE_HEADING('Redis availability passed because debug mode is True'))
