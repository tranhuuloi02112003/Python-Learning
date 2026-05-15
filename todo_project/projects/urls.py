from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("create/", views.ProjectCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="edit"),
    path("<int:pk>/archive/", views.project_archive, name="archive"),
    path("<int:pk>/restore/", views.project_restore, name="restore"),
]

