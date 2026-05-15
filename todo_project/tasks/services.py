from django.utils import timezone

from .choices import TaskStatus


def create_task(data):
    return data.save()


def update_task(form):
    return form.save()


def delete_task(task):
    task.delete()


def mark_task_done(task):
    task.status = TaskStatus.DONE
    task.completed_at = timezone.now()
    task.save(update_fields=["status", "completed_at", "updated_at"])
    return task


def restore_task(task):
    task.status = TaskStatus.TODO
    task.completed_at = None
    task.save(update_fields=["status", "completed_at", "updated_at"])
    return task


def toggle_task_done(task):
    if task.status == TaskStatus.DONE:
        return restore_task(task)
    return mark_task_done(task)


def archive_task(task):
    task.is_archived = True
    task.save(update_fields=["is_archived", "updated_at"])
    return task
