from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import (
    DepartmentForm,
    EmployeeForm,
    GoalForm,
    TaskForm,
    TimeLogForm,
    UserCreationForm,
    UserEditForm,
)
from .models import Department, Employee, Goal, Task, TimeLog


# Admin and HOD Views
def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, f"User '{user.username}' created successfully.")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "session/add_user.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "tasks/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect("user_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserEditForm(instance=user)

    return render(request, "session/edit_user.html", {"form": form, "user_obj": user})


@login_required
def create_task(request):
    if request.user.is_staff:  # Admin or HOD can create tasks
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.assigned_to = Employee.objects.get(user=request.user)
                task.save()
                return redirect("dashboard")
        else:
            form = TaskForm()
        return render(request, "tasks/create_tasks.html", {"form": form})


# Employee Views


@login_required
def employee_dashboard(request):
    tasks = Task.objects.filter(assigned_to__user=request.user)
    return render(request, "tasks/employee_dashboard.html", {"tasks": tasks})


@login_required
def log_time(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == "POST":
        form = TimeLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.task = task
            log.employee = Employee.objects.get(user=request.user)
            log.save()
            return redirect("employee_dashboard")
    else:
        form = TimeLogForm()
    return render(request, "tasks/log_time.html", {"form": form, "task": task})


# Goal Views


@login_required
def create_goal(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.employee = Employee.objects.get(user=request.user)
            goal.save()
            return redirect("employee_dashboard")
    else:
        form = GoalForm()
    return render(request, "tasks/create_goal.html", {"form": form})


@login_required
def goal_dashboard(request):
    goals = Goal.objects.filter(employee__user=request.user)
    return render(request, "tasks/goal_dashboard.html", {"goals": goals})


# Admin Views for Departments and Employees


@login_required
@user_passes_test(lambda u: u.is_staff)  # Restrict to admin staff only
def create_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("department_list")
    else:
        form = DepartmentForm()
    return render(request, "tasks/create_department.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def department_list(request):
    departments = Department.objects.all()
    return render(request, "tasks/department_list.html", {"departments": departments})


@login_required
@user_passes_test(lambda u: u.is_staff)  # Restrict to admin staff only
def create_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
    else:
        form = EmployeeForm()
    return render(request, "tasks/create_employee.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "tasks/employee_list.html", {"employees": employees})
