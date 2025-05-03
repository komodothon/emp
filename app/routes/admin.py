"""admin.py"""

from flask import Blueprint, render_template, request, jsonify

from app.models import Department, Role, Designation, ContractType, Status, User
from extensions import db
from flask_login import login_required
from app.services import role_required
from sqlalchemy import func
from pprint import pprint
from app.services.admin_services import build_dashboard_data

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

    dashboard_data = build_dashboard_data()

    return render_template(
        "admin_dashboard.html",
        dashboard_data=dashboard_data,
    )

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



