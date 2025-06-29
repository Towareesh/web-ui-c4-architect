from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # def generate_token(self):
    #     payload = {
    #         'exp': datetime.datetime.now() + datetime.timedelta(days=1),
    #         'iat': datetime.datetime.now(),
    #         'sub': str(self.id)
    #     }
    #     return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')