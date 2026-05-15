from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.AllTasksView.as_view(), name="all"),
    path("inbox/", views.InboxView.as_view(), name="inbox"),
    path("today/", views.TodayView.as_view(), name="today"),
    path("upcoming/", views.UpcomingView.as_view(), name="upcoming"),
    path("overdue/", views.OverdueView.as_view(), name="overdue"),
    path("completed/", views.CompletedView.as_view(), name="completed"),
    path("create/", views.TaskCreateView.as_view(), name="create"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.TaskUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.task_delete, name="delete"),
    path("<int:pk>/toggle/", views.task_toggle, name="toggle"),
    path("<int:pk>/archive/", views.task_archive, name="archive"),
]
