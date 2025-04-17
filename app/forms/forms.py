"""forms/forms.py"""

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class EmployeeForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    phone = StringField("Phone")
    address = StringField("Address")

    department = SelectField("Department", choices=[], coerce=int)
    role = SelectField("Role", choices=[], coerce=int)
    designation = SelectField("Designation", choices=[], coerce=int)
    contract_type = SelectField("Contract Type", choices=[], coerce=int)
    status = SelectField("Status", choices=[], coerce=int)

    date_of_birth = DateField("Date of Birth", format="%Y-%m-%d")
    hire_date = DateField("Hire Date", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Save Changes")


