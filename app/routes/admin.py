"""admin.py"""

from flask import Blueprint, render_template, request, jsonify
from app.models import Department, Role, Designation, ContractType, Status, User
from extensions import db
from flask_login import login_required
from app.services import role_required
from sqlalchemy import func
from pprint import pprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

CATEGORY_MODELS = {
    "Departments": Department,
    "Roles": Role,
    "Designations": Designation,
    "Contract Types": ContractType
}


@admin_bp.route("/admin_dashboard")
@login_required
@role_required("SuperAdmin")
def admin_dashboard():
    criteria = [Department, Role, Designation, ContractType, Status]
    data = {}
    for model in criteria:
        data[model] = model.query.all()
    
    # Overview stats
    total_employees = User.query.count()

    employees_by_department = db.session.query(
        Department.name, func.count(User.id).label("No. of Users")
    ).join(User, User.department_id == Department.id).group_by(Department.name).all()
    
    employees_by_role = db.session.query(
        Role.name, func.count(User.id).label("No. of Users")
    ).join(User, User.role_id == Role.id).group_by(Role.name).all()

    employees_by_status = db.session.query(
        Status.name, func.count(User.id).label("No. of Users")
    ).join(User, User.status_id == Status.id).group_by(Status.name).all()

    overview = {
        "total_employees": total_employees,
        "by_department": employees_by_department,
        "by_role": employees_by_role,
        "by_status": employees_by_status,
    }

    return render_template("admin_dashboard.html", data=data, overview=overview)


@admin_bp.route("/add_criteria", methods=["POST"])
@login_required
@role_required("SuperAdmin")
def add_item():
    data = request.get_json()
    category = data.get("category")
    name = data.get("name")

    model = CATEGORY_MODELS.get(category)
    if model and name:
        new_item = model(name=name)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"error": "Invalid request"}), 400


@admin_bp.route("/edit_criteria", methods=["POST"])
@login_required
@role_required("SuperAdmin")
def edit_item():
    data = request.get_json()
    category = data.get("category")
    id = data.get("id")
    new_name = data.get("name")

    model = CATEGORY_MODELS.get(category)
    if model:
        item = model.query.get(id)
        if item:
            item.name = new_name
            db.session.commit()
            return jsonify({"success": True})
    return jsonify({"error": "Invalid request"}), 400



