"""app/models/admin_entities.py"""

from .base import BaseModel
from extensions import db

class Department(BaseModel):
    __tablename__ = 'departments'

    category_name = "Departments"
    display_columns = ['id', 'name']
    parent_id = db.Column(
        db.Integer, 
        db.ForeignKey(
            "departments.id",
            use_alter=True, 
            name='fk_department_parent'),
        nullable=True,     
    )
    
    # relationship
    parent = db.relationship(
        "Department", 
        remote_side=lambda: [Department.id], 
        backref=db.backref("subdepartments", lazy="dynamic"),
    )

class Role(BaseModel):
    __tablename__ = 'roles'

    category_name = "Roles"
    display_columns = ['id', 'name']

class Designation(BaseModel):
    __tablename__ = 'designations'

    category_name = "Designations"
    display_columns = ['id', 'name']

class ContractType(BaseModel):
    __tablename__ = 'contract_types'

    category_name = "Contract_Types"
    display_columns = ['id', 'name']

class Status(BaseModel):
    __tablename__ = 'statuses'

    category_name = "Statuses"
    display_columns = ['id', 'name']