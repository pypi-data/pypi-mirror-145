from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User

class SignupForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Must be 8 characters or longer")])
  confirm = PasswordField('Repeat Password', validators=[DataRequired(),  EqualTo('password', message="Passwords must match")])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username')
  
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class MessageForm(FlaskForm):
  message = StringField('message', validators=[DataRequired()])
  submit = SubmitField('Post')

class GroupCreateForm(FlaskForm): 
  member = SelectMultipleField('Add to group')
  name = StringField('message', validators=[DataRequired()], name="groupName")