"""app/models/payroll_models.py"""

from app.models.base import BaseModel
from extensions import db

class PayrollRecord(BaseModel):
    __tablename__ = "payroll_records"
    __table_args__ = (
        db.UniqueConstraint("employee_id", "salary_month", name="unique_employee_month"),
    )

    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, )

    salary_month = db.Column(db.String(7), nullable=False)
    basic = db.Column(db.Float, nullable=False)
    hra = db.Column(db.Float, default=0.0, nullable=True)
    allowances = db.Column(db.Float, default=0.0, nullable=True)
    deduction_tax = db.Column(db.Float, nullable=True, default=0.0)
    deduction_others = db.Column(db.Float, nullable=True, default=0.0)
    salary_gross = db.Column(db.Float, nullable=False)
    salary_net = db.Column(db.Float, nullable=False)

    employee = db.relationship("User", back_populates="payroll_records")


class SalaryStructure(BaseModel):
    __tablename__ = "salary_structures"

    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    basic = db.Column(db.Float, nullable=False)
    hra_percentage = db.Column(db.Float, nullable=True, default=0.0)
    allowances_percentage = db.Column(db.Float, nullable=True, default=0.0)
    deduction_tax_percentage = db.Column(db.Float, nullable=True, default=0.0)
    deduction_others_percentage = db.Column(db.Float, nullable=True, default=0.0)

    employee = db.relationship("User", back_populates="salary_structure")