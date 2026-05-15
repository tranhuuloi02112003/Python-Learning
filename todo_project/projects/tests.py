from django.test import TestCase
from django.urls import reverse

from tasks.choices import TaskStatus
from tasks.models import Task
from .models import Project
from .selectors import get_project_progress
from .services import archive_project, restore_project


class ProjectModelTests(TestCase):
    def test_defaults(self):
        project = Project.objects.create(name="TaskLog")
        self.assertEqual(str(project), "TaskLog")
        self.assertEqual(project.status, "active")


class ProjectSelectorTests(TestCase):
    def test_progress(self):
        project = Project.objects.create(name="TaskLog")
        Task.objects.create(title="Todo", project=project)
        Task.objects.create(title="Done", project=project, status=TaskStatus.DONE)

        project = get_project_progress().get(id=project.id)
        self.assertEqual(project.total_tasks, 2)
        self.assertEqual(project.done_tasks, 1)
        self.assertEqual(project.progress_percent, 50)


class ProjectServiceTests(TestCase):
    def test_archive_restore(self):
        project = Project.objects.create(name="TaskLog")
        archive_project(project)
        project.refresh_from_db()
        self.assertEqual(project.status, "archived")

        restore_project(project)
        project.refresh_from_db()
        self.assertEqual(project.status, "active")


class ProjectViewTests(TestCase):
    def test_detail_renders(self):
        project = Project.objects.create(name="TaskLog")
        response = self.client.get(reverse("projects:detail", args=[project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/detail.html")

