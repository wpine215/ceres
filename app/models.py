from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	fridges = db.relationship('Fridge', backref='owner', lazy='dynamic')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Fridge(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	item = db.Column(db.String(64))
	quantity = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	expiration = db.Column(db.DateTime, index=True)

class Reference(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	item = db.Column(db.String(64), index=True, unique=True)
	optimal = db.Column(db.String(32), index=False)
	freezer = db.Column(db.Integer)
	fridge = db.Column(db.Integer)
	roomtemp = db.Column(db.Integer)
	
@login.user_loader
def load_user(id):
    return User.query.get(int(id))