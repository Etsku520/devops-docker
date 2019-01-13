from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username", [validators.length(min=5, max=22)])
    password = PasswordField("Password", [validators.length(min=5, max=22)])
  
    class Meta:
        csrf = False

class RegisterationForm(FlaskForm):
    name = StringField("Name", [validators.length(min=4, max=22)])
    username = StringField("Username", [validators.length(min=5, max=22)])
    password = PasswordField("Password", [validators.length(min=5, max=22)])
    repeat = PasswordField("Repeat")
  
    class Meta:
        csrf = False
