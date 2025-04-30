"""
Forms for user management, employee tracking, goal setting, journaling, and task/time logging in the task management app.
"""

from django import forms
from django.contrib.auth.models import User

from .models import Department, Employee, Goal, JournalEntry, Task, TimeLog


class UserCreationForm(forms.ModelForm):
    """
    Form for creating a new user, including password and admin access checkbox.
    """

    password = forms.CharField(widget=forms.PasswordInput)
    is_staff = forms.BooleanField(required=False, label="Is Admin?")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff",
        ]


class UserEditForm(forms.ModelForm):
    """
    Form for editing existing user profile information.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class DepartmentForm(forms.ModelForm):
    """
    Form for creating or updating a department.
    """

    class Meta:
        model = Department
        fields = ["name", "hod"]


class EmployeeForm(forms.ModelForm):
    """
    Form for creating or updating an employee.
    """

    class Meta:
        model = Employee
        fields = ["user", "department", "date_joined", "position"]


class GoalForm(forms.ModelForm):
    """
    Form for setting or editing a personal goal for an employee.
    """

    class Meta:
        model = Goal
        fields = ["title", "description", "target_date", "achieved"]


class JournalEntryForm(forms.ModelForm):
    """
    Form for logging a journal entry.
    """

    class Meta:
        model = JournalEntry
        fields = ["entry_date", "content"]


class TimeLogForm(forms.ModelForm):
    """
    Form for logging time spent on a task.
    """

    class Meta:
        model = TimeLog
        fields = ["start_time", "end_time"]


class TaskForm(forms.ModelForm):
    """
    Form for creating or editing a task.
    """

    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "due_date", "priority"]
