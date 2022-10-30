# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
# from application.models import User
#
# class LoginForm(FlaskForm):
# 	email = StringField("Email", validators=[DataRequired(), Email()])
# 	password = StringField("Password", validators=[DataRequired()])
# 	remember_me = BooleanField("Remember Me")
# 	submit = SubmitField("Login")
#
# class Registration(FlaskForm):
# 	email = StringField("Email", validators=[DataRequired()])
# 	password = PasswordField("Password", validators=[DataRequired()])
# 	# password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
# 	first_name = StringField("First Name", validators=[DataRequired()])
# 	last_name = StringField("Last Name", validators=[DataRequired()])
# 	submit = SubmitField("Register")
#
# 	def validate_email(self, email):
# 		user = User.objects(email=email.data).first()
# 		if user:
# 			raise ValidationError("Email is already in use. Pick another one.")


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User


class LoginForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
	submit = SubmitField("Login")


class Registration(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
	first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=55)])
	last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=55)])
	submit = SubmitField("Register Now")

	def validate_email(self, email):
		user = User.objects(email=email.data).first()
		if user:
			raise ValidationError("Email is already in use. Pick another one.")

class AddRelations(FlaskForm):
	name = StringField("Name", validators=[DataRequired(), Length(min=2, max=55)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	number = StringField("Number", validators=[DataRequired(), Length(min=2, max=55)])
	submit = SubmitField("Add")

