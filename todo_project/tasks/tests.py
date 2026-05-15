from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from projects.models import Project
from .choices import TaskPriority, TaskStatus
from .models import Task
from . import selectors, services


class TaskModelTests(TestCase):
    def test_defaults(self):
        task = Task.objects.create(title="Write plan")
        self.assertEqual(str(task), "Write plan")
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertEqual(task.priority, TaskPriority.MEDIUM)


class TaskSelectorTests(TestCase):
    def setUp(self):
        today = timezone.localdate()
        self.project = Project.objects.create(name="TaskLog")
        self.inbox = Task.objects.create(title="Inbox")
        self.today = Task.objects.create(title="Today", due_date=today)
        self.upcoming = Task.objects.create(title="Upcoming", due_date=today + timedelta(days=2))
        self.overdue = Task.objects.create(title="Overdue", due_date=today - timedelta(days=2))
        self.done = Task.objects.create(title="Done", status=TaskStatus.DONE)
        self.archived = Task.objects.create(title="Archived", is_archived=True)

    def test_page_selectors(self):
        self.assertIn(self.inbox, selectors.get_inbox_tasks())
        self.assertIn(self.today, selectors.get_today_tasks())
        self.assertIn(self.upcoming, selectors.get_upcoming_tasks())
        self.assertIn(self.overdue, selectors.get_overdue_tasks())
        self.assertIn(self.done, selectors.get_completed_tasks())
        self.assertNotIn(self.archived, selectors.get_all_tasks())


class TaskServiceTests(TestCase):
    def test_done_restore_archive(self):
        task = Task.objects.create(title="Ship")
        services.mark_task_done(task)
        task.refresh_from_db()
        self.assertEqual(task.status, TaskStatus.DONE)
        self.assertIsNotNone(task.completed_at)

        services.restore_task(task)
        task.refresh_from_db()
        self.assertEqual(task.status, TaskStatus.TODO)
        self.assertIsNone(task.completed_at)

        services.archive_task(task)
        task.refresh_from_db()
        self.assertTrue(task.is_archived)


class TaskViewTests(TestCase):
    def test_list_pages_render(self):
        expected_templates = {
            "all": "tasks/all_tasks.html",
            "inbox": "tasks/inbox.html",
            "today": "tasks/today.html",
            "upcoming": "tasks/upcoming.html",
            "overdue": "tasks/overdue.html",
            "completed": "tasks/completed.html",
        }
        for name, template in expected_templates.items():
            response = self.client.get(reverse(f"tasks:{name}"))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

    def test_detail_renders(self):
        task = Task.objects.create(title="Detail")
        response = self.client.get(reverse("tasks:detail", args=[task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/detail.html")
