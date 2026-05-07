from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models import Project, ProjectMember, User, Task
from app import db

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/')
@login_required
def list_projects():
    if current_user.is_admin():
        projects = Project.query.all()
    else:
        member_ids = [pm.project_id for pm in ProjectMember.query.filter_by(user_id=current_user.id).all()]
        projects = Project.query.filter(Project.id.in_(member_ids)).all()
    return render_template('projects/list.html', projects=projects)

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if not current_user.is_admin():
        flash('Only Admins can create projects.', 'danger')
        return redirect(url_for('projects.list_projects'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            flash('Project name is required.', 'danger')
            return render_template('projects/create.html')
        project = Project(name=name, description=description, owner_id=current_user.id)
        db.session.add(project)
        db.session.flush()
        pm = ProjectMember(project_id=project.id, user_id=current_user.id)
        db.session.add(pm)
        db.session.commit()
        flash('Project created!', 'success')
        return redirect(url_for('projects.view_project', project_id=project.id))
    return render_template('projects/create.html')

@projects_bp.route('/<int:project_id>')
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    if not current_user.is_admin() and not project.is_member(current_user):
        abort(403)
    members = project.get_members()
    tasks = Task.query.filter_by(project_id=project_id).all()
    all_users = User.query.all() if current_user.is_admin() else []
    return render_template('projects/view.html', project=project, members=members, tasks=tasks, all_users=all_users)

@projects_bp.route('/<int:project_id>/add_member', methods=['POST'])
@login_required
def add_member(project_id):
    if not current_user.is_admin():
        flash('Only Admins can add members.', 'danger')
        return redirect(url_for('projects.view_project', project_id=project_id))
    project = Project.query.get_or_404(project_id)
    user_id = request.form.get('user_id', type=int)
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
    elif project.is_member(user):
        flash('User is already a member.', 'warning')
    else:
        pm = ProjectMember(project_id=project_id, user_id=user_id)
        db.session.add(pm)
        db.session.commit()
        flash(f'{user.username} added to project.', 'success')
    return redirect(url_for('projects.view_project', project_id=project_id))

@projects_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    if not current_user.is_admin():
        abort(403)
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'success')
    return redirect(url_for('projects.list_projects'))
