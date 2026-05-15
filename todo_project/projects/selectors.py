from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from .choices import ProjectStatus
from .models import Project


def get_active_projects():
    return Project.objects.filter(status=ProjectStatus.ACTIVE).order_by("name")


def get_project_detail(project_id):
    return get_object_or_404(Project, pk=project_id)


def get_project_progress():
    return (
        Project.objects.exclude(status=ProjectStatus.ARCHIVED)
        # annotate() thêm field tính toán tạm vào từng Project trong kết quả query.
        # "tasks" là related_name từ Task.project, nên Django đếm các task thuộc project đó.
        .annotate(
            # Tổng số task chưa archived của từng project.
            # Q(...) là điều kiện query; tasks__is_archived nghĩa là đi từ Project
            # qua related_name "tasks" sang field is_archived của Task.
            total_tasks=Count("tasks", filter=Q(tasks__is_archived=False)),
            # Số task đã done của từng project, cũng bỏ qua task archived.
            # Có thể truyền nhiều điều kiện vào Q(...), Django hiểu là AND.
            done_tasks=Count(
                "tasks",
                filter=Q(tasks__is_archived=False, tasks__status="done"),
            ),
        )
        .order_by("name")
    )


def get_project_tasks(project):
    return (
        project.tasks.filter(is_archived=False)
        # Lấy sẵn Project kèm theo mỗi Task để khi gọi task.project không query thêm.
        # Tối ưu database, không phải chặn Task truy cập ngược lại Project.
        .select_related("project")
        .order_by("status", "due_date", "-created_at")
    )
