from django.contrib.auth.models import User
from django.db import models

priority_choices = [("Low", "Low"), ("Medium", "Medium"), ("High", "High")]


# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    hod = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


# Employee Model
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees"
    )
    date_joined = models.DateField()
    position = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()


# Task Model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="tasks"
    )
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    priority = models.CharField(
        max_length=6, choices=priority_choices, default="Medium"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


# Time Log Model
class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="time_logs")
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="time_logs"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()  # Duration in seconds

    def __str__(self):
        return f"Time Log for {self.task.title}"


# Goal Model
class Goal(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="goals"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Journal Entry Model
class JournalEntry(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="journal_entries"
    )
    entry_date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return f"Journal Entry for {self.entry_date}"
