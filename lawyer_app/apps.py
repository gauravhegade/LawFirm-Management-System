from django.apps import AppConfig

# import os


class LawyerAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lawyer_app"

    def ready(self):
        import signal

        from .email_queue import EmailWorker, condition, email_queue, email_worker

        if not email_worker or not email_worker.is_alive():
            email_worker = EmailWorker()
            email_worker.start()

        def stop_worker(signum, frame):
            print("Received signal to stop worker...")
            email_queue.put(None)
            with condition:
                condition.notify()

            # if signum == signal.SIGINT:
            #     os.kill(os.getpid(), signal.SIGINT)

        signal.signal(signal.SIGTERM, stop_worker)
        # signal.signal(signal.SIGINT, stop_worker)
