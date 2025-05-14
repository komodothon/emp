"""app/routes/test.py"""

import json
from flask import Blueprint, render_template

from extensions import db
from app.services.test_services import build_department_tree
from app.models import User
from app.services.payroll.payroll_services import create_payroll_record


test_bp = Blueprint("test", __name__)

@test_bp.route("/test", methods=["GET"])
def test():
    tree = build_department_tree()
    # print(json.dumps(tree, indent=4))

    root_node = list(tree.values())[0] 

    user = db.session.get(User, 2)
    month = "2025-01"
    
    create_payroll_record(user, month)


    return render_template("test.html", tree=tree, root_node=root_node)