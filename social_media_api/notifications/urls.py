from django.urls import path
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/mark-read/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
]
