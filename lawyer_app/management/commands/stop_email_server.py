from django.core.management.base import BaseCommand

from lawfirm_management_system.email_queue import condition, email_queue


class Command(BaseCommand):
    help = "Stop the email worker thread gracefully"

    def handle(self, *args, **kwargs):
        email_queue.put(None)
        with condition:
            condition.notify()
        self.stdout.write(self.style.SUCCESS("Email worker has been stopped."))
