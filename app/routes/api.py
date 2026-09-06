from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Task, Notification
from app.utils import log_activity
from app import db
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks/<int:task_id>/status', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status in ['Todo', 'In Progress', 'Review', 'Done']:
        old_status = task.status
        task.status = new_status
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        log_activity('Status Changed', 'Task', task.id, f'Changed status from {old_status} to {new_status}')
        return jsonify({'success': True, 'message': 'Status updated'})
    return jsonify({'success': False, 'message': 'Invalid status'}), 400

@api_bp.route('/notifications/read', methods=['POST'])
@login_required
def mark_notifications_read():
    unread = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    for n in unread:
        n.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/notifications/read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    n = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first()
    if n:
        n.is_read = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404
