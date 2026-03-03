from django.core.management.base import BaseCommand
from queue1.worker import run_worker


class Command(BaseCommand):
    help = "Run background job worker"

    def handle(self, *args, **options):
        run_worker()