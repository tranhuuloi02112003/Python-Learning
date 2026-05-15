from django.db import models


class ProjectStatus(models.TextChoices):
    # TextChoices là enum của Django dùng cho CharField có choices.
    # Mỗi dòng gồm (giá trị lưu trong DB, nhãn hiển thị cho user).
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"
    ARCHIVED = "archived", "Archived"
