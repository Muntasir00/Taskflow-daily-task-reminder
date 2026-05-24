from django.urls import path
from .views import ReminderCreateView, ReminderDetailView, ReminderListView

urlpatterns = [
    path("reminders/", ReminderCreateView.as_view()),
    path("reminders/list/", ReminderListView.as_view()),
    path("reminders/<int:pk>/", ReminderDetailView.as_view()),
]
