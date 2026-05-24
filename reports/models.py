from django.db import models


class DailyReport(models.Model):
    date = models.DateField(unique=True)
    total_reminders = models.IntegerField(default=0)
    sent_reminders = models.IntegerField(default=0)
    failed_reminders = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
