from django.core.management.base import BaseCommand, CommandError
from time import time
from resiskane.skotte.models import Station
from resiskane.skotte.stations import populate_by_qs

class Command(BaseCommand):
    args = 'None'
    help = 'Refreshes all stations in the database'

    def _clearDatabase(self):
        Station.objects.all().delete()

    def _populateDatabase(self):
        f = open('skotte/data/station-names', 'rt')
        names = map(lambda s: s.strip().decode('utf-8'), f.readlines())
        f.close()

        for name in names:
            populate_by_qs(name)

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

