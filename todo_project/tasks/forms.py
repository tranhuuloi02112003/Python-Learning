from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']#Mình chỉ cần người dùng nhập Tên công việc (title) thôi.