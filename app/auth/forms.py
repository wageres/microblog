from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
class LoginForm(FlaskForm):
	username = StringField('username',validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])
	remember_me = BooleanField('remember_me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('username',validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('password',validators=[DataRequired()])
	password2 = PasswordField('Repeat Password',
		validators=[DataRequired(),EqualTo('password'),])
	submit = SubmitField('Register')

	#Если вначале идёт validate_ то WTForm добавляет функции к стандартной валидации
	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self,email):
			user = User.query.filter_by(email=email.data).first()
			if user is not None:
				raise ValidationError('Please use a different email.')

class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')	

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Request Password Reset')