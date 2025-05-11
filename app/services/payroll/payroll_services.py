"""app/services/payroll_services.py"""

import os
import io

from flask import current_app
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


from app.models import User, PayrollRecord, SalaryStructure
from extensions import db



# helper function to check for duplicated
def check_payroll_exists(user_id, month):
    payroll_exists = False
    if PayrollRecord.query.filter_by(employee_id=user_id, salary_month=month).first():
        payroll_exists = True
    return payroll_exists

# helper function for calculating salary components
def calculate_salary_components(salary_structure):
    hra = salary_structure.basic * (salary_structure.hra_percentage / 100)
    allowances = salary_structure.basic * (salary_structure.allowances_percentage / 100)
    deductions_tax = salary_structure.basic * (salary_structure.deduction_tax_percentage / 100)
    deductions_others = salary_structure.basic * (salary_structure.deduction_others_percentage / 100)

    return hra, allowances, deductions_tax, deductions_others


# High level public function
def process_payroll_batch(department_ids: list, month: str):
    
    # status_id = 1 means "Active"
    employees = (
        User.query
        .filter(User.status_id == 1)
        .filter(User.department_id.in_(department_ids))
        .all()
    )
    for employee in employees:
        if not check_payroll_exists(employee.id, month):
            create_payroll_record(employee, month)


def create_payroll_record(employee, month):
    salary_structure = SalaryStructure.query.filter_by(employee_id=employee.id).first()

    if salary_structure:
        hra, allowances, deductions_tax, deductions_others = calculate_salary_components(salary_structure)

        basic = salary_structure.basic
        salary_gross = basic + hra + allowances

        salary_net = salary_gross - deductions_tax - deductions_others

        payroll_record = PayrollRecord(
            employee_id = employee.id,
            salary_month = month,

            basic = basic,
            hra =hra,
            allowances = allowances,

            deduction_tax = deductions_tax,
            deduction_others = deductions_others,

            salary_gross = salary_gross,
            salary_net = salary_net
        )

        db.session.add(payroll_record)
        db.session.commit()

    else:
        print(f"No salary structure found for {employee}")


def generate_payroll_records(id=None):

    query = db.session.query(
            User.id,
            User.first_name,
            User.last_name,
            PayrollRecord.salary_month,
            PayrollRecord.salary_gross,
            PayrollRecord.salary_net
    ).join(User, User.id == PayrollRecord.employee_id)

    if id is not None:
        query = query.filter(User.id == id)
    
    return query.all()
    
# Payslip related

def get_payslip_info(user_id, month):
    payroll_record = db.session.query(PayrollRecord).filter_by(employee_id=user_id, salary_month=month).first()

    if payroll_record:
        full_name = f"{payroll_record.employee.first_name} {payroll_record.employee.last_name}"
        employee_id = payroll_record.employee_id
        department = payroll_record.employee.department.name
        designation = payroll_record.employee.designation.name

        salary_month = payroll_record.salary_month

        base_salary = payroll_record.basic
        hra = payroll_record.hra
        allowances = payroll_record.allowances
        
        salary_gross = payroll_record.salary_gross

        deduction_tax = payroll_record.deduction_tax
        deduction_others = payroll_record.deduction_others
        salary_net = payroll_record.salary_net

        payslip_info = {
            "Full Name": full_name,
            "Employee ID": employee_id,
            "Department": department,
            "Designation": designation,
            "Salary Month": salary_month,
            "Base Salary": base_salary,
            "HRA": hra,
            "Allowances": allowances,
            "Gross Salary": salary_gross,
            "Tax Deductions": deduction_tax,
            "Other Deductions": deduction_others,
            "Net Salary": salary_net
        }
        return payslip_info
        

    else:
        return None
    

def generate_payslip_pdf(payslip_info):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    styles = getSampleStyleSheet()

    # --- Logo (top-right)
    logo_path = os.path.join(current_app.root_path, 'static', 'images', 'company_logo.jpg')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, width - 130, height - 100, width=80, height=60, preserveAspectRatio=True)

    # --- Table 1: Company and Employee Info
    company_info = Paragraph(
        "ACME Corporation Pvt. Ltd.<br/>123 Corporate Lane<br/>Tech City, India",
        styles["Normal"]
    )
    employee_info = Paragraph(
        f"""
        <b>Employee Name:</b> {payslip_info.get('Full Name', '')}<br/>
        <b>Employee ID:</b> {payslip_info.get('Employee ID', '')}<br/>
        <b>Department:</b> {payslip_info.get('Department', '')}<br/>
        <b>Designation:</b> {payslip_info.get('Designation', '')}<br/>
        <b>Salary Month:</b> {payslip_info.get('Salary Month', '')}
        """, styles["Normal"]
    )

    table1_data = [[company_info, employee_info]]
    table1 = Table(table1_data, colWidths=[width * 0.45, width * 0.45])
    table1.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    w1, h1 = table1.wrapOn(c, width, height)
    table1_y = height - 130  # Position for Table 1
    table1.drawOn(c, 40, table1_y - h1)

    # --- Table 2: Salary Components
    salary_components = []
    for key, value in payslip_info.items():
        if key in ['Full Name', 'Salary Month', 'Employee ID', 'Department', 'Designation']:
            continue
        if isinstance(value, (int, float)):
            value = f"${value:,.2f}"
        salary_components.append([key, value])

    if salary_components:
        salary_components.insert(0, ["Component", "Amount"])
        table2 = Table(salary_components, colWidths=[width * 0.5, width * 0.4])
        table2.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        w2, h2 = table2.wrapOn(c, width, height)

        # Position Table 2 below Table 1, with visible gap (e.g., 40 pts)
        table2_y = table1_y - h1 - 40
        table2.drawOn(c, 40, table2_y - h2)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer




