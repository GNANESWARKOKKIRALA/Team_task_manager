from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Task, Project, ProjectMember, ActivityLog
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    if current_user.is_admin():
        projects = Project.query.all()
        all_tasks = Task.query.all()
        activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(15).all()
    else:
        member_project_ids = [pm.project_id for pm in ProjectMember.query.filter_by(user_id=current_user.id).all()]
        projects = Project.query.filter(Project.id.in_(member_project_ids)).all()
        all_tasks = Task.query.filter_by(assigned_to=current_user.id).all()
        activities = ActivityLog.query.filter_by(user_id=current_user.id).order_by(ActivityLog.created_at.desc()).limit(15).all()

    total_tasks = len(all_tasks)
    done_tasks = sum(1 for t in all_tasks if t.status == 'Done')
    in_progress = sum(1 for t in all_tasks if t.status == 'In Progress')
    todo_tasks = sum(1 for t in all_tasks if t.status == 'Todo')
    review_tasks = sum(1 for t in all_tasks if t.status == 'Review')
    
    overdue_tasks = [t for t in all_tasks if t.is_overdue()]
    upcoming_deadlines = [t for t in all_tasks if t.due_date and not t.is_overdue() and t.status != 'Done' and (t.due_date - datetime.utcnow()).days <= 7]
    upcoming_deadlines.sort(key=lambda x: x.due_date)

    completion_rate = int((done_tasks / total_tasks * 100)) if total_tasks > 0 else 0

    # Data for charts
    status_chart_data = [todo_tasks, in_progress, review_tasks, done_tasks]
    priority_chart_data = {
        'Low': sum(1 for t in all_tasks if t.priority == 'Low'),
        'Medium': sum(1 for t in all_tasks if t.priority == 'Medium'),
        'High': sum(1 for t in all_tasks if t.priority == 'High'),
        'Critical': sum(1 for t in all_tasks if t.priority == 'Critical')
    }

    return render_template('dashboard/index.html',
        projects=projects[:5], # Recent projects
        total_projects=len(projects),
        active_projects=sum(1 for p in projects if p.status == 'Active'),
        total_tasks=total_tasks,
        done_tasks=done_tasks,
        in_progress=in_progress,
        todo_tasks=todo_tasks,
        overdue_tasks=overdue_tasks,
        completion_rate=completion_rate,
        upcoming_deadlines=upcoming_deadlines,
        activities=activities,
        status_chart_data=status_chart_data,
        priority_chart_data=priority_chart_data,
        now=datetime.utcnow()
    )
