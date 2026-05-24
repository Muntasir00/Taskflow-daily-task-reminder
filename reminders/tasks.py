from celery import shared_task
from django.utils import timezone
from .models import Reminder


@shared_task(bind=True, max_retries=3)
def send_reminder_task(self, reminder_id: int):
    try:
        reminder = Reminder.objects.get(id=reminder_id)

        # For practice, print instead of sending real email.
        print(f"Sending reminder to {reminder.email}: {reminder.message}")

        reminder.status = "sent"
        reminder.sent_at = timezone.now()
        reminder.save(update_fields=["status", "sent_at"])

        return {
            "reminder_id": reminder.id,
            "status": "sent",
        }

    except Reminder.DoesNotExist:
        return {
            "reminder_id": reminder_id,
            "status": "not_found",
        }

    except Exception as exc:
        reminder = Reminder.objects.get(id=reminder_id)
        reminder.status = "failed"
        reminder.error_message = str(exc)
        reminder.save(update_fields=["status", "error_message"])

        raise self.retry(exc=exc, countdown=10)
