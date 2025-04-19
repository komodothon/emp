"""app/forms/departmentform.py"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class DepartmentForm(FlaskForm):
    name = StringField("Department Name", validators=[DataRequired()])
    description = StringField("Description")
    parent_id = SelectField("Parent Department", coerce=int, choices=[], default=None)
    submit = SubmitField("Save Changes")