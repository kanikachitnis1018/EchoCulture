from models import db, login_manager
from models import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Feedback(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    feedback = db.Column(db.String(length=200), nullable = False)
    stars = db.Column(db.Integer(), nullable = False)
    department = db.Column(db.String(length=30), nullable = False)
    postion = db.Column(db.String(length= 80), nullable = False)
    
    def map_to_stars(score):
        if score <= 0.2:
            stars = 1
        elif score <= 0.4:
            stars = 2
        elif score <= 0.6:
            stars = 3
        elif score <= 0.8:
            stars = 4
        else:
            stars = 5
        return stars
        

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(length=20), nullable=False)
    lastname = db.Column(db.String(length=20), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
            