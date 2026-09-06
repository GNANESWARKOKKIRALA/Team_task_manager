from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Task, Project

my_tasks_bp = Blueprint('my_tasks', __name__)

@my_tasks_bp.route('/')
@login_required
def index():
    status_filter = request.args.get('status', 'All')
    priority_filter = request.args.get('priority', 'All')
    sort_by = request.args.get('sort', 'Newest')
    
    query = Task.query.filter_by(assigned_to=current_user.id)
    
    if status_filter != 'All':
        if status_filter == 'Overdue':
            # SQLite datetime comparison is tricky, but we'll do it in Python for simplicity here
            # or handle it in Jinja, but let's filter what we can in DB
            pass # Handle overdue below
        else:
            query = query.filter_by(status=status_filter)
            
    if priority_filter != 'All':
        query = query.filter_by(priority=priority_filter)
        
    if sort_by == 'Oldest':
        query = query.order_by(Task.created_at.asc())
    elif sort_by == 'Due Date':
        query = query.order_by(Task.due_date.asc()) # nulls might sort first depending on DB
    else:
        query = query.order_by(Task.created_at.desc())
        
    tasks = query.all()
    
    if status_filter == 'Overdue':
        tasks = [t for t in tasks if t.is_overdue()]
        
    return render_template('my_tasks/index.html', tasks=tasks, 
                           status_filter=status_filter, priority_filter=priority_filter, sort_by=sort_by)
