"""app/services/admin_services.py"""
from sqlalchemy import func
from datetime import datetime, timezone, timedelta

from extensions import db
from app.models import User, Department, Role, Status
import json


def build_department_tree(departments):
    tree= {}
    lookup = {
        dept.id: {
            "name": dept.name,
            "children": [],
        } for dept in departments
    }

    for dept in departments:
        if dept.parent_id:
            lookup[dept.parent_id]["children"].append(lookup[dept.id])
        else:
            tree[dept.id] = lookup[dept.id]
    return tree

def build_dashboard_data():
    total_employees = User.query.count()
    active_employees = User.query.filter(User.status.has(name = 'Active')).count()
    inactive_employees = User.query.filter(User.status.has(name = 'Inactive')).count()


    # employees distribution
    employees_by_department = db.session.query(
        Department.name, func.count(User.id)
    ).join(User, User.department_id==Department.id).group_by(Department.name).all()

    # print(f"employees_by_department: {json.dumps(dict(employees_by_department), indent=4)}")

    employees_by_role = db.session.query(
        Role.name, func.count(User.id)
    ).join(User.role).group_by(Role.name).all()

    # department hierarchy tree
    departments = Department.query.all()
    department_hierarchy = build_department_tree(departments)

    # critical alerts
    today = datetime.now(tz=timezone.utc).date()
    next_month = today + timedelta(days=30)

    resignations_soon = User.query.filter(User.status.has(name = "Under notice")).count()
    contracts_expiring = User.query.filter(User.contract_end_date <= next_month).count()
    new_employees_this_month = User.query.filter(
        func.extract('month', User.hire_date) == today.month
    ).count()

    # recent_activity 
    # recent_changes = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(5).all()
    recent_changes = "text"
    
    dashboard_data = {
        "organization_health": {
            "active_employees": active_employees,
            "inactive_employees": inactive_employees,
        },
        "employee_distribution": {
            "by_department": dict(employees_by_department),
            "by_role": dict(employees_by_role),
        },
        "departments_tree": department_hierarchy,
        "critical_alerts": {
            "resignations_soon": resignations_soon,
            "contracts_expiring": contracts_expiring,
            "new_employees_this_month": new_employees_this_month,
        },
        "recent_changes": recent_changes,
    }
    # print(f"[admin_services.py]: {dashboard_data}")
    return dashboard_data


