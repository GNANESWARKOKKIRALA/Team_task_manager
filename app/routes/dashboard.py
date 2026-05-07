from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Task, Project, ProjectMember
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    if current_user.is_admin():
        projects = Project.query.all()
        all_tasks = Task.query.all()
    else:
        member_project_ids = [pm.project_id for pm in ProjectMember.query.filter_by(user_id=current_user.id).all()]
        projects = Project.query.filter(Project.id.in_(member_project_ids)).all()
        all_tasks = Task.query.filter_by(assigned_to=current_user.id).all()

    total_tasks = len(all_tasks)
    done_tasks = sum(1 for t in all_tasks if t.status == 'Done')
    in_progress = sum(1 for t in all_tasks if t.status == 'In Progress')
    overdue_tasks = [t for t in all_tasks if t.is_overdue()]

    return render_template('dashboard/index.html',
        projects=projects,
        total_tasks=total_tasks,
        done_tasks=done_tasks,
        in_progress=in_progress,
        overdue_tasks=overdue_tasks,
        now=datetime.utcnow()
    )
