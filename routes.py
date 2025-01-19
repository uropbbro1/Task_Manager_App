from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
import secrets

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_task = Task(title=title, description=description, author=current_user)
        db.session.add(new_task)
        db.session.commit()
    tasks = Task.query.filter_by(user_id=current_user.id)
    return render_template('index.html', tasks=tasks)

@app.route('/task/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        flash('You can only complete your tasks!', 'danger')
        return redirect(url_for('index'))
    task.completed = True
    db.session.commit()
    flash('Task has been marked as completed.', 'success')
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        flash('You can only edit your tasks!', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        db.session.commit()
        flash('Task has been updated.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('You are logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
           flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))