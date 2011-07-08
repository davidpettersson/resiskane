from django.core.management.base import BaseCommand, CommandError
from resiskane.skotte.models import Station
from time import time

class Command(BaseCommand):
    args = 'None'
    help = 'Refreshes all stations in the database'

    def _clearDatabase(self):
        pass

    def _populateDatabase(self):
        pass

    def handle(self, *args, **options):
        try:
            mark = time()
            self._clearDatabase()
            delta_clear = time() - mark
            mark = time()
            self._populateDatabase()
            delta_populate = time() - mark
            self.stdout.write('OK (clear=%.2fs, populate=%.2fs)\n' % (delta_clear, delta_populate))
        except Exception as e:
            raise CommandError('Failed to refresh station database: ' + str(e))

