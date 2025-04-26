from django.contrib.auth.models import User
from django.db import models

priority_choices = [("Low", "Low"), ("Medium", "Medium"), ("High", "High")]


# Department Model
class Department(models.Model):
    """
    Represents a department within the organization.

    Attributes:
        name (str): Name of the department.
        hod (User): Head of Department, linked to the User model.
        created_at (date): Date the department was created.
        updated_at (date): Date the department was last updated.
    """

    name = models.CharField(max_length=100)
    hod = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manager")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        """Returns the department name as a string."""
        return self.name


# Employee Model
class Employee(models.Model):
    """
    Represents an employee in the organization.

    Attributes:
        user (User): One-to-one link with the User model.
        department (Department): Foreign key to the department.
        date_joined (date): Date the employee joined.
        position (str): Position/title of the employee.
        is_active (bool): Status if the employee is active.
        created_at (date): Date the record was created.
        updated_at (date): Date the record was last updated.
    """

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
        """Returns the full name of the user."""
        return self.user.get_full_name()


# Task Model
class Task(models.Model):
    """
    Represents a task assigned to an employee.

    Attributes:
        title (str): Title of the task.
        description (str): Details of the task.
        assigned_to (Employee): Employee to whom the task is assigned.
        due_date (date): Task deadline.
        completed (bool): Task completion status.
        priority (str): Priority of the task.
        created_at (datetime): When the task was created.
        updated_at (date): When the task was last updated.
    """

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
        """Returns the title of the task."""
        return self.title


# Time Log Model
class TimeLog(models.Model):
    """
    Represents a time log for a task performed by an employee.

    Attributes:
        task (Task): Task associated with the time log.
        employee (Employee): Employee who logged the time.
        start_time (datetime): Start time of the task.
        end_time (datetime): End time of the task.
        duration (timedelta): Duration of time spent.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="time_logs")
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="time_logs"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()  # Duration in seconds

    def __str__(self):
        """Returns a label indicating which task this time log belongs to."""
        return f"Time Log for {self.task.title}"


# Goal Model
class Goal(models.Model):
    """
    Represents a goal set by an employee.

    Attributes:
        employee (Employee): Employee who set the goal.
        title (str): Title of the goal.
        description (str): Details about the goal.
        target_date (date): Deadline to achieve the goal.
        achieved (bool): Whether the goal was achieved.
    """

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="goals"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)

    def __str__(self):
        """Returns the title of the goal."""
        return self.title


# Journal Entry Model
class JournalEntry(models.Model):
    """
    Represents a daily journal entry by an employee.

    Attributes:
        employee (Employee): Employee who wrote the entry.
        entry_date (date): Date of the journal entry.
        content (str): Content of the journal entry.
    """

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="journal_entries"
    )
    entry_date = models.DateField()
    content = models.TextField()

    def __str__(self):
        """Returns a string identifying the journal entry by its date."""
        return f"Journal Entry for {self.entry_date}"
