from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Leader, Collaborator, Project, Content
from database import db, init_db
import os
import logging

logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')

    init_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return Leader.query.get(int(user_id))

    @app.route('/')
    def index():
        leaders = Leader.query.limit(6).all()
        return render_template('index.html', leaders=leaders)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/leaders')
    def all_leaders():
        leaders = Leader.query.all()
        return render_template('leaders.html', leaders=leaders)

    @app.route('/profile/<int:leader_id>')
    def profile(leader_id):
        leader = Leader.query.filter(Leader.id == leader_id).first()
        if leader is None:
            abort(404)
        return render_template('profile.html', leader=leader)

    @app.route('/search')
    def search():
        query = request.args.get('q', '')
        leaders = Leader.query.filter(
            (Leader.name.ilike(f'%{query}%')) | (Leader.company.ilike(f'%{query}%'))
        ).all()
        return jsonify([{'id': l.id, 'name': l.name, 'company': l.company} for l in leaders])

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            try:
                name = request.form['name']
                company = request.form['company']
                email = request.form['email']
                password = request.form['password']

                if Leader.query.filter_by(email=email).first():
                    flash('Email already registered')
                    return redirect(url_for('register'))

                new_leader = Leader(name=name, company=company, email=email)
                new_leader.set_password(password)
                db.session.add(new_leader)
                db.session.commit()

                flash('Registration successful. Please log in.')
                return redirect(url_for('login'))
            except Exception as e:
                app.logger.error(f'Registration error: {str(e)}')
                db.session.rollback()
                return render_template('500.html'), 500

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            leader = Leader.query.filter_by(email=email).first()

            if leader and leader.check_password(password):
                login_user(leader)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/edit_profile', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        if request.method == 'POST':
            current_user.name = request.form['name']
            current_user.company = request.form['company']
            current_user.bio = request.form['bio']

            # Handle collaborators
            collaborator_names = [name.strip() for name in request.form['collaborators'].split(',') if name.strip()]
            current_user.collaborators = []
            for name in collaborator_names:
                collaborator = Collaborator.query.filter_by(name=name).first()
                if not collaborator:
                    collaborator = Collaborator(name=name)
                current_user.collaborators.append(collaborator)

            # Handle projects
            project_names = [name.strip() for name in request.form['projects'].split(',') if name.strip()]
            current_user.projects = []
            for name in project_names:
                project = Project.query.filter_by(name=name, leader=current_user).first()
                if not project:
                    project = Project(name=name, leader=current_user)
                current_user.projects.append(project)

            # Handle contents
            content_titles = [title.strip() for title in request.form['contents'].split(',') if title.strip()]
            current_user.contents = []
            for title in content_titles:
                content = Content.query.filter_by(title=title, leader=current_user).first()
                if not content:
                    content = Content(title=title, leader=current_user, type='unknown')
                current_user.contents.append(content)

            db.session.commit()
            flash('Profile updated successfully')
            return redirect(url_for('dashboard'))

        return render_template('edit_profile.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)