from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    color_theme= models.CharField(max_length=15, default="blue")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # on_delete=models.CASCADE: Lệnh "Xóa dây chuyền
    # null=True, blank=True: Lệnh "Cho phép bỏ trống"
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    # Magic method
    def __str__(self):
        return self.title