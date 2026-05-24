from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Reminder
from .serializers import ReminderSerializer
from .tasks import send_reminder_task


class ReminderCreateView(APIView):
    def post(self, request):
        serializer = ReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reminder = serializer.save()

        delay_seconds = max(
            0, int((reminder.remind_at - timezone.now()).total_seconds())
        )

        task = send_reminder_task.apply_async(
            args=[reminder.id],
            countdown=delay_seconds,
        )

        reminder.celery_task_id = task.id
        reminder.save(update_fields=["celery_task_id"])

        return Response(
            ReminderSerializer(reminder).data, status=status.HTTP_201_CREATED
        )


class ReminderDetailView(APIView):
    def get(self, request, pk):
        reminder = Reminder.objects.get(id=pk)
        return Response(ReminderSerializer(reminder).data)


class ReminderListView(APIView):
    def get(self, request):
        reminders = Reminder.objects.all().order_by("-created_at")
        return Response(ReminderSerializer(reminders, many=True).data)
