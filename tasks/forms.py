from django import forms
from django.contrib.auth.models import User

from .models import Department, Employee, Goal, JournalEntry, Task, TimeLog


class UserCreationForm(forms.ModelForm):
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
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


# Department Form
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "hod"]


# Employee Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["user", "department", "date_joined", "position"]


# Goal Form
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["title", "description", "target_date", "achieved"]


# Journal Entry Form
class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["entry_date", "content"]


# Time Log Form
class TimeLogForm(forms.ModelForm):
    class Meta:
        model = TimeLog
        fields = ["start_time", "end_time"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "due_date", "priority"]
