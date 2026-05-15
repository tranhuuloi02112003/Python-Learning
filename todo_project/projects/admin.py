from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "color_theme", "created_at")
    list_filter = ("status", "color_theme")
    search_fields = ("name", "description")

