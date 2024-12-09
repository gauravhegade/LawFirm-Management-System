from django.core.management.base import BaseCommand

from lawfirm_management_system.email_queue import EmailWorker, email_worker


class Command(BaseCommand):
    help = "Restart the email worker thread"

    def handle(self, *args, **kwargs):
        if not email_worker.is_alive():
            email_worker = EmailWorker()
            email_worker.start()
            self.stdout.write(self.style.SUCCESS("Email worker has been restarted."))
        else:
            self.stdout.write(self.style.WARNING("Email worker is already running."))
