from django.db import models

from .choices import ProjectStatus


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color_theme = models.CharField(max_length=20, default="emerald")
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Meta trong model dùng để cấu hình thêm cho model.
        # ordering giúp Project.objects.all() mặc định sắp xếp theo name.
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def is_archived(self):
        return self.status == ProjectStatus.ARCHIVED

    @property
    def color_dot_class(self):
        return {
            "blue": "bg-blue-500",
            "orange": "bg-orange-500",
            "green": "bg-green-500",
            "purple": "bg-purple-500",
            "emerald": "bg-emerald-500",
        }.get(self.color_theme, "bg-emerald-500")

    @property
    def progress_percent(self):
        total = getattr(self, "total_tasks", 0) or 0
        done = getattr(self, "done_tasks", 0) or 0
        return int((done / total) * 100) if total else 0
