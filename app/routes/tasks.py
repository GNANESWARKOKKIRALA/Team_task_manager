from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import Task, Project, ProjectMember, User, Comment
from app.utils import log_activity, create_notification
from app import db
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/create/<int:project_id>', methods=['GET', 'POST'])
@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)
    if not current_user.is_admin() and not project.is_member(current_user):
        abort(403)
    members = project.get_members()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        assigned_to = request.form.get('assigned_to', type=int)
        priority = request.form.get('priority', 'Medium')
        due_date_str = request.form.get('due_date', '')
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                pass
        if not title:
            flash('Task title is required.', 'danger')
            return render_template('tasks/create.html', project=project, members=members)
            
        task = Task(
            title=title, description=description,
            project_id=project_id, assigned_to=assigned_to,
            created_by=current_user.id, priority=priority, due_date=due_date
        )
        db.session.add(task)
        db.session.commit()
        
        log_activity('Created Task', 'Task', task.id, f'Created task: {title}')
        if assigned_to and assigned_to != current_user.id:
            create_notification(assigned_to, f"You were assigned to task: {title}", url_for('tasks.view_task', task_id=task.id))
            
        flash('Task created!', 'success')
        return redirect(url_for('projects.view_project', project_id=project_id))
    return render_template('tasks/create.html', project=project, members=members)

@tasks_bp.route('/<int:task_id>/update_status', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    project = Project.query.get(task.project_id)
    if not current_user.is_admin() and task.assigned_to != current_user.id and not project.is_member(current_user):
        abort(403)
    new_status = request.form.get('status')
    if new_status in ['Todo', 'In Progress', 'Review', 'Done']:
        old = task.status
        task.status = new_status
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        log_activity('Status Changed', 'Task', task.id, f'From {old} to {new_status}')
        if task.assigned_to and task.assigned_to != current_user.id:
             create_notification(task.assigned_to, f"Status updated to {new_status} for task: {task.title}", url_for('tasks.view_task', task_id=task.id))
        
        flash('Task status updated.', 'success')
    return redirect(url_for('projects.view_project', project_id=task.project_id))

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not current_user.is_admin():
        abort(403)
    project_id = task.project_id
    title = task.title
    db.session.delete(task)
    db.session.commit()
    
    log_activity('Deleted Task', 'Project', project_id, f'Deleted task: {title}')
    flash('Task deleted.', 'success')
    return redirect(url_for('projects.view_project', project_id=project_id))

@tasks_bp.route('/<int:task_id>', methods=['GET', 'POST'])
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    project = Project.query.get(task.project_id)
    if not current_user.is_admin() and not project.is_member(current_user):
        abort(403)
    members = project.get_members()
    
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if content:
            comment = Comment(content=content, task_id=task.id, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            log_activity('Comment Added', 'Task', task.id)
            if task.assigned_to and task.assigned_to != current_user.id:
                 create_notification(task.assigned_to, f"New comment on task: {task.title}", url_for('tasks.view_task', task_id=task.id))
            flash('Comment added.', 'success')
        return redirect(url_for('tasks.view_task', task_id=task.id))
        
    return render_template('tasks/view.html', task=task, project=project, members=members)
