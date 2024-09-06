from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Leader(db.Model, UserMixin):
    __tablename__ = 'leaders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    projects = db.relationship('Project', back_populates='leader', lazy='dynamic')
    collaborators = db.relationship('Collaborator', back_populates='leader', lazy='dynamic')
    contents = db.relationship('Content', back_populates='leader', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password,method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    leader_id = db.Column(db.Integer, db.ForeignKey('leaders.id'))
    leader = db.relationship('Leader', back_populates='projects')

class Collaborator(db.Model):
    __tablename__ = 'collaborators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))
    leader_id = db.Column(db.Integer, db.ForeignKey('leaders.id'))
    leader = db.relationship('Leader', back_populates='collaborators')

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'free' or 'paid'
    url = db.Column(db.String(200))
    leader_id = db.Column(db.Integer, db.ForeignKey('leaders.id'))
    leader = db.relationship('Leader', back_populates='contents')
