from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView

from .forms import TaskForm
from .models import Task
from . import selectors, services

# Class base
class TaskListView(View):
    template_name = "tasks/all_tasks.html"
    page_title = "All Tasks"
    page_description = "Everything that is active across your workspace."
    active_nav = "all"
    topbar_search_placeholder = "Search tasks..."
    selector = staticmethod(selectors.get_all_tasks)

    def get(self, request):
        # request.GET là query params trên URL.
        tasks = self.selector(request.GET)
        return render(
            request,
            self.template_name,
            {
                "tasks": tasks,
                "page_title": self.page_title,
                "page_description": self.page_description,
                "active_nav": self.active_nav,
                "current_filters": request.GET,
                "topbar_search_action": request.path,
                "topbar_search_placeholder": self.topbar_search_placeholder,
            },
        )


class AllTasksView(TaskListView):
    pass


class InboxView(TaskListView):
    template_name = "tasks/inbox.html"
    page_title = "Inbox"
    page_description = "Tasks not assigned to a project yet."
    active_nav = "inbox"
    topbar_search_placeholder = "Search inbox tasks..."
    selector = staticmethod(selectors.get_inbox_tasks)


class TodayView(TaskListView):
    template_name = "tasks/today.html"
    page_title = "Today"
    page_description = "Tasks due today that still need attention."
    active_nav = "today"
    topbar_search_placeholder = "Search today's work..."
    selector = staticmethod(selectors.get_today_tasks)

    def get(self, request):
        tasks = self.selector(request.GET)
        completed_tasks = selectors.get_today_completed_tasks()
        return render(
            request,
            self.template_name,
            {
                "tasks": tasks,
                "completed_tasks": completed_tasks,
                "today_stats": {
                    "total": len(tasks) + len(completed_tasks),
                    "completed": len(completed_tasks),
                    "remaining": len(tasks),
                },
                "page_title": self.page_title,
                "page_description": self.page_description,
                "active_nav": self.active_nav,
                "current_filters": request.GET,
                "topbar_search_action": request.path,
                "topbar_search_placeholder": self.topbar_search_placeholder,
            },
        )


class UpcomingView(TaskListView):
    template_name = "tasks/upcoming.html"
    page_title = "Upcoming"
    page_description = "Future work ordered by your filters."
    active_nav = "upcoming"
    topbar_search_placeholder = "Search upcoming work..."
    selector = staticmethod(selectors.get_upcoming_tasks)


class OverdueView(TaskListView):
    template_name = "tasks/overdue.html"
    page_title = "Overdue"
    page_description = "Past due tasks that are not done or cancelled."
    active_nav = "overdue"
    topbar_search_placeholder = "Search overdue tasks..."
    selector = staticmethod(selectors.get_overdue_tasks)


class CompletedView(TaskListView):
    template_name = "tasks/completed.html"
    page_title = "Completed"
    page_description = "Finished work that is still visible in your workspace."
    active_nav = "completed"
    topbar_search_placeholder = "Search completed tasks..."
    selector = staticmethod(selectors.get_completed_tasks)

# Các view chi tiết, tạo/sửa task
class TaskCreateView(View):
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            services.create_task(form)
            messages.success(request, "Task created.")
            return redirect(request.POST.get("next") or "tasks:all")
        messages.error(request, "Task could not be created. Please check your input.")
        return redirect(request.POST.get("next") or "tasks:all")


class TaskUpdateView(View):
    def post(self, request, pk):
        # pk được Django lấy từ URL pattern <int:pk> và truyền vào method post().
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            services.update_task(form)
            messages.success(request, "Task updated.")
        else:
            messages.error(request, "Task could not be updated.")
        return redirect("tasks:detail", pk=task.pk)


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"

    def get_queryset(self):
        # Override get_queryset() của DetailView để chỉ cho phép lấy task chưa archived.
        return selectors.base_tasks()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "all"
        context["edit_task_form"] = TaskForm(instance=self.object)
        return context


def task_toggle(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        services.toggle_task_done(task)
        messages.success(request, "Task status updated.")
    return redirect(request.POST.get("next") or "tasks:all")


def task_archive(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        services.archive_task(task)
        messages.success(request, "Task archived.")
    return redirect(request.POST.get("next") or "tasks:all")


def task_delete(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        services.delete_task(task)
        messages.success(request, "Task deleted.")
    return redirect(request.POST.get("next") or "tasks:all")
