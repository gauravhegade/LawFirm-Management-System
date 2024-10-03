from django.core.management.base import BaseCommand
from my_app.email_queue import email_queue, condition

class Command(BaseCommand):
    help = 'Stop the email worker thread gracefully'

    def handle(self, *args, **kwargs):
        email_queue.put(None)
        with condition:
            condition.notify() 
        self.stdout.write(self.style.SUCCESS('Email worker has been stopped.'))