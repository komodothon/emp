"""app/seed/setup_admin_db.py"""

from dotenv import load_dotenv
import os
load_dotenv()

from app import create_app
from extensions import db, bcrypt
from app.models import Department, Role, Designation, ContractType, Status

DEPARTMENTS = ["Admin Dept", "HR", "Finance", "IT", "Sales", "Engineering", "Production", "Quality", "Supply Chain"]
ROLES = [
    ("SuperAdmin", "Full access. Can manage users, departments, employees, payroll, etc."),
    ("Admin", "Manage employees and departments but cannot manage user accounts."),
    ("Manager", "Can view and manage employees within their department only."),
    ("Employee", "Can only see their own profile, attendance, and payslips."),
]
DESIGNATIONS = ["Admin Manager", "Admin Executive", "HR Manager", "HR Executive", "Finance Manager", "Finance Executive", "IT Manager", "IT Engineer", "Sales Manager", "Sales Executive", "Engineering Manager", "Senior Engineer", "Engineering Technician", "Production Manager", "Production Technician", "Quality Manager", "Quality Engineer", "Supply Chain Manager", "Supply Chain Executive"]
CONTRACT_TYPES = ["Permanent", "Contract", "Internship"]
STATUSES = ["Active", "Inactive"]

def create_department():
    for department_name in DEPARTMENTS:
        department = Department(name=department_name, description=f"{department_name} Department")
        db.session.add(department)

def create_role():
    for role_name in ROLES:
        role = Role(name=role_name[0], description=role_name[-1])
        db.session.add(role)

def create_designation():
    for designation_name in DESIGNATIONS:
        designation = Designation(name=designation_name, description=f"{designation_name} Designation")
        db.session.add(designation)

def create_contract_type():
    for contract_type_name in CONTRACT_TYPES:
        contract_type = ContractType(name=contract_type_name, description=f"{contract_type_name} Contract Type")
        db.session.add(contract_type)

def create_status():
    for status_name in STATUSES:
        status = Status(name=status_name, description=f"{status_name} Status")
        db.session.add(status)

def main():
    app = create_app()
    with app.app_context():
        # db.create_all()
        create_department()
        create_role()
        create_designation()
        create_contract_type()
        create_status()

        db.session.commit()
        db.session.close()


if __name__ == "__main__":
    main()

