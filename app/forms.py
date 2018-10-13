from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

choices = [{'dairy','Dairy'},
		   {'fruit','Fruit'},
		   {'vegetable', 'Vegetable'},
		   {'meat', 'Meat'},
	       {'grains', 'Grains'},
		   {'seafood', 'Seafood'},
		   {'beverage', 'Beverage'}]

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please select a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different e-mail.')

class ItemForm(FlaskForm):
	type = SelectField('Type', choices=choices)
	item = SelectField('Item', choices=choices)
	quant = IntegerField('Quantity', validators=[DataRequired()])
	# Add date picker here??
	submit = SubmitField('Add item')
