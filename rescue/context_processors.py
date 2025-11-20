"""
Context processors for templates
"""

def notification_count(request):
    """Add unread notification count to context for shelters"""
    if request.user.is_authenticated and hasattr(request.user, 'shelter'):
        from .models import Notification
        unread_count = Notification.objects.filter(
            shelter=request.user.shelter,
            is_read=False
        ).count()
        return {'unread_notification_count': unread_count}
    return {'unread_notification_count': 0}

