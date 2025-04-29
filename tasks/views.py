from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    DepartmentForm,
    EmployeeForm,
    GoalForm,
    TaskForm,
    TimeLogForm,
    UserCreationForm,
    UserEditForm,
)
from .models import Department, Employee, Goal, Task


# Admin and HOD Views
def is_admin(user):
    """Check if the user is an admin (staff user)."""
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def add_user(request):
    """View to add a new user. Only accessible by admin users."""
    if request.method != "POST":
        form = UserCreationForm()
        return render(request, "tasks/create-user.html", {"form": form})

    form = UserCreationForm(request.POST or None)
    if not form.is_valid():
        messages.error(request, "Please correct the errors below.")
        return render(request, "tasks/create-user.html", {"form": form})

    user = form.save(commit=False)
    user.set_password(form.cleaned_data["password"])
    user.save()
    messages.success(request, f"User '{user.username}' created successfully.")
    return redirect("home")


def user_login(request):
    """Authenticate and log in a user."""
    if request.method != "POST":
        return render(request, "tasks/login.html")

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return redirect("home")

    messages.error(request, "Invalid username or password.")
    return render(request, "tasks/login.html")


def user_logout(request):
    """Log out the currently logged-in user."""
    logout(request)
    return redirect("login_user")


@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    """Edit an existing user's details. Only accessible by admin users."""
    user = get_object_or_404(User, id=user_id)

    if request.method != "POST":
        form = UserEditForm(instance=user)
        return render(
            request, "session/edit_user.html", {"form": form, "user_obj": user}
        )

    form = UserEditForm(request.POST, instance=user)
    if not form.is_valid():
        messages.error(request, "Please correct the errors below.")
        return render(
            request, "session/edit_user.html", {"form": form, "user_obj": user}
        )

    form.save()
    messages.success(request, "User updated successfully.")
    return redirect("user_list")


@login_required
def create_task(request):
    """Create a new task. Only accessible by admin or HOD users."""
    if request.user.is_staff:
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.assigned_to = Employee.objects.get(user=request.user)
                task.save()
                return redirect("employee_dashboard")
        else:
            form = TaskForm()
        return render(request, "tasks/create_tasks.html", {"form": form})
    else:
        return redirect("unauthorized")  # or render a 403 page


# Employee Views


@login_required
def employee_dashboard(request):
    """Display the employee's dashboard with assigned tasks."""
    tasks = Task.objects.filter(assigned_to__user=request.user)
    return render(request, "tasks/employee_dashboard.html", {"tasks": tasks})


@login_required
def log_time(request, task_id):
    """Log working time for a specific task."""
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
    """Create a new personal goal for the logged-in employee."""
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
    """Display the goals for the logged-in employee."""
    goals = Goal.objects.filter(employee__user=request.user)
    return render(request, "tasks/goal_dashboard.html", {"goals": goals})


# Admin Views for Departments and Employees


@login_required
@user_passes_test(lambda u: u.is_staff)  # Restrict to admin staff only
def create_department(request):
    """Create a new department. Only accessible by admin staff."""
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
    """List all departments. Only accessible by admin staff."""
    departments = Department.objects.all()
    return render(request, "tasks/department_list.html", {"departments": departments})


@login_required
@user_passes_test(lambda u: u.is_staff)  # Restrict to admin staff only
def create_employee(request):
    """Create a new employee record. Only accessible by admin staff."""
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
    """List all employees. Only accessible by admin staff."""
    employees = Employee.objects.all()
    return render(request, "tasks/employee_list.html", {"employees": employees})


@login_required
def home(request):
    """Home page view for logged-in users."""
    user = request.user

    context = {
        "user": user,
    }

    return render(request, "tasks/home.html", context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    """List all users with pagination. Only accessible by admin staff."""
    users = User.objects.all().order_by("username")
    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tasks/user-list.html", {"users": page_obj})


def edit_department(request, department_id):
    """Edit an existing department."""
    department = get_object_or_404(Department, id=department_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
            return redirect("all_departments")
    else:
        form = DepartmentForm(instance=department)
    return render(
        request, "tasks/edit_department.html", {"form": form, "department": department}
    )


def delete_department(request, department_id):
    """Delete an existing department."""
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    messages.success(request, "Department deleted successfully.")
    return redirect("department_list")
