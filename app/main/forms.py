from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User
from flask import request


class EditProfileForm(FlaskForm):
	username = StringField('Имя', validators=[DataRequired()])
	about_me = TextAreaField('Обо мне',validators=[Length(min=0,max=140)])
	submit = SubmitField('Подтвердить')

	def __init__(self,original_username,*args,**kwargs):
		super(EditProfileForm,self).__init__(*args,**kwargs)
		self.original_username = original_username

	def validate_username(self,username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError('Пожалуйста введите другое имя!')


class PostForm(FlaskForm):
	post = TextAreaField('Напишите что-нибудь',validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField('Отправить')

class SearchForm(FlaskForm):
	q = StringField('Поиск', validators=[DataRequired()])

	def __init__(self,*args,**kwargs):
		if "formdata" not in kwargs:
			kwargs['formdata'] = request.args#определяет, откуда Flask-WTF получает формы
		if 'csrf_enabled' not in kwargs:
			kwargs['csrf_enabled'] = False#CSRF - защита
		super(SearchForm, self).__init__(*args, **kwargs)

