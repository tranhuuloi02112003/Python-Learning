from django.contrib import admin

# Register your models here.

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "priority", "due_date", "is_archived")
    list_filter = ("status", "priority", "is_archived", "project")
    search_fields = ("title", "description")
