"""app/routes/departments.py"""

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from app.models import Department
from extensions import db
from app.services import role_required
from app.forms import DepartmentForm
from app.services import get_parent_dept_choices

departments_bp = Blueprint("departments", __name__, url_prefix="/departments")

@departments_bp.route("/")
@login_required
@role_required("SuperAdmin")
def index():
    try:
        departments = Department.query.all()
    except Exception as e:
        flash("Error loading departments. Please try again later.", "danger")
        print(f"[Departments index error]: {e}")
        departments = []
    return render_template("departments/index.html", departments=departments)

@departments_bp.route("/add", methods=["GET", "POST"])
@login_required
@role_required("SuperAdmin")
def add_department():
    form = DepartmentForm()

    try:
        departments = Department.query.all()
        form.parent_id.choices = [(0, "None")] + [(d.id, d.name) for d in departments]
    except Exception as e:
        flash("Failed to prepare the form. Please try again.", "danger")
        print(f"[Departments add error]: {e}")
        return redirect(url_for("departments.index"))

    if form.validate_on_submit():
        try:
            parent_id = form.parent_id.data if form.parent_id.data != 0 else None
            new_department = Department(
                name=form.name.data,
                description=form.description.data,
                parent_id=parent_id
            )

            db.session.add(new_department)
            db.session.commit()
            flash(f"Department '{new_department.name}' added successfully.", "success")
            return redirect(url_for("departments.index"))

        except Exception as e:
            db.session.rollback()
            flash("Error saving the department. Please try again.", "danger")
            print(f"[Departments add error]: {e}")

    # Keep selected parent option on form errors
    if form.parent_id.data is None:
        form.parent_id.data = 0

    return render_template("departments/add.html", form=form)

@departments_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("SuperAdmin")
def edit_department(id):
    try:
        dept = Department.query.get_or_404(id)
    except Exception as e:
        flash(f"Department not found or other database error", "danger")
        print(f"[Departments edit load Error: {e}]")
        return redirect(url_for("departments.index"))
    
    form = DepartmentForm(obj=dept)

    try:
        # Populate parent field choices
        parent_dept_choices = get_parent_dept_choices(dept)
        form.parent_id.choices = [(0, "None")] + [(d.id, d.name) for d in parent_dept_choices]
    except Exception as e:
        flash("Error preparing form. Please try again later.", "danger")
        print(f"[Department edit form error: {e}]")
        return redirect(url_for("departments.index"))

    if form.validate_on_submit():
        try:
            dept.name = form.name.data
            dept.description = form.description.data
            dept.parent_id = form.parent_id.data if form.parent_id.data != 0 else None

            db.session.commit()
            flash("Department updated successfully.", "success")
            return redirect(url_for("departments.index"))
        except Exception as e:
            db.session.rollback()
            flash("Department edit error. Please try again later.", "danger")
            print(f"[Departments edit error: {e}]")
            return redirect(url_for("departments.index"))

    # Set the default selection for parent_id dropdown
    form.parent_id.data = dept.parent_id if dept.parent_id else 0

    return render_template("departments/edit.html", form=form)