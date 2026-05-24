from celery import shared_task
from django.utils import timezone
from reminders.models import Reminder
from .models import DailyReport
from datetime import timedelta

@shared_task
def generate_daily_report():
    today = timezone.localdate()

    total = Reminder.objects.filter(created_at__date=today).count()
    sent = Reminder.objects.filter(created_at__date=today, status="sent").count()
    failed = Reminder.objects.filter(created_at__date=today, status="failed").count()

    report, _ = DailyReport.objects.update_or_create(
        date=today,
        defaults={
            "total_reminders": total,
            "sent_reminders": sent,
            "failed_reminders": failed,
        },
    )

    return {
        "date": str(report.date),
        "total": total,
        "sent": sent,
        "failed": failed,
    }


@shared_task
def cleanup_old_sent_reminders():
    cutoff = timezone.now() - timedelta(days=30)

    deleted_count, _ = Reminder.objects.filter(
        status="sent",
        sent_at__lt=cutoff,
    ).delete()

    return {"deleted_count": deleted_count}
