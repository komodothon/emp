"""app/forms/employeeform.py"""

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired


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

    date_of_birth = DateField("Date of Birth", format="%d/%m/%Y")
    hire_date = DateField("Hire Date", format="%d/%m/%Y", validators=[DataRequired()])

    contract_end_date = DateField("Contract End Date", format="%d/%m/%Y", validators=[DataRequired()])
    submit = SubmitField("Save Changes")


