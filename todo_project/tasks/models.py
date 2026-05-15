from django.db import models
from django.utils import timezone

from .choices import TaskPriority, TaskStatus


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # Tên quan hệ ngược: từ Project có thể gọi project.tasks.all()
        # để lấy các Task thuộc project đó.
        related_name="tasks",
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    priority = models.CharField(
        max_length=20,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM,
    )
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["status", "due_date", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_done(self):
        return self.status == TaskStatus.DONE

    @property
    def status_badge_class(self):
        return {
            TaskStatus.TODO: "bg-slate-100 text-slate-700",
            TaskStatus.IN_PROGRESS: "bg-blue-50 text-blue-700",
            TaskStatus.DONE: "bg-emerald-50 text-emerald-700",
            TaskStatus.CANCELLED: "bg-slate-100 text-slate-500",
        }.get(self.status, "bg-slate-100 text-slate-700")

    @property
    def priority_badge_class(self):
        return {
            TaskPriority.LOW: "bg-slate-100 text-slate-700",
            TaskPriority.MEDIUM: "bg-indigo-50 text-indigo-700",
            TaskPriority.HIGH: "bg-orange-50 text-orange-700",
            TaskPriority.URGENT: "bg-red-50 text-red-600",
        }.get(self.priority, "bg-slate-100 text-slate-700")

    @property
    def due_state(self):
        if not self.due_date:
            return "none"
        today = timezone.localdate()
        if self.due_date < today:
            return "overdue"
        if self.due_date == today:
            return "today"
        return "upcoming"

    @property
    def overdue_days(self):
        if self.due_state != "overdue":
            return 0
        return (timezone.localdate() - self.due_date).days
