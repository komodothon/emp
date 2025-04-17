"""app/models/admin_entities.py"""

from .base import BaseModel
from extensions import db

class Department(BaseModel):
    __tablename__ = 'departments'

    category_name = "Departments"
    display_columns = ['id', 'name']

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