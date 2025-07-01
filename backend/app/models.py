from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Text

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    
    # Связи
    projects = db.relationship('Project', backref='owner', lazy=True)
    requirements = db.relationship('Requirement', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    entities = db.Column(db.JSON, nullable=True)
    # Заменяем JSONB на JSON
    relationships = db.Column(db.JSON, nullable=True)
    
    # Внешние ключи
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirement.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Requirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entities = db.Column(db.JSON, nullable=True)
    # Заменяем JSONB на JSON
    relationships = db.Column(db.JSON, nullable=True)
    
    # Внешние ключи
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    # def generate_token(self):
    #     payload = {
    #         'exp': datetime.datetime.now() + datetime.timedelta(days=1),
    #         'iat': datetime.datetime.now(),
    #         'sub': str(self.id)
    #     }
    #     return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')