from django.contrib import admin

from .models import Department, Employee, Goal, JournalEntry, Task, TimeLog

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(TimeLog)
admin.site.register(Goal)
admin.site.register(JournalEntry)

# Register your models here.
