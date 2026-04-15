from complaints.models import Notification


def notifications_context(request):
    """Add unread notification count to all template contexts."""
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
        return {'unread_notifications': unread_notifications}
    return {'unread_notifications': 0}
