"""
Context processors for templates
"""

def notification_count(request):
    """Add unread notification count to context for shelters"""
    if request.user.is_authenticated and hasattr(request.user, 'shelter'):
        try:
            from .models import Notification
            unread_count = Notification.objects.filter(
                shelter=request.user.shelter,
                is_read=False
            ).count()
            return {'unread_notification_count': unread_count}
        except Exception as e:
            # If database tables don't exist yet, return 0
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error in notification_count: {e}")
            pass
    return {'unread_notification_count': 0}

