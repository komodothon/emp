"""app/routes/payroll_route.py"""

from flask import Blueprint, render_template, request, jsonify, send_file
from flask_login import login_required
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.services import role_required, process_payroll_batch, generate_payroll_records, get_payslip_info, generate_payslip_pdf
# from app.services.payroll import process_payroll_batch

from app.forms import PayrollProcessForm
from app.models import Department, User, PayrollRecord

payroll_bp = Blueprint("payroll", __name__, url_prefix="/payroll")


@payroll_bp.route("/", methods=["GET", "POST"])
@login_required
@role_required("SuperAdmin")
def index():
    form = PayrollProcessForm()

    form.departments.choices = [(dept.id, dept.name) for dept in Department.query.all()]

    today = datetime.now()
    months = []

    for i in range(6):
        month_date = today - relativedelta(months=i)
        value = month_date.strftime('%Y-%m')
        display = month_date.strftime('%B %Y')
        months.append((value, display))
    
    form.salary_month.choices = months

    if form.validate_on_submit():
        action = request.form.get("action")        

        if action == "run":
            salary_month = form.salary_month.data
            # print(f"salary_month: {salary_month}")

            department_ids = form.departments.data

            process_payroll_batch(department_ids, salary_month)

        payroll_records = generate_payroll_records()

        return render_template("payroll/payroll_records.html", payroll_records=payroll_records)

    return render_template(
        "payroll/payroll_index.html", 
        form=form,
    )

@login_required
@role_required("SuperAdmin")
@payroll_bp.route("/search_payslip", methods=["GET", "POST"])
def search_payslip():
    user_id = request.args.get("employee_id")
    payroll_records = generate_payroll_records(user_id)
    print(f"[payroll_route]: payroll_records: {payroll_records}")

    return render_template("payroll/payroll_records.html", payroll_records=payroll_records)


@login_required
@role_required("SuperAdmin")
@payroll_bp.route("/payslip_pdf/<int:user_id>/<month>", methods=["GET"])
def payslip_pdf(user_id, month):
    payslip_info = get_payslip_info(user_id, month)

    if payslip_info:
        pdf_buffer = generate_payslip_pdf(payslip_info)
    return send_file(
        pdf_buffer,
        as_attachment=False,
        download_name=f"Payslip_{user_id}_{month}.pdf",
        mimetype='application/pdf'
    )






# JS AJAX routes

@payroll_bp.route("/search_suggestions", methods=["GET"])
def search_suggestions():
    query = request.args.get('q', "")

    if not query:
        return jsonify([])
    
    results = User.query.filter(
        (User.id.ilike(f"%{query}%")) |
        (User.first_name.ilike(f"%{query}%")) |
        (User.last_name.ilike(f"%{query}%"))
    ).limit(10).all()

    suggestions = [
        {
            "id": emp.id,
            "name": f"{emp.first_name} {emp.last_name}",
            "department": emp.department.name if emp.department else "N/A",
            "designation": emp.designation.name if emp.designation else "N/A",
        } for emp in results
    ]

    return jsonify(suggestions)
