import threading
import queue
from django.core.mail import send_mail
import os

email_queue = queue.Queue()
condition = threading.Condition()

class EmailWorker(threading.Thread):
    def __init__(self):
    
        threading.Thread.__init__(self)
        self.daemon = True  
        self.thread_data()

    def thread_data(self):
        print(f"Thread ID: {threading.get_ident()}, Process ID: {os.getpid()}")

    def run(self):
        while True:
            with condition:
                
                while email_queue.empty():
                    print("Queue is empty, worker is going to sleep...")
                    condition.wait()  

                email_task = email_queue.get()

            if email_task is None:
                break  

            try:
                self.thread_data()
                subject, plain_message, from_email, recipient_list, html_message = email_task

                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False,
                    html_message=html_message
                )
                print(f"Email sent to: {recipient_list}")
            except Exception as e:
                print(f"Error sending email: {e}")
            finally:
                email_queue.task_done()  

email_worker = EmailWorker()

