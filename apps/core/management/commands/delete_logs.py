import os
from datetime import datetime, timedelta

import pytz
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """
    Defines a management command to delete log files older than two weeks.
    Retrieves the log file path from settings.
    Checks if the log file exists and if it's older than two weeks.
    Deletes the log file if it meets the criteria.
    Logs messages about file operations and errors.
    """

    help = 'Delete log files older than two weeks'

    def handle(self, *args, **options):
        log_path = settings.LOG_FILE_PATH
        self.stdout.write(f'Log file path: {log_path}')
        if not os.path.exists(log_path):
            self.stdout.write(self.style.WARNING('Log file does not exist.'))
            return

        try:
            current_time = datetime.now(tz=pytz.timezone('Asia/Tehran'))
            self.stdout.write(f'Current time: {current_time}')
            file_modified_time = datetime.fromtimestamp(os.path.getmtime(log_path), tz=pytz.utc)
            self.stdout.write(f'File modified time: {file_modified_time}')
            time_difference = current_time - file_modified_time
            self.stdout.write(f'Time difference: {time_difference}')
            if time_difference.total_seconds() > timedelta(weeks=2).total_seconds():
                os.remove(log_path)
                self.stdout.write(self.style.SUCCESS(f'Deleted log file: {log_path}'))
            else:
                self.stdout.write(self.style.WARNING('Log file is not older than two weeks.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
