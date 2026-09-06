from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, ProjectMember, Task
from app import db

team_bp = Blueprint('team', __name__)

@team_bp.route('/')
@login_required
def index():
    users = User.query.all()
    # Annotate users with task stats
    for user in users:
        tasks = Task.query.filter_by(assigned_to=user.id).all()
        user.total_tasks = len(tasks)
        user.completed_tasks = len([t for t in tasks if t.status == 'Done'])
        user.pending_tasks = len([t for t in tasks if t.status != 'Done'])
        user.completion_rate = int((user.completed_tasks / user.total_tasks * 100)) if user.total_tasks > 0 else 0
    return render_template('team/index.html', users=users)

@team_bp.route('/user/<int:user_id>/role', methods=['POST'])
@login_required
def change_role(user_id):
    if not current_user.is_admin():
        flash('Unauthorized', 'danger')
        return redirect(url_for('team.index'))
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot change your own role.', 'warning')
        return redirect(url_for('team.index'))
        
    new_role = request.form.get('role')
    if new_role in ['Admin', 'Member']:
        user.role = new_role
        db.session.commit()
        flash(f"Role updated for {user.username}.", "success")
        
    return redirect(url_for('team.index'))
