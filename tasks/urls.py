"""
URL patterns for the Tasks application.

This module defines all the URL routes for the tasks app, including
authentication, task management, department management, and employee management.
"""

from django.urls import path

from . import views

# URL patterns for tasks
urlpatterns = [
    path("register/", views.add_user, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("home/", views.home, name="home"),
    path("users/", views.user_list, name="user-list"),
    path("create_task/", views.create_task, name="create-task"),
    path("employee_dashboard/", views.employee_dashboard, name="employee-dashboard"),
    path("log_time/<int:task_id>/", views.log_time, name="log-time"),
    # Department URLs
    path("create_department/", views.create_department, name="create-department"),
    path("department_list/", views.department_list, name="department-list"),
    path(
        "departments/edit/<int:department_id>/",
        views.edit_department,
        name="edit-department",
    ),
    path(
        "departments/delete/<int:department_id>/",
        views.delete_department,
        name="delete-department",
    ),
    # Employee URLs
    path("create_employee/", views.create_employee, name="create-employee"),
    path("employee_list/", views.employee_list, name="employee-list"),
]
