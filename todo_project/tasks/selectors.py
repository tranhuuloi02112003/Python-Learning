from django.db.models import Case, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .choices import TaskStatus
from .models import Task


PRIORITY_ORDER = Case(
    When(priority="urgent", then=Value(1)),
    When(priority="high", then=Value(2)),
    When(priority="medium", then=Value(3)),
    When(priority="low", then=Value(4)),
    default=Value(5),
    output_field=IntegerField(),
)


def base_tasks():
    return Task.objects.filter(is_archived=False).select_related("project")


def apply_task_search_filter_sort(queryset, params):
    search = params.get("q")
    status = params.get("status")
    project_id = params.get("project")
    sort = params.get("sort", "newest")

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    if status:
        queryset = queryset.filter(status=status)
    if project_id:
        queryset = queryset.filter(project_id=project_id)

    if sort == "oldest":
        return queryset.order_by("created_at")
    if sort == "due_date":
        return queryset.order_by("due_date", "-created_at")
    if sort == "priority":
        return queryset.alias(priority_order=PRIORITY_ORDER).order_by(
            "priority_order", "due_date", "-created_at"
        )
    return queryset.order_by("-created_at")


def get_all_tasks(params=None):
    return apply_task_search_filter_sort(base_tasks(), params or {})


def get_inbox_tasks(params=None):
    params = params or {}
    queryset = base_tasks().filter(project__isnull=True)

    if params.get("created") == "today":
        queryset = queryset.filter(created_at__date=timezone.localdate())
    if params.get("deadline") == "yes":
        queryset = queryset.filter(due_date__isnull=False)

    return apply_task_search_filter_sort(queryset, params)


def get_today_tasks(params=None):
    today = timezone.localdate()
    return apply_task_search_filter_sort(
        base_tasks()
        .filter(due_date=today)
        .exclude(status__in=[TaskStatus.DONE, TaskStatus.CANCELLED]),
        params or {},
    )


def get_upcoming_tasks(params=None):
    today = timezone.localdate()
    return apply_task_search_filter_sort(
        base_tasks()
        .filter(due_date__gt=today)
        .exclude(status__in=[TaskStatus.DONE, TaskStatus.CANCELLED]),
        params or {},
    )


def get_overdue_tasks(params=None):
    today = timezone.localdate()
    return apply_task_search_filter_sort(
        base_tasks()
        .filter(due_date__lt=today)
        .exclude(status__in=[TaskStatus.DONE, TaskStatus.CANCELLED]),
        params or {},
    )


def get_completed_tasks(params=None):
    return apply_task_search_filter_sort(
        base_tasks().filter(status=TaskStatus.DONE), params or {}
    )


def get_today_completed_tasks():
    today = timezone.localdate()
    return (
        base_tasks()
        .filter(status=TaskStatus.DONE, completed_at__date=today)
        .order_by("-completed_at", "-updated_at")
    )


def get_task_detail(task_id):
    return get_object_or_404(base_tasks(), pk=task_id)
