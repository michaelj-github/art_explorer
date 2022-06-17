from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length
from wtforms_validators import AlphaNumeric

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])

class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20), AlphaNumeric(message="Your username should be only letters and numbers, no symbols.")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class UpdateForm(FlaskForm):
    """User update form."""

    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])
    share = SelectField("Share your collection?", choices=[('Yes', 'Yes. Share my collection with other users.'), ('No', 'No. Do not share my collection.')])
    
class ChangePasswordForm(FlaskForm):
    """Change pasword form."""

    password = PasswordField("New Password", validators=[InputRequired(), Length(min=6, max=55)])

class UpdateComments(FlaskForm):
    """User comments update form."""

    comment = TextAreaField("Comments")    