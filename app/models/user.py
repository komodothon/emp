"""app/models/user.py"""

from flask_login import UserMixin
from datetime import datetime

from extensions import db, bcrypt
from .base import BaseModel


class User(UserMixin, BaseModel):
    __tablename__ = 'users'


    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    designation_id = db.Column(db.Integer, db.ForeignKey('designations.id'), nullable=False)
    contract_type_id = db.Column(db.Integer, db.ForeignKey('contract_types.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)

    phone = db.Column(db.String(15), unique=True, nullable=True)
    address = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    hire_date = db.Column(db.Date, nullable=False, default=datetime.now)

    contract_end_date = db.Column(db.Date, nullable=True)

    # relationships
    credential = db.relationship("UserCredential", uselist=False, lazy="joined")

    department = db.relationship("Department", backref="users", uselist=False)
    role = db.relationship("Role", backref="users", uselist=False)
    designation = db.relationship("Designation", backref="users", uselist=False)
    contract_type = db.relationship("ContractType", backref="users", uselist=False)
    status = db.relationship("Status", backref="users", uselist=False)

    # payroll relationships
    payroll_records = db.relationship(
        "PayrollRecord", 
        back_populates="employee", 
        cascade="all, delete-orphan"
    )
    salary_structure = db.relationship(
        "SalaryStructure", 
        back_populates="employee", 
        cascade="all, delete-orphan", 
        uselist=False
    )

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} - {self.department} - {self.role}>"
        
    def set_password(self, plain_password):
        password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')
        self.credential = UserCredential(password_hash=password_hash)

    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self.credential.password_hash, plain_password)

    @property
    def status_name(self):
        return self.status.name if self.status else None

class UserCredential(BaseModel):
    __tablename__ = 'user_credentials'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)