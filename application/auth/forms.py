from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
  
class AddUserForm(FlaskForm):
    name = StringField("Koko nimi")
    username = StringField("Käyttäjänimi")
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    username = StringField("Käyttäjä")
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False
