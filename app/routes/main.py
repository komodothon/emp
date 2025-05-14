"""routes/main.py"""

from flask import Blueprint, render_template, redirect, request, url_for, flash, jsonify, current_user
from flask_login import login_required
from extensions import db, bcrypt
from app.models import User,Department, Role, Designation, ContractType, Status
from app.forms import EmployeeForm


main_bp = Blueprint("main", __name__)

@main_bp.route("/dashboard")
@login_required
def dashboard():
    print("[main dashboard] route hit")
    print(f"[main dashboard] current_user = {current_user}")


    try:
        users = User.query.all()
        departments = Department.query.all()
        roles = Role.query.all()
        designations = Designation.query.all()
        contract_types = ContractType.query.all()
        statuses = Status.query.all()

        return render_template(
            "dashboard.html",
            users=users,
            departments=departments,
            roles=roles,
            designations=designations,
            contract_types=contract_types,
            statuses=statuses,
        )
    except Exception as e:
        print(f"[Dashboard Error]: {e}")
        flash("An unexpected error occurred. Please try again.", "danger")
        return redirect(url_for("auth.login"))


@main_bp.route("/employee_list")
@login_required
def show_employee_list():
    employee_list = User.query.all()
    # print(employee_list)
    return render_template("employee_list.html", list=employee_list)

@main_bp.route("/view_employee/<int:id>")
@login_required
def view_employee(id):

    try:
        employee = User.query.get(id)
        if not employee:
            flash("Employee not found.", "danger")
            return redirect(url_for("dashboard"))
        
        departments = Department.query.all()
        roles = Role.query.all()
        designations = Designation.query.all()
        contract_types = ContractType.query.all()
        statuses = Status.query.all()
        
        return render_template("view_employee.html",
                               employee=employee,
                               departments=departments,
                               designations=designations,
                               contract_types=contract_types,
                               statuses=statuses
                               )
    
    except Exception as e:
        print(e)
        flash(f"An error occurred: {e}. Please try again.", "danger")
        return redirect(url_for("main.dashboard"))
    
@main_bp.route("/edit_employee/<int:id>", methods=["GET", "POST"])
@login_required
def edit_employee(id):

    # full use of flaskform here. choices are loaded and pre-populated here in this route.
    try:
        employee = User.query.get(id)
        
        if not employee:
            flash("Employee not found.", "danger")
            return redirect(url_for("main.show_employee_list"))

        form = EmployeeForm(obj=employee)

        # load form field choices and pre-populate with existing info.
        form.department.choices = [(d.id, d.name) for d in Department.query.all()]
        form.role.choices = [(r.id, r.name) for r in Role.query.all()]
        form.designation.choices = [(des.id, des.name) for des in Designation.query.all()]
        form.contract_type.choices = [(c.id, c.name) for c in ContractType.query.all()]
        form.status.choices = [(s.id, s.name) for s in Status.query.all()]

        if request.method == 'GET':
            form.department.data = employee.department_id
            form.role.data = employee.role_id
            form.designation.data = employee.designation_id
            form.contract_type.data = employee.contract_type_id
            form.status.data = employee.status_id

        if request.method == "POST":

            if form.validate_on_submit():      
                # username and email not to be updated via here, as they are unique. 

                employee.first_name = form.first_name.data
                employee.last_name = form.last_name.data
                employee.phone = form.phone.data
                employee.address = form.address.data
                
                employee.department_id = form.department.data
                employee.role_id = form.role.data
                employee.designation_id = form.designation.data
                employee.contract_type_id = form.contract_type.data
                employee.status_id = form.status.data

                employee.date_of_birth = form.date_of_birth.data
                employee.hire_date = form.hire_date.data
                employee.contract_end_date = form.contract_end_date.data
                
                db.session.commit()
                flash("Employee details updated successfully.", "success")
                # print(employee)
                return redirect(url_for("main.view_employee", id=employee.id))
            else:
                flash("Invalid data. Please try again.", "danger")
                # print(form.data)
                # print(form.errors)
            return redirect(url_for("main.view_employee", id=employee.id))
        return render_template("edit_employee.html",
                            employee=employee,
                            form=form
                            )
    except Exception as e:
        print(f"[Edit Employee Error]: {e}")
        flash("An unexpected error occurred. Please try again.", "danger")
        return redirect(url_for("main.dashboard"))


@main_bp.route("/add_employee", methods=["GET", "POST"])
@login_required
def add_employee():
    form = EmployeeForm()

    # load form field choices.
    form.department.choices = [(d.id, d.name) for d in Department.query.all()]
    print(form.department.choices)
    form.role.choices = [(r.id, r.name) for r in Role.query.all()]
    form.designation.choices = [(des.id, des.name) for des in Designation.query.all()]
    form.contract_type.choices = [(c.id, c.name) for c in ContractType.query.all()]
    form.status.choices = [(s.id, s.name) for s in Status.query.all()]

    if request.method == "POST":
        if form.validate_on_submit():
            print(form.data)
            new_employee = User(
                username = form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email = form.email.data,
                phone=form.phone.data,
                address=form.address.data,

                department_id=int(form.department.data),
                role_id=int(form.role.data),
                designation_id=int(form.designation.data),
                contract_type_id=int(form.contract_type.data),
                status_id=int(form.status.data),

                date_of_birth=form.date_of_birth.data,
                hire_date=form.hire_date.data,
                contract_end_date = form.contract_end_date.data,
            )

            db.session.add(new_employee)
            db.session.flush()

            password_str = f"Hello{new_employee.id}"
            new_employee.set_password(password_str)

            db.session.commit()

            flash("Employee added successfully.", "success")
            return redirect(url_for("main.dashboard"))
        else:
            print(form.data)
            print(form.errors)
            flash("Invalid data. Please try again.", "danger")
            return redirect(url_for("main.add_employee"))

    return render_template("add_employee.html",
                           form=form,
                           )

@main_bp.route("/search_employee", methods=["GET"])
def search_employee():
    
    # Check if there are search parameters in the request
    if request.args:
        search_params = request.args.to_dict()
        
        # Start with a base query
        query = User.query
        
        # Add search term filter if 'q' parameter exists
        if 'q' in search_params and search_params['q']:
            query = query.filter(
                (User.first_name.ilike(f"%{search_params['q']}%")) |
                (User.last_name.ilike(f"%{search_params['q']}%")) |
                (User.username.ilike(f"%{search_params['q']}%")) |
                (User.email.ilike(f"%{search_params['q']}%"))
            )
        
        # Add department filter if selected
        if search_params.get("department"):
            query = query.filter(User.department_id == search_params["department"])
        
        # Add role filter if selected
        if search_params.get("role"):
            query = query.filter(User.role_id == search_params["role"])
        
        # Add designation filter if selected
        if search_params.get("designation"):
            query = query.filter(User.designation_id == search_params["designation"])
        
        # Add contract_type filter if selected
        if search_params.get("contract_type"):
            query = query.filter(User.contract_type_id == search_params["contract_type"])
        
        # Add status filter if selected
        if search_params.get("status"):
            query = query.filter(User.status_id == search_params["status"])
        
        # Execute the query
        employees = query.all()
        
        # Format results for JSON response
        results = [{
            "id": emp.id,
            "username": emp.username,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "email": emp.email
        } for emp in employees]
        
        return jsonify(results)
    else:
        # If no search query, render the search page
        employees = User.query.all()
        departments = Department.query.all()
        roles = Role.query.all()
        designations = Designation.query.all()
        contract_types = ContractType.query.all()
        statuses = Status.query.all()

        return render_template("search_employee.html",
                            employees=employees,
                            departments=departments,
                            roles=roles,
                            designations=designations,
                            contract_types=contract_types,
                            statuses=statuses)


# Javascript dynamic routes
@main_bp.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    print(type(user.status_id))

    department_id = int(request.form.get('department'))
    role_id = int(request.form.get('role'))
    designation_id = int(request.form.get('designation'))
    contract_type_id = int(request.form.get('contract_type'))
    status_id = int(request.form.get('status'))

    print(department_id, role_id, designation_id, contract_type_id, status_id)
    user.department_id = department_id if department_id else user.department_id
    user.role_id = role_id if role_id else user.role_id
    user.designation_id = designation_id if designation_id else user.designation_id
    user.contract_type_id = contract_type_id if contract_type_id else user.contract_type_id
    user.status_id = status_id if status_id else user.status_id
    
    db.session.commit()
    flash("User details updated successfully!", "success")
    return redirect(url_for('main.dashboard'))



