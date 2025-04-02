from django.core.management.base import BaseCommand
from django.db import connection
from import_data import import_excel_data


class Command(BaseCommand):
    help = 'Import voters data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            # Verify database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            # Import data
            count = import_excel_data(file_path)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {count} voters')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing voters: {str(e)}')
            )