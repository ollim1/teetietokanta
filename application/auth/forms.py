from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class AddUserForm(FlaskForm):
    name = StringField("Koko nimi", [validators.Length(min=1, max=143)])
    username = StringField("Käyttäjänimi", [validators.Length(min=1, max=143)])
    password = PasswordField("Salasana", [validators.Length(min=1, max=143), validators.equal_to("password_check", message="Salasanojen on oltava sama")])
    password_check = PasswordField("Sanasanan tarkistus", [validators.Length(min=1, max=143)])
  
    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    username = StringField("Käyttäjä", [validators.Length(min=1, max=143)])
    password = PasswordField("Salasana", [validators.Length(min=1, max=143)])
  
    class Meta:
        csrf = False
