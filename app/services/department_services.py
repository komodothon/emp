"""app/services/department_services.py"""


from app.models import Department

def get_descendent_dept_ids(department):
    ids = set()
    for sub in department.subdepartments:
        ids.add(sub.id)
        ids.update(get_descendent_dept_ids(sub))
    return ids

def get_parent_dept_choices(department):
    # below returns a list
    all_departments = Department.query.all()
    # below is a set
    excluded_ids = get_descendent_dept_ids(department)
    # Also exclude subject department
    excluded_ids.add(department.id)  

    parent_dept_choices = [dept for dept in all_departments if dept.id not in excluded_ids]
    return parent_dept_choices