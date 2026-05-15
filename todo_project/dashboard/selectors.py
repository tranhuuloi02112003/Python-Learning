from datetime import timedelta

from django.utils import timezone

from projects.selectors import get_project_progress
from tasks.choices import TaskStatus
from tasks.models import Task
from tasks.selectors import get_overdue_tasks, get_today_tasks


def get_dashboard_summary():
    # Selector này chỉ đọc và gom số liệu cho dashboard, không thay đổi database.
    today = timezone.localdate()
    active = Task.objects.filter(is_archived=False)
    # Actionable = task còn cần xử lý, bỏ qua task đã done/cancelled.
    actionable = active.exclude(status__in=[TaskStatus.DONE, TaskStatus.CANCELLED])

    # Đầu tuần hiện tại, dùng để đếm task đã hoàn thành trong tuần.
    week_start = today - timedelta(days=today.weekday())

    # Lấy một vài task quan trọng để hiển thị nhanh trên dashboard.
    today_tasks_list = get_today_tasks({"sort": "priority"})[:5]
    overdue_tasks_list = get_overdue_tasks({"sort": "priority"})[:3]

    return {
        "total_tasks": active.count(),
        "today_tasks": actionable.filter(due_date=today).count(),
        "overdue_tasks": actionable.filter(due_date__lt=today).count(),
        "in_progress_tasks": active.filter(status=TaskStatus.IN_PROGRESS).count(),
        "completed_this_week": active.filter(
            status=TaskStatus.DONE, completed_at__date__gte=week_start
        ).count(),
        "today_tasks_list": today_tasks_list,
        "overdue_tasks_list": overdue_tasks_list,
        "project_progress": get_project_progress(),
    }
