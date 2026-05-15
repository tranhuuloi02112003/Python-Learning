from .choices import ProjectStatus
from .models import Project


def create_project(data):
    # **data bung dict thành keyword arguments cho Project.objects.create().
    # Ví dụ: {"name": "..."} -> create(name="...")
    return Project.objects.create(**data)


def update_project(project, data):
    # data là dict từ form.cleaned_data; .items() lấy cả key và value.
    # Nếu chỉ lặp qua data thì Python chỉ trả về key, không có value để gán.
    for field, value in data.items():
        # Gán field động cho project, ví dụ field="name" -> project.name = value.
        setattr(project, field, value)
    project.save()
    return project


def archive_project(project):
    project.status = ProjectStatus.ARCHIVED
    # update_fields chỉ lưu các field được liệt kê; thêm updated_at để auto_now được ghi xuống DB.
    project.save(update_fields=["status", "updated_at"])
    return project


def restore_project(project):
    project.status = ProjectStatus.ACTIVE
    # update_fields chỉ lưu các field được liệt kê; thêm updated_at để auto_now được ghi xuống DB.
    project.save(update_fields=["status", "updated_at"])
    return project
