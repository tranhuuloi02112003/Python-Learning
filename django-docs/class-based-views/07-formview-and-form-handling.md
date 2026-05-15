# 07. FormView and Form Handling

## 1. Mục tiêu

File này học về `FormView` trong Django.

`FormView` dùng khi cần xử lý form, nhưng form đó không nhất thiết dùng để tạo hoặc cập nhật trực tiếp một model object.

Sau khi học xong phần này, cần hiểu được:

```txt
- FormView là gì
- FormView khác gì với CreateView và UpdateView
- Khi nào nên dùng FormView
- Khi nào không nên dùng FormView
- form_class dùng để làm gì
- template_name dùng để làm gì
- success_url dùng để làm gì
- form_valid() dùng khi nào
- form_invalid() dùng khi nào
- get_form_kwargs() dùng khi nào
- get_initial() dùng khi nào
```

File được chia thành 2 phần:

```txt
Part 1: Basic
Dùng khi cần hiểu FormView và xử lý form cơ bản.

Part 2: Advanced / Mở rộng
Dùng khi cần custom form, truyền thêm dữ liệu vào form, xử lý search/filter/upload/custom action.
```

---

# Part 1: Basic

## 2. FormView là gì?

`FormView` là generic class-based view dùng để hiển thị và xử lý form.

Nó xử lý flow cơ bản:

```txt
GET request
→ hiển thị form rỗng

POST request
→ bind dữ liệu vào form
→ validate form
→ nếu hợp lệ thì chạy form_valid()
→ nếu lỗi thì chạy form_invalid()
```

Nói ngắn gọn:

```txt
FormView = dùng để xử lý form custom
```

---

## 3. FormView khác gì với CreateView và UpdateView?

`CreateView` và `UpdateView` thường dùng với `ModelForm`.

Chúng có nhiệm vụ chính là:

```txt
CreateView → tạo object mới
UpdateView → cập nhật object đã có
```

Còn `FormView` không tự save model object.

`FormView` phù hợp với các form như:

```txt
- Contact form
- Search form
- Filter form
- Upload form
- Subscribe form
- Change password form
- Custom action form
- Form gửi email
- Form tính toán dữ liệu
```

Ví dụ:

```txt
User điền contact form
→ validate dữ liệu
→ gửi email
→ redirect tới trang thanks
```

Ở đây không nhất thiết tạo object trong database, nên `FormView` hợp lý hơn `CreateView`.

---

## 4. Khi nào dùng FormView?

Nên dùng `FormView` khi:

```txt
- Cần xử lý form nhưng không phải tạo model object
- Cần validate input rồi thực hiện custom action
- Cần gửi email
- Cần search/filter dữ liệu
- Cần upload file
- Cần gọi service khác
- Cần xử lý action sau khi submit
```

Ví dụ:

```txt
/contact/             → ContactForm
/search/              → SearchForm
/reports/export/      → ExportReportForm
/tasks/bulk-action/   → BulkActionForm
```

---

## 5. Khi nào không nên dùng FormView?

Không nên dùng `FormView` nếu mục tiêu chính là tạo hoặc sửa model object theo flow thông thường.

Ví dụ:

```txt
/tasks/create/       → CreateView
/tasks/1/edit/       → UpdateView
```

Không nên dùng `FormView` rồi tự viết toàn bộ logic save model nếu `CreateView` hoặc `UpdateView` đã làm tốt việc đó.

Quy tắc đơn giản:

```txt
Tạo object mới bằng ModelForm
→ CreateView

Sửa object đã có bằng ModelForm
→ UpdateView

Form custom không map trực tiếp CRUD model
→ FormView
```

---

## 6. Ví dụ ContactForm

Tạo form:

```python
# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

Form này không phải `ModelForm`.

Nó chỉ dùng để nhận input từ user.

---

## 7. Function-based view tương đương

Nếu viết bằng FBV:

```python
# views.py
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # send email or custom logic here

            return redirect("contact_success")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {
        "form": form,
    })
```

Ở đây mình tự xử lý:

```txt
1. Check request.method
2. Nếu GET thì tạo form rỗng
3. Nếu POST thì bind request.POST vào form
4. Validate form
5. Lấy cleaned_data
6. Xử lý custom action
7. Redirect nếu thành công
8. Render lại form nếu lỗi
```

---

## 8. Viết bằng FormView

```python
# views.py
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import ContactForm

class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        # send email or custom logic here

        return super().form_valid(form)
```

URL:

```python
# urls.py
from django.urls import path
from .views import ContactView
from django.views.generic import TemplateView

urlpatterns = [
    path("contact/", ContactView.as_view(), name="contact"),
    path(
        "contact/success/",
        TemplateView.as_view(template_name="pages/contact_success.html"),
        name="contact_success",
    ),
]
```

---

## 9. FormView đang làm thay mình những gì?

Khi user truy cập bằng GET:

```txt
1. Tạo form rỗng
2. Render template_name
```

Khi user submit bằng POST:

```txt
1. Bind request.POST vào form
2. Validate form
3. Nếu form hợp lệ thì gọi form_valid()
4. Nếu form lỗi thì gọi form_invalid()
5. Nếu form valid và form_valid() gọi super(), redirect tới success_url
```

Vì vậy ta không cần tự viết:

```python
if request.method == "POST":
    form = ContactForm(request.POST)

    if form.is_valid():
        ...
else:
    form = ContactForm()
```

`FormView` đã xử lý flow đó.

---

## 10. Template cho FormView

File:

```txt
templates/pages/contact.html
```

Ví dụ:

```django
<h1>Contact</h1>

<form method="post">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Send</button>
</form>
```

`FormView` tự truyền biến:

```txt
form
```

vào template.

Vì vậy template có thể dùng:

```django
{{ form.as_p }}
```

---

## 11. `form_class`

`form_class` cho Django biết cần dùng form nào.

Ví dụ:

```python
class ContactView(FormView):
    form_class = ContactForm
```

Nếu không khai báo `form_class`, Django không biết phải tạo form gì.

---

## 12. `template_name`

`template_name` cho Django biết cần render template nào.

Ví dụ:

```python
class ContactView(FormView):
    template_name = "pages/contact.html"
```

Nếu không khai báo `template_name`, Django sẽ không biết render form ở đâu, trừ khi có convention hoặc override method khác.

---

## 13. `success_url`

`success_url` cho Django biết sau khi form hợp lệ thì redirect đi đâu.

Ví dụ:

```python
success_url = reverse_lazy("contact_success")
```

Nếu không có `success_url`, sau khi form valid Django không biết redirect tới đâu, trừ khi bạn override `get_success_url()`.

---

## 14. `form_valid()`

`form_valid()` được gọi khi form hợp lệ.

Ví dụ:

```python
def form_valid(self, form):
    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]

    # custom logic

    return super().form_valid(form)
```

Dùng `form_valid()` khi cần xử lý dữ liệu đã validate.

Dữ liệu hợp lệ nằm trong:

```python
form.cleaned_data
```

Ví dụ:

```python
message = form.cleaned_data["message"]
```

Cuối method thường gọi:

```python
return super().form_valid(form)
```

để Django tiếp tục redirect tới `success_url`.

---

## 15. `form_invalid()`

`form_invalid()` được gọi khi form không hợp lệ.

Thông thường không cần override.

Nếu form lỗi, `FormView` tự render lại template cùng form errors.

Có thể override khi muốn log hoặc custom behavior.

```python
def form_invalid(self, form):
    print(form.errors)
    return super().form_invalid(form)
```

Quy tắc:

```txt
Form hợp lệ → form_valid()

Form lỗi → form_invalid()
```

---

## 16. Flow tổng quan của FormView

```txt
GET /contact/
    ↓
FormView tạo form rỗng
    ↓
Render contact.html

POST /contact/
    ↓
FormView bind request.POST vào form
    ↓
Validate form
    ↓
Nếu valid: gọi form_valid()
    ↓
Redirect success_url

Nếu invalid: gọi form_invalid()
    ↓
Render lại contact.html kèm errors
```

---

## 17. Bảng tổng kết Basic

| Thành phần       | Vai trò                     |
| ---------------- | --------------------------- |
| `FormView`       | Xử lý form custom           |
| `form_class`     | Form class cần dùng         |
| `template_name`  | Template render form        |
| `success_url`    | Redirect sau khi form valid |
| `form_valid()`   | Xử lý khi form hợp lệ       |
| `form_invalid()` | Xử lý khi form lỗi          |
| `cleaned_data`   | Dữ liệu đã validate         |

---

# Part 2: Advanced / Mở rộng

## 18. Khi nào cần xem phần Advanced?

Phần Basic đủ dùng khi:

```txt
- Form đơn giản
- Submit xong redirect cố định
- Không cần truyền thêm dữ liệu vào form
- Không cần initial data
- Không cần custom redirect
```

Cần xem phần Advanced khi gặp case như:

```txt
- Form cần user hiện tại
- Form cần dữ liệu từ URL kwargs
- Form cần initial data
- Redirect động theo dữ liệu submit
- Search/filter bằng GET
- Upload file
- Gửi email
- Thêm message
- Custom form rendering
```

---

## 19. Truyền user hiện tại vào form với `get_form_kwargs()`

Nhiều form cần biết user hiện tại.

Ví dụ form cần filter project theo user.

```python
# forms.py
from django import forms
from .models import Project

class ExportReportForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.none())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["project"].queryset = Project.objects.filter(
                created_by=self.user
            )
```

View:

```python
# views.py
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import ExportReportForm

class ExportReportView(FormView):
    template_name = "reports/export.html"
    form_class = ExportReportForm
    success_url = reverse_lazy("report_export_success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
```

Điểm chính:

```python
kwargs["user"] = self.request.user
```

Sau đó trong form lấy bằng:

```python
self.user = kwargs.pop("user", None)
```

---

## 20. Truyền dữ liệu từ URL kwargs vào form

Ví dụ URL:

```python
path(
    "projects/<int:project_pk>/export/",
    ExportProjectReportView.as_view(),
    name="project_export",
)
```

View:

```python
class ExportProjectReportView(FormView):
    template_name = "reports/export_project.html"
    form_class = ExportReportForm
    success_url = reverse_lazy("report_export_success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project_pk"] = self.kwargs["project_pk"]
        return kwargs
```

Form:

```python
class ExportReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.project_pk = kwargs.pop("project_pk", None)
        super().__init__(*args, **kwargs)
```

Dùng khi form cần biết context từ URL.

---

## 21. Set initial data với `get_initial()`

`get_initial()` dùng để set giá trị mặc định cho form.

Ví dụ URL:

```txt
/contact/?email=loi@example.com
```

View:

```python
class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")

    def get_initial(self):
        initial = super().get_initial()

        email = self.request.GET.get("email")
        if email:
            initial["email"] = email

        return initial
```

Khi user mở form, field email sẽ được fill sẵn.

Dùng `get_initial()` khi cần:

```txt
- Fill sẵn dữ liệu từ query params
- Fill sẵn dữ liệu từ user profile
- Fill sẵn dữ liệu từ object/context khác
```

---

## 22. Redirect động với `get_success_url()`

Nếu redirect phụ thuộc vào dữ liệu submit, dùng `get_success_url()`.

Ví dụ form chọn project, submit xong redirect về project detail.

```python
from django.urls import reverse

class ExportReportView(FormView):
    template_name = "reports/export.html"
    form_class = ExportReportForm

    def form_valid(self, form):
        self.project = form.cleaned_data["project"]

        # custom export logic

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_detail", kwargs={
            "pk": self.project.pk,
        })
```

Quy tắc:

```txt
Redirect cố định → success_url

Redirect phụ thuộc dữ liệu form → get_success_url()
```

---

## 23. Gửi email trong FormView

Ví dụ contact form gửi email.

```python
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import ContactForm

class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        send_mail(
            subject=f"Contact from {name}",
            message=message,
            from_email=email,
            recipient_list=["admin@example.com"],
        )

        return super().form_valid(form)
```

Trong thực tế, nên xử lý lỗi gửi mail nếu cần.

Ví dụ:

```python
def form_valid(self, form):
    try:
        send_mail(...)
    except Exception:
        form.add_error(None, "Could not send email. Please try again.")
        return self.form_invalid(form)

    return super().form_valid(form)
```

---

## 24. Thêm success message

Dùng `SuccessMessageMixin`:

```python
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

class ContactView(SuccessMessageMixin, FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully."
```

Template hiển thị messages:

```django
{% if messages %}
    <ul>
        {% for message in messages %}
            <li>{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
```

---

## 25. Search form bằng FormView

Có 2 kiểu search phổ biến:

```txt
GET search
POST search
```

Với search/filter, thường nên dùng GET để URL có thể share/bookmark.

Ví dụ:

```txt
/tasks/search/?q=django
```

Form:

```python
# forms.py
from django import forms

class TaskSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search")
```

View:

```python
# views.py
from django.views.generic.edit import FormView
from .forms import TaskSearchForm
from .models import Task

class TaskSearchView(FormView):
    template_name = "tasks/task_search.html"
    form_class = TaskSearchForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["data"] = self.request.GET or None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = context["form"]
        results = Task.objects.none()

        if form.is_valid():
            q = form.cleaned_data.get("q")

            if q:
                results = Task.objects.filter(title__icontains=q)

        context["results"] = results
        return context
```

Template:

```django
<form method="get">
    {{ form.as_p }}
    <button type="submit">Search</button>
</form>

<ul>
    {% for task in results %}
        <li>{{ task.title }}</li>
    {% empty %}
        <li>No results.</li>
    {% endfor %}
</ul>
```

Lưu ý:

```txt
Search/filter list thường có thể dùng ListView + get_queryset().
Nếu search chủ yếu là hiển thị danh sách object, ListView thường hợp hơn.
```

---

## 26. Upload file với FormView

Form:

```python
# forms.py
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
```

View:

```python
# views.py
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UploadFileForm

class UploadFileView(FormView):
    template_name = "files/upload.html"
    form_class = UploadFileForm
    success_url = reverse_lazy("upload_success")

    def form_valid(self, form):
        uploaded_file = form.cleaned_data["file"]

        # handle uploaded_file here
        # for chunk in uploaded_file.chunks():
        #     ...

        return super().form_valid(form)
```

Template:

```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Upload</button>
</form>
```

Điểm quan trọng:

```html
enctype="multipart/form-data"
```

Nếu thiếu dòng này, file upload sẽ không hoạt động đúng.

---

## 27. Custom action form

Ví dụ bulk complete task.

Form:

```python
# forms.py
from django import forms

class BulkCompleteTaskForm(forms.Form):
    task_ids = forms.CharField()

    def clean_task_ids(self):
        value = self.cleaned_data["task_ids"]

        try:
            ids = [int(item) for item in value.split(",") if item.strip()]
        except ValueError:
            raise forms.ValidationError("Invalid task ids.")

        return ids
```

View:

```python
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import BulkCompleteTaskForm
from .models import Task

class BulkCompleteTaskView(FormView):
    template_name = "tasks/bulk_complete.html"
    form_class = BulkCompleteTaskForm
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        task_ids = form.cleaned_data["task_ids"]

        Task.objects.filter(id__in=task_ids).update(is_done=True)

        return super().form_valid(form)
```

Dùng `FormView` rất hợp cho các action không phải CRUD một object đơn lẻ.

---

## 28. Thêm context cho form page

Dùng `get_context_data()`.

Ví dụ contact page cần thêm page title:

```python
class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Contact us"
        return context
```

Template:

```django
<h1>{{ page_title }}</h1>
```

---

## 29. Chọn form động với `get_form_class()`

Ví dụ staff dùng form khác user thường:

```python
class ReportFormView(FormView):
    template_name = "reports/report_form.html"
    success_url = reverse_lazy("report_success")

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminReportForm

        return UserReportForm
```

Dùng khi form phụ thuộc:

```txt
- user role
- query params
- URL kwargs
- loại action
```

Nếu không cần form động, dùng `form_class` là đủ.

---

## 30. Chọn template động với `get_template_names()`

Ví dụ mobile template khác desktop:

```python
class ContactView(FormView):
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")

    def get_template_names(self):
        if self.request.user.is_staff:
            return ["pages/staff_contact.html"]

        return ["pages/contact.html"]
```

Nếu không cần động, dùng:

```python
template_name = "pages/contact.html"
```

---

## 31. FormView với LoginRequiredMixin

Nếu form chỉ dành cho user đã login:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

class ExportReportView(LoginRequiredMixin, FormView):
    template_name = "reports/export.html"
    form_class = ExportReportForm
    success_url = reverse_lazy("report_success")
```

Thứ tự kế thừa nên là:

```python
class ExportReportView(LoginRequiredMixin, FormView):
```

Mixin thường đặt bên trái generic view.

---

## 32. Full example thực tế

Ví dụ form export report theo project của user.

Form:

```python
# forms.py
from django import forms
from .models import Project

class ExportReportForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.none())
    include_completed_tasks = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["project"].queryset = Project.objects.filter(
                created_by=user
            )
```

View:

```python
# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import ExportReportForm

class ExportReportView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "reports/export.html"
    form_class = ExportReportForm
    success_message = "Report export has been started."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.project = form.cleaned_data["project"]
        include_completed_tasks = form.cleaned_data["include_completed_tasks"]

        # Start export report job here
        # export_report(
        #     project=self.project,
        #     include_completed_tasks=include_completed_tasks,
        #     requested_by=self.request.user,
        # )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_detail", kwargs={
            "pk": self.project.pk,
        })
```

URL:

```python
# urls.py
from django.urls import path
from .views import ExportReportView

urlpatterns = [
    path("reports/export/", ExportReportView.as_view(), name="report_export"),
]
```

Template:

```django
<h1>Export Report</h1>

<form method="post">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Export</button>
</form>
```

---

## 33. Lỗi thường gặp

### 33.1. Quên `success_url`

Sai:

```python
class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
```

Nếu `form_valid()` gọi `super().form_valid(form)`, Django cần `success_url`.

Đúng:

```python
class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")
```

Hoặc override:

```python
def get_success_url(self):
    return reverse("contact_success")
```

---

### 33.2. Quên return trong `form_valid()`

Sai:

```python
def form_valid(self, form):
    send_mail(...)
```

Đúng:

```python
def form_valid(self, form):
    send_mail(...)
    return super().form_valid(form)
```

`form_valid()` phải return response.

---

### 33.3. Dùng `form.cleaned_data` trước khi form valid

Không nên lấy `cleaned_data` trước khi form đã validate.

Trong `form_valid()`, form đã valid nên dùng được:

```python
def form_valid(self, form):
    email = form.cleaned_data["email"]
```

---

### 33.4. Upload file nhưng thiếu `enctype`

Sai:

```django
<form method="post">
```

Đúng:

```django
<form method="post" enctype="multipart/form-data">
```

---

### 33.5. Truyền custom kwargs vào form nhưng form không pop ra

View:

```python
def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["user"] = self.request.user
    return kwargs
```

Form sai:

```python
class ExportReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
```

Form đúng:

```python
class ExportReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
```

Nếu không `pop("user")`, form có thể báo lỗi unexpected keyword argument.

---

### 33.6. Dùng FormView cho create model đơn giản

Không nên dùng `FormView` nếu đang tạo object model theo flow chuẩn.

Không nên:

```python
class TaskCreateView(FormView):
    form_class = TaskForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
```

Nên dùng:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
```

---

## 34. Bảng tổng kết method/attribute

| Method / Attribute     | Vai trò                        |
| ---------------------- | ------------------------------ |
| `form_class`           | Form class cần dùng            |
| `template_name`        | Template render form           |
| `success_url`          | Redirect cố định sau khi valid |
| `form_valid()`         | Xử lý khi form hợp lệ          |
| `form_invalid()`       | Xử lý khi form lỗi             |
| `get_success_url()`    | Redirect động                  |
| `get_form_kwargs()`    | Truyền thêm dữ liệu vào form   |
| `get_initial()`        | Set initial data               |
| `get_context_data()`   | Thêm context cho template      |
| `get_form_class()`     | Chọn form động                 |
| `get_template_names()` | Chọn template động             |

---

## 35. Nên dùng cách nào trong thực tế?

Dùng `FormView` khi:

```txt
Form không phải create/update model object theo flow chuẩn.
```

Ví dụ:

```txt
Contact form
→ FormView

Export report form
→ FormView

Upload file form
→ FormView

Bulk action form
→ FormView

Create task bằng ModelForm
→ CreateView

Update task bằng ModelForm
→ UpdateView
```

---

## 36. Kết luận

`FormView` là lựa chọn tốt khi cần xử lý form custom.

Cách nhớ:

```txt
CreateView = tạo object model

UpdateView = sửa object model

FormView = xử lý form custom
```

`FormView` tự xử lý:

```txt
GET form
POST form
Validate
form_valid()
form_invalid()
Redirect success_url
```

Khi cần custom, thường override:

```txt
form_valid()
form_invalid()
get_form_kwargs()
get_initial()
get_success_url()
get_context_data()
```

---

## 37. Ghi nhớ nhanh

```txt
FormView dùng cho form custom.

form_class cho biết dùng form nào.

template_name cho biết render template nào.

success_url cho biết redirect đi đâu sau khi form valid.

form_valid() chạy khi form hợp lệ.

form_invalid() chạy khi form lỗi.

cleaned_data chứa dữ liệu đã validate.

get_form_kwargs() dùng để truyền user, URL kwargs hoặc dữ liệu custom vào form.

get_initial() dùng để fill sẵn dữ liệu.

get_success_url() dùng khi redirect động.

Upload file cần enctype="multipart/form-data".

Nếu form là ModelForm để create/update object, ưu tiên CreateView/UpdateView.
```

---
