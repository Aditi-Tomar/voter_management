from django.core.management.base import BaseCommand
from passes.models import TemplePass


class Command(BaseCommand):
    help = 'Cleanup orphaned TemplePass entries'

    def handle(self, *args, **options):
        # Delete TemplePass entries with no associated PassRequest
        orphaned_passes = TemplePass.objects.filter(pass_request__isnull=True)
        count = orphaned_passes.count()
        orphaned_passes.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {count} orphaned TemplePass entries'
            )
        )