"""seed/mod_contr_end_date.py"""

from random import randint

from app import create_app
from extensions import db
from app.models import User, ContractType
from datetime import date, timedelta




def main():

    app = create_app()
    # db.create_all()
    with app.app_context():
        contract = ContractType.query.filter_by(name='Contract').first()
        internship = ContractType.query.filter_by(name='Internship').first()

        contract_users = User.query.filter(User.contract_type.has(name='Contract')).all()
        internship_users = User.query.filter(User.contract_type.has(name='Internship')).all()

        


        if contract_users:
            for user in contract_users:
                random_days = randint(20, 40)
                user.contract_end_date = date.today() + timedelta(days=random_days)
            
        if internship_users:
            for user in internship_users:
                random_days = randint(20, 40)
                user.contract_end_date = date.today() + timedelta(days=random_days)

        db.session.commit()
        db.session.close()

if __name__ == "__main__":
    main()