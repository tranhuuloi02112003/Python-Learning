from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    # Tự động lấy giờ hiện tại khi tạo mới
    created_at = models.DateTimeField(auto_now_add=True)

    # Magic method
    def __str__(self):
        return self.title
