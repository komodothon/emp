"""seed/seed_salary_structure.py"""

from app import create_app
from extensions import db
from app.models import User, SalaryStructure, Role

# helper function to create salary_structure instance
def create_salary_structure(structure, id):
    if structure:
        salary_structure = SalaryStructure(
            employee_id = id,
            basic = structure["basic"],
            hra_percentage = structure["hra_percentage"],
            allowances_percentage = structure["allowances_percentage"],
            deduction_tax_percentage = structure["deduction_tax_percentage"],
            deduction_others_percentage = structure["deduction_others_percentage"],
        )

        db.session.add(salary_structure)
        db.session.flush()
        
        print(f"[salary structure seed file] SalaryStructure instance id: {salary_structure.id}")


        return salary_structure

    else:
        return None

def seed_salary_structure():
    employees = User.query.all()

    structure_employee = {
        "basic": 5000,
        "hra_percentage": 20,
        "allowances_percentage": 10,
        "deduction_tax_percentage": 5,
        "deduction_others_percentage": 1,
    }

    structure_manager_or_admin = {
        "basic": 7000,
        "hra_percentage": 25,
        "allowances_percentage": 10,
        "deduction_tax_percentage": 6,
        "deduction_others_percentage": 1,
    }

    structure_super_admin = {
        "basic": 9000,
        "hra_percentage": 25,
        "allowances_percentage": 10,
        "deduction_tax_percentage": 6,
        "deduction_others_percentage": 1,
    }

    for employee in employees:
        try:
            match employee.role.name:
                case "Employee": 
                    employee.salary_structure = create_salary_structure(structure_employee, employee.id)
                case "Manager" | "Admin":
                    employee.salary_structure = create_salary_structure(structure_manager_or_admin, employee.id)
                case "SuperAdmin":
                    employee.salary_structure = create_salary_structure(structure_super_admin, employee.id)
                
                # fallback case
                case _:
                    print(f"Unknown role '{employee.role}' for employee ID {employee.id}")
                    # Optionally: raise an error or assign a default structure

        except Exception as e:
            print(f"[salary structure seed file] Error assigning salary structure to employee ID {employee.id}: {e}")

    db.session.commit()
    

def main():
    app = create_app()
    # db.create_all()
    with app.app_context():
        seed_salary_structure()

if __name__ == "__main__":
    main()