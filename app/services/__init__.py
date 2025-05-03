"""app/services/__init__.py"""

from app.services.role_decorator import role_required
from app.services.department_services import get_parent_dept_choices
from app.services.admin_services import build_dashboard_data