from django.urls import path

from . import views

# URL patterns for tasks
urlpatterns = [
    path("register/", views.add_user, name="register_user"),
    path("login/", views.user_login, name="login_user"),
    path("logout/", views.user_logout, name="logout"),
    path("create_task/", views.create_task, name="create_task"),
    path("employee_dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("log_time/<int:task_id>/", views.log_time, name="log_time"),
    # Department URLs
    path("create_department/", views.create_department, name="create_department"),
    path("department_list/", views.department_list, name="department_list"),
    # Employee URLs
    path("create_employee/", views.create_employee, name="create_employee"),
    path("employee_list/", views.employee_list, name="employee_list"),
]
