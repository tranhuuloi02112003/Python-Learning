from django import forms
from .models import Task

class TaskForm(forms.ModelForm):

    title = forms.CharField(
        min_length=3,
        widget=forms.TextInput(attrs={'placeholder': 'Nhập việc cần làm...'}),
        error_messages={
            'min_length': 'Tên công việc quá ngắn, hãy nhập ít nhất 3 ký tự!',
            'required': 'Vui lòng nhập công việc!'
        }
    )
    class Meta:
        model = Task
        fields = ['title', 'project'] 

    def clean_title(self):
         # Lấy dữ liệu người dùng đã nhập (lúc này Django đã tự strip() rồi)
        title = self.cleaned_data.get('title')

        if Task.objects.filter(title__iexact=title).exclude(pk= self.instance.pk).exists():
            raise forms.ValidationError('Việc này đã có trong danh sách!')

        return title
