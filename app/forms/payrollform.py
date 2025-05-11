"""app/forms/payrollform.py"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectMultipleField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput

from datetime import date

class PayrollProcessForm(FlaskForm):
    salary_month = SelectField("Salary Month", validators=[DataRequired()], choices=[])

    # Option to process for entire org
    process_entire_org = BooleanField('Process for Entire Organization')
    
    # Checkbox list of departments
    departments = SelectMultipleField(
        "Select Departments",
        coerce=int,
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput(),
    )

    submit = SubmitField("Submit")
    


