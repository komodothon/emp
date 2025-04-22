"""seed/setup_db.py"""

import os
from dotenv import load_dotenv

from app import create_app
from extensions import db, bcrypt

from app.models import User, UserCredential, Department, Role, Designation, ContractType, Status

from random import randint, choice
from datetime import datetime, date, timedelta

load_dotenv()

app = create_app()

def gen_ph_no():
    first_no = choice([6, 7, 8, 9])
    rest_no = randint(100000000, 999999999)
    return f"+91{first_no}{rest_no}"

def gen_birth_date():
    start_date = datetime(1980, 1, 1)
    end_date = datetime(2000, 12, 31, 23, 59, 59)
    
    random_seconds = randint(0, int((end_date - start_date).total_seconds()))
    random_date = start_date + timedelta(seconds=random_seconds)
    
    return random_date

def gen_hire_date():
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 12, 31, 23, 59, 59)
    
    random_seconds = randint(0, int((end_date - start_date).total_seconds()))
    random_date = start_date + timedelta(seconds=random_seconds)
    
    return random_date

def assign_department_id():
    departments = Department.query.all()
    # print(departments)
    return choice(departments).id if departments else 1

def assign_role_id():
    roles = Role.query.all()
    return choice(roles).id if roles else 1

def assign_designation_id():
    designations = Designation.query.all()
    return choice(designations).id if designations else 1

def assign_contract_type_id():
    contract_types = ContractType.query.all()
    return choice(contract_types).id if contract_types else 1

def assign_status():
    statuses = Status.query.all()
    return choice(statuses).id if statuses else 1

def main():

    with app.app_context():
        # db.create_all()
        add_sample_users()

        db.session.commit()
        db.session.close()


def add_sample_users():

    superuser = User(
        username="kadir",
        email="kadir@sample.com",
        first_name = "Kadir",
        last_name = "Vedachalam",

        department_id = 1,
        role_id = 1,
        designation_id = 1,
        contract_type_id = 1,
        status_id = 1,

        phone = gen_ph_no(),
        address = f"address",
        date_of_birth = gen_birth_date(),
        hire_date = gen_hire_date(),
    )
    db.session.add(superuser)
    db.session.flush() # add user and flush to get the id

    superuser.set_password("Hello")

    if os.getenv("FLASK_ENV") == "development":
        for i in range(2, 15):

            username = f"user{i}"
            email = f"user{i}@sample.com"
            first_name = f"F{i}"
            last_name = f"L{i}"

            department_id = assign_department_id()
            role_id = assign_role_id()
            designation_id = assign_designation_id()
            contract_type_id = assign_contract_type_id()

            phone = gen_ph_no()
            address = f"address{i}"
            date_of_birth = gen_birth_date()
            hire_date = gen_hire_date()
            status_id = assign_status()

            user = User(
                username=username, 
                email=email, 
                first_name = first_name,
                last_name = last_name,
                department_id = department_id,
                role_id = role_id,
                designation_id = designation_id,
                contract_type_id = contract_type_id,
                phone = phone,
                address = address,
                date_of_birth = date_of_birth,
                hire_date = hire_date,
                status_id = status_id,
            )  
            db.session.add(user)
            db.session.flush() # add user and flush to get the id
            
            # Set password/user.credential
            user.set_password(f"Hello{i}")
       

if __name__ == "__main__":
    main()