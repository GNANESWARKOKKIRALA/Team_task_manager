from app import db
from app.models import Notification, ActivityLog
from flask_login import current_user

def create_notification(user_id, message, link=None):
    """Create a new notification for a user."""
    if not user_id:
        return
    notification = Notification(user_id=user_id, message=message, link=link)
    db.session.add(notification)
    db.session.commit()

def log_activity(action, entity_type, entity_id, description=None):
    """Log an activity performed by the current user."""
    user_id = current_user.id if current_user and current_user.is_authenticated else None
    log = ActivityLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description
    )
    db.session.add(log)
    db.session.commit()
