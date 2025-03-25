from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Notification

class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch notifications for the logged-in user
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

        # Serialize notifications
        notification_data = [
            {
                "id": notification.id,
                "actor": notification.actor.username,
                "verb": notification.verb,
                "target": str(notification.target),
                "timestamp": notification.timestamp,
                "is_read": notification.is_read
            }
            for notification in notifications
        ]

        return Response({"notifications": notification_data}, status=status.HTTP_200_OK)


class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            # Fetch the notification object
            notification = Notification.objects.get(id=pk, recipient=request.user)
        except Notification.DoesNotExist:
            raise NotFound("Notification not found.")

        # Mark the notification as read
        notification.is_read = True
        notification.save()

        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
