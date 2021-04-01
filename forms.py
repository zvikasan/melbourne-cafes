from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, EqualTo


# WTForm
class AddCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    has_wifi = SelectField("Free WiFi available?", choices=['Yes', 'No'], validators=[DataRequired()])
    has_sockets = SelectField('Power Socket Availability', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    quiet_noisy = SelectField('Noise level in the cafe', choices=['Quiet', 'Noisy'], validators=[DataRequired()])
    location = StringField("In which suburb cafe is located?", validators=[DataRequired()])
    map_url = StringField("GoogleMaps link to Cafe address", validators=[DataRequired(), URL()])
    img_url = StringField("Link to a photo of cafe interior", validators=[DataRequired(), URL()])
    submit = SubmitField("Add Cafe")
    btn_cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})

class EditCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    coffee_price = StringField("Coffee price", validators=[DataRequired()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    has_wifi = SelectField("Free WiFi available?", choices=['Yes', 'No'], validators=[DataRequired()])
    has_sockets = SelectField('Power Socket Availability', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    quiet_noisy = SelectField('Noise level in the cafe', choices=['Quiet', 'Noisy'], validators=[DataRequired()])
    location = StringField("In which suburb cafe is located?", validators=[DataRequired()])
    map_url = StringField("GoogleMaps link to Cafe address", validators=[DataRequired(), URL()])
    img_url = StringField("Link to a photo of cafe interior", validators=[DataRequired(), URL()])
    submit = SubmitField("Update")
    btn_cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[EqualTo('password_2', message='Passwords must match')])
    password_2 = PasswordField("Repeat Password", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    submit = SubmitField("Register")
    btn_cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    register = SubmitField(label='Register', render_kw={'formnovalidate': True})
    btn_cancel = SubmitField(label='Cancel', render_kw={'formnovalidate': True})
