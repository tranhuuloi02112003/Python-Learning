from django import forms

from .models import Task


BASE_INPUT_CLASS = (
    "w-full rounded-lg border border-[#bccac0] bg-white px-3 py-2 text-sm "
    "text-[#191c1e] outline-none transition focus:border-[#059669] "
    "focus:ring-2 focus:ring-[#059669]/20"
)


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        min_length=3,
        widget=forms.TextInput(
            attrs={"class": BASE_INPUT_CLASS, "placeholder": "Task title", "minlength": "3"}
        ),
        error_messages={
            "min_length": "Tên công việc quá ngắn, hãy nhập ít nhất 3 ký tự.",
            "required": "Vui lòng nhập công việc.",
        },
    )

    class Meta:
        model = Task
        fields = ["title", "description", "project", "status", "priority", "due_date"]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "Add context, notes, or next steps",
                    "rows": 3,
                }
            ),
            "project": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
            "status": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
            "priority": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
            "due_date": forms.DateInput(
                attrs={"class": BASE_INPUT_CLASS, "type": "date"}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if Task.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Việc này đã có trong danh sách.")
        return title
