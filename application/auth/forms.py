from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class AddUserForm(FlaskForm):
    name = StringField("Koko nimi", [validators.Length(min=1, max=143)])
    username = StringField("Käyttäjänimi", [validators.Length(min=1, max=143)])
    password = PasswordField("Salasana", [validators.Length(min=1, max=143)])
  
    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    username = StringField("Käyttäjä", [validators.Length(min=1, max=143)])
    password = PasswordField("Salasana", [validators.Length(min=1, max=143)])
  
    class Meta:
        csrf = False
