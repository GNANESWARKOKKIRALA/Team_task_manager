from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Task, User
from app import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        # username change could also be added, but keeping it simple
        current_user.email = email
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile.index'))
        
    tasks = Task.query.filter_by(assigned_to=current_user.id).all()
    total = len(tasks)
    completed = len([t for t in tasks if t.status == 'Done'])
    pending = total - completed
    overdue = len([t for t in tasks if t.is_overdue()])
    rate = int((completed / total) * 100) if total > 0 else 0
    
    return render_template('profile/index.html', 
        total_tasks=total, completed=completed, pending=pending, 
        overdue=overdue, completion_rate=rate)
