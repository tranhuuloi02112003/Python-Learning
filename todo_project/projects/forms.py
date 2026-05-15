from django import forms

from .choices import ProjectStatus
from .models import Project


BASE_INPUT_CLASS = (
    "w-full rounded-lg border border-[#bccac0] bg-white px-3 py-2 text-sm "
    "text-[#191c1e] outline-none transition focus:border-[#059669] "
    "focus:ring-2 focus:ring-[#059669]/20"
)


class ProjectForm(forms.ModelForm):
    # ModelForm: form được tạo dựa trên model Project.
    # Dùng chung cho create/update project, Django sẽ tự map field form với field model.
    class Meta:
        # Khai báo model và các field được phép hiển thị/submit từ form.
        model = Project
        fields = ["name", "description", "color_theme", "status"]
        # widgets chỉ quyết định cách field render ra HTML và class CSS của input.
        widgets = {
            "name": forms.TextInput(
                attrs={"class": BASE_INPUT_CLASS, "placeholder": "Project name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": BASE_INPUT_CLASS,
                    "placeholder": "Short project description",
                    "rows": 3,
                }
            ),
            "color_theme": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
            "status": forms.Select(attrs={"class": BASE_INPUT_CLASS}),
        }

    # ChoiceField khai báo các option hợp lệ cho color_theme trong form.
    # Mỗi tuple là (giá trị lưu vào DB, nhãn hiển thị cho user).
    color_theme = forms.ChoiceField(
        choices=[
            ("emerald", "Emerald"),
            ("blue", "Blue"),
            ("orange", "Orange"),
            ("green", "Green"),
            ("purple", "Purple"),
        ],
        initial="emerald",
    )
    # status lấy option từ ProjectStatus.choices để render dropdown trạng thái.
    status = forms.ChoiceField(choices=ProjectStatus.choices, initial=ProjectStatus.ACTIVE)
