# 06. CreateView, UpdateView and DeleteView

## 1. Mục tiêu

File này học về 3 generic class-based views dùng cho CRUD trong Django:

```txt
CreateView
UpdateView
DeleteView
```

File được chia thành 2 phần:

```txt
Part 1: Basic
Dùng khi cần tạo, sửa, xóa object theo flow cơ bản.

Part 2: Advanced / Mở rộng
Dùng khi cần custom form, gán user, custom redirect, permission, success message, hoặc xử lý logic trước/sau khi save/delete.
```

Sau khi học xong phần này, cần hiểu được:

```txt
- CreateView dùng để làm gì
- UpdateView dùng để làm gì
- DeleteView dùng để làm gì
- Cách dùng model, form_class, fields, template_name, success_url
- reverse_lazy() dùng để làm gì
- form_valid() dùng khi nào
- get_success_url() dùng khi nào
- Cách xử lý create/update/delete theo user hiện tại
```

---

# Part 1: Basic

## 2. Model và Form ví dụ dùng chung

Giả sử ta có model `Task`:

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    def __str__(self):
        return self.title
```

Form:

```python
# forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "is_done"]
```

Lưu ý:

```txt
created_by không nằm trong form vì field này nên được gán tự động bằng user đang login.
```

---

## 3. CreateView là gì?

`CreateView` dùng để tạo object mới thông qua form.

Ví dụ:

```txt
/tasks/create/
```

Khi user truy cập bằng GET:

```txt
Hiển thị form tạo task.
```

Khi user submit form bằng POST:

```txt
Validate form → save object → redirect.
```

Nói ngắn gọn:

```txt
CreateView = dùng để tạo object mới
```

---

## 4. UpdateView là gì?

`UpdateView` dùng để sửa object đã tồn tại.

Ví dụ:

```txt
/tasks/1/edit/
```

Khi user truy cập bằng GET:

```txt
Hiển thị form với dữ liệu hiện tại của task.
```

Khi user submit form bằng POST:

```txt
Validate form → update object → redirect.
```

Nói ngắn gọn:

```txt
UpdateView = dùng để cập nhật object
```

---

## 5. DeleteView là gì?

`DeleteView` dùng để xóa object.

Ví dụ:

```txt
/tasks/1/delete/
```

Khi user truy cập bằng GET:

```txt
Hiển thị màn xác nhận xóa.
```

Khi user submit confirm bằng POST:

```txt
Xóa object → redirect.
```

Nói ngắn gọn:

```txt
DeleteView = dùng để xóa object
```

---

## 6. CreateView cơ bản

### 6.1. Function-based view tương đương

Nếu viết bằng FBV:

```python
# views.py
from django.shortcuts import render, redirect
from .forms import TaskForm

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {
        "form": form,
    })
```

Ở đây mình tự xử lý:

```txt
1. Kiểm tra request.method
2. Nếu GET thì tạo form rỗng
3. Nếu POST thì bind request.POST vào form
4. Validate form
5. Save object
6. Redirect nếu thành công
7. Render lại form nếu có lỗi
```

---

### 6.2. Viết bằng CreateView

```python
# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Task
from .forms import TaskForm

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")
```

URL:

```python
# urls.py
from django.urls import path
from .views import TaskCreateView

urlpatterns = [
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
]
```

---

### 6.3. CreateView đang làm thay mình những gì?

Khi user truy cập bằng GET:

```txt
1. Tạo form rỗng
2. Render template_name
```

Khi user submit bằng POST:

```txt
1. Bind request.POST vào form
2. Validate form
3. Nếu form hợp lệ thì save object
4. Redirect tới success_url
5. Nếu form lỗi thì render lại template kèm errors
```

Vì vậy ta không cần tự viết:

```python
if request.method == "POST":
    form = TaskForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect("task_list")
else:
    form = TaskForm()
```

---

## 7. Template cho CreateView

File:

```txt
templates/tasks/task_form.html
```

Ví dụ:

```django
<h1>Create Task</h1>

<form method="post">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Save</button>
</form>

<a href="{% url 'task_list' %}">Back to list</a>
```

`CreateView` tự truyền biến:

```txt
form
```

vào template.

Vì vậy template có thể dùng:

```django
{{ form.as_p }}
```

---

## 8. UpdateView cơ bản

### 8.1. Function-based view tương đương

Nếu viết bằng FBV:

```python
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("task_detail", pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {
        "form": form,
        "task": task,
    })
```

Ở đây mình tự xử lý:

```txt
1. Lấy object theo pk
2. Nếu không có thì trả 404
3. Nếu GET thì tạo form với instance=task
4. Nếu POST thì bind request.POST với instance=task
5. Validate form
6. Save object đã update
7. Redirect
8. Render lại form nếu lỗi
```

---

### 8.2. Viết bằng UpdateView

```python
# views.py
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Task
from .forms import TaskForm

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")
```

URL:

```python
# urls.py
from django.urls import path
from .views import TaskUpdateView

urlpatterns = [
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_update"),
]
```

---

### 8.3. UpdateView đang làm thay mình những gì?

Khi user truy cập:

```txt
/tasks/1/edit/
```

`UpdateView` tự xử lý:

```txt
1. Lấy object Task theo pk
2. Nếu không tìm thấy thì trả 404
3. Nếu GET thì tạo form với instance hiện tại
4. Render template_name
5. Nếu POST thì bind request.POST với instance hiện tại
6. Validate form
7. Nếu form hợp lệ thì save object
8. Redirect tới success_url
9. Nếu form lỗi thì render lại template
```

Vì vậy ta không cần tự viết:

```python
task = get_object_or_404(Task, pk=pk)
form = TaskForm(request.POST, instance=task)
```

---

## 9. Dùng chung template cho CreateView và UpdateView

Vì cả create và update đều dùng form, có thể dùng chung:

```txt
templates/tasks/task_form.html
```

Template:

```django
{% if object %}
    <h1>Edit Task</h1>
{% else %}
    <h1>Create Task</h1>
{% endif %}

<form method="post">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Save</button>
</form>

<a href="{% url 'task_list' %}">Back to list</a>
```

Trong `UpdateView`, object hiện tại thường có trong template dưới tên:

```txt
object
```

Nếu có khai báo:

```python
context_object_name = "task"
```

thì cũng có thể dùng:

```django
{{ task }}
```

Ví dụ:

```python
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    context_object_name = "task"
    success_url = reverse_lazy("task_list")
```

---

## 10. DeleteView cơ bản

### 10.1. Function-based view tương đương

Nếu viết bằng FBV:

```python
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {
        "task": task,
    })
```

Ở đây mình tự xử lý:

```txt
1. Lấy object theo pk
2. Nếu không có thì trả 404
3. Nếu GET thì render confirm page
4. Nếu POST thì gọi task.delete()
5. Redirect
```

---

### 10.2. Viết bằng DeleteView

```python
# views.py
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Task

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")
```

URL:

```python
# urls.py
from django.urls import path
from .views import TaskDeleteView

urlpatterns = [
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]
```

---

### 10.3. DeleteView đang làm thay mình những gì?

Khi user truy cập bằng GET:

```txt
1. Lấy object theo pk
2. Render confirm page
```

Khi user confirm bằng POST:

```txt
1. Lấy object theo pk
2. Xóa object
3. Redirect tới success_url
```

Vì vậy ta không cần tự viết:

```python
if request.method == "POST":
    task.delete()
    return redirect("task_list")
```

---

## 11. Template cho DeleteView

File:

```txt
templates/tasks/task_confirm_delete.html
```

Ví dụ:

```django
<h1>Delete Task</h1>

<p>Are you sure you want to delete "{{ object }}"?</p>

<form method="post">
    {% csrf_token %}
    <button type="submit">Yes, delete</button>
</form>

<a href="{% url 'task_detail' object.pk %}">Cancel</a>
```

Nếu view có khai báo:

```python
context_object_name = "task"
```

thì template có thể viết:

```django
<p>Are you sure you want to delete "{{ task }}"?</p>

<a href="{% url 'task_detail' task.pk %}">Cancel</a>
```

---

## 12. `fields` và `form_class`

Có 2 cách khai báo form cho `CreateView` và `UpdateView`.

---

### 12.1. Cách 1: Dùng `fields`

```python
class TaskCreateView(CreateView):
    model = Task
    fields = ["title", "description", "is_done"]
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")
```

Django sẽ tự tạo ModelForm dựa trên `fields`.

Cách này nhanh, phù hợp demo hoặc form đơn giản.

---

### 12.2. Cách 2: Dùng `form_class`

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")
```

Cách này nên dùng trong project thực tế vì form được tách riêng trong `forms.py`.

Nên ưu tiên:

```python
form_class = TaskForm
```

khi form cần custom widget, validation, label, help_text, clean method.

---

### 12.3. Không nên dùng đồng thời `fields` và `form_class`

Không nên:

```python
class TaskCreateView(CreateView):
    model = Task
    fields = ["title"]
    form_class = TaskForm
```

Chỉ chọn một trong hai.

Quy tắc:

```txt
Form đơn giản, demo nhanh
→ fields

Project thực tế, form có khả năng mở rộng
→ form_class
```

---

## 13. `success_url` và `reverse_lazy()`

Sau khi create/update/delete thành công, Django cần biết redirect đi đâu.

Ví dụ:

```python
success_url = reverse_lazy("task_list")
```

`reverse_lazy()` dùng để reverse URL name thành URL thật, nhưng thực hiện muộn hơn.

Không nên dùng `reverse()` trực tiếp ở class attribute:

```python
success_url = reverse("task_list")
```

Vì class được import khi Django load URLconf, lúc đó URL resolver có thể chưa sẵn sàng.

Nên dùng:

```python
success_url = reverse_lazy("task_list")
```

Quy tắc:

```txt
Trong class attribute của CBV → dùng reverse_lazy()

Trong method runtime → có thể dùng reverse()
```

---

## 14. URL tổng hợp cho CRUD

```python
# urls.py
from django.urls import path
from .views import (
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]
```

Thông thường project sẽ có thêm:

```python
path("tasks/", TaskListView.as_view(), name="task_list")
path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail")
```

---

## 15. Flow tổng quan

### 15.1. Flow của CreateView

```txt
GET /tasks/create/
    ↓
Tạo form rỗng
    ↓
Render task_form.html

POST /tasks/create/
    ↓
Bind request.POST vào form
    ↓
Validate form
    ↓
Nếu valid: save object
    ↓
Redirect success_url
```

---

### 15.2. Flow của UpdateView

```txt
GET /tasks/1/edit/
    ↓
Lấy object theo pk
    ↓
Tạo form với instance hiện tại
    ↓
Render task_form.html

POST /tasks/1/edit/
    ↓
Lấy object theo pk
    ↓
Bind request.POST vào form với instance hiện tại
    ↓
Validate form
    ↓
Nếu valid: save object
    ↓
Redirect success_url
```

---

### 15.3. Flow của DeleteView

```txt
GET /tasks/1/delete/
    ↓
Lấy object theo pk
    ↓
Render confirm delete page

POST /tasks/1/delete/
    ↓
Lấy object theo pk
    ↓
Delete object
    ↓
Redirect success_url
```

---

## 16. Bảng tổng kết Basic

| View         | Mục đích   | Cần khai báo thường dùng                                            |
| ------------ | ---------- | ------------------------------------------------------------------- |
| `CreateView` | Tạo object | `model`, `form_class` hoặc `fields`, `template_name`, `success_url` |
| `UpdateView` | Sửa object | `model`, `form_class` hoặc `fields`, `template_name`, `success_url` |
| `DeleteView` | Xóa object | `model`, `template_name`, `success_url`                             |

---

# Part 2: Advanced / Mở rộng

## 17. Khi nào cần xem phần Advanced?

Phần Basic đủ dùng khi:

```txt
- Form đơn giản
- Redirect cố định
- Không cần gán user tự động
- Không cần custom permission
- Không cần xử lý logic trước/sau khi save
```

Cần xem phần Advanced khi gặp case như:

```txt
- Gán created_by = request.user khi tạo object
- Chỉ cho user sửa/xóa object của họ
- Redirect về detail page của object vừa tạo
- Thêm success message
- Custom dữ liệu truyền vào form
- Custom form_valid()
- Custom form_invalid()
- Custom get_success_url()
- Custom delete()
```

---

## 18. Gán user hiện tại khi CreateView save

Một case rất thường gặp:

```txt
Khi tạo task, created_by phải là user đang login.
```

Vì `created_by` không nằm trong form, ta cần gán trong `form_valid()`.

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Task
from .forms import TaskForm

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
```

Giải thích:

```python
form.instance.created_by = self.request.user
```

gán user hiện tại vào object trước khi save.

```python
return super().form_valid(form)
```

tiếp tục flow mặc định của `CreateView`, tức là save object và redirect.

---

## 19. `form_valid()` dùng khi nào?

`form_valid()` được gọi khi form đã pass validation.

Dùng `form_valid()` khi cần xử lý logic trước hoặc sau khi save.

Ví dụ thường gặp:

```txt
- Gán user hiện tại
- Gán field mặc định không nằm trong form
- Gửi notification sau khi tạo object
- Ghi activity log
- Thêm success message
```

Ví dụ:

```python
def form_valid(self, form):
    form.instance.created_by = self.request.user
    response = super().form_valid(form)

    # logic sau khi save
    # create_activity_log(self.object)

    return response
```

Lưu ý:

```txt
Sau khi gọi super().form_valid(form), object đã được save và thường có thể truy cập qua self.object.
```

---

## 20. `form_invalid()` dùng khi nào?

`form_invalid()` được gọi khi form không hợp lệ.

Thông thường không cần override.

Chỉ dùng khi muốn custom xử lý khi form lỗi.

Ví dụ log lỗi form:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
```

Quy tắc:

```txt
Form valid → form_valid()

Form invalid → form_invalid()
```

---

## 21. Redirect về detail page sau khi create/update

Thay vì redirect cố định về list:

```python
success_url = reverse_lazy("task_list")
```

ta có thể redirect về detail page của object vừa tạo/sửa.

Dùng `get_success_url()`:

```python
from django.urls import reverse

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse("task_detail", kwargs={
            "pk": self.object.pk,
        })
```

Sau khi form valid, `self.object` là object đã được save.

Với `UpdateView` cũng tương tự:

```python
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse("task_detail", kwargs={
            "pk": self.object.pk,
        })
```

Quy tắc:

```txt
Redirect cố định → success_url

Redirect động theo object hiện tại → get_success_url()
```

---

## 22. Giới hạn user chỉ được sửa task của mình

Với `UpdateView`, nếu chỉ khai báo:

```python
class TaskUpdateView(UpdateView):
    model = Task
```

thì user có thể thử truy cập:

```txt
/tasks/999/edit/
```

Nếu task đó tồn tại, có thể bị sửa nhầm nếu không có permission logic.

Cách xử lý tốt là filter object trong `get_queryset()`:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse("task_detail", kwargs={
            "pk": self.object.pk,
        })
```

Khi đó `UpdateView` chỉ tìm object trong danh sách task của user hiện tại.

Nếu user truy cập task của người khác, Django trả 404.

---

## 23. Giới hạn user chỉ được xóa task của mình

Với `DeleteView` cũng làm tương tự:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
```

Quy tắc:

```txt
Muốn giới hạn object được phép update/delete
→ custom get_queryset()
```

Không nên chỉ ẩn nút sửa/xóa ở frontend.

Backend vẫn phải kiểm tra quyền truy cập.

---

## 24. Thêm success message

Nếu muốn hiển thị message sau khi tạo/sửa/xóa thành công, có thể dùng `SuccessMessageMixin`.

Ví dụ CreateView:

```python
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")
    success_message = "Task was created successfully."
```

UpdateView:

```python
class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")
    success_message = "Task was updated successfully."
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

Lưu ý:

```txt
SuccessMessageMixin thường dùng tốt với CreateView và UpdateView.
Với DeleteView, nếu cần message, có thể custom thêm trong form_valid() hoặc delete flow tùy version/project style.
```

---

## 25. Custom dữ liệu truyền vào form với `get_form_kwargs()`

`get_form_kwargs()` dùng khi form cần nhận thêm dữ liệu ngoài `request.POST`.

Ví dụ form cần biết user hiện tại:

```python
# forms.py
class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = ["title", "description", "is_done"]
```

View:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
```

Dùng khi form cần:

```txt
- user hiện tại
- project hiện tại
- dữ liệu từ URL kwargs
- dữ liệu để filter field choices
```

Ví dụ filter choices theo user trong form.

---

## 26. Thêm context cho form page

Có thể dùng `get_context_data()` giống các CBV khác.

Ví dụ muốn truyền page title:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Task"
        return context
```

UpdateView:

```python
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit Task"
        return context
```

Template:

```django
<h1>{{ page_title }}</h1>
```

---

## 27. Custom DeleteView redirect động

Với `DeleteView`, nhiều lúc redirect cần phụ thuộc object hiện tại.

Ví dụ task thuộc project, sau khi xóa task thì redirect về detail của project.

Model giả sử:

```python
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
```

View:

```python
from django.urls import reverse
from django.views.generic import DeleteView

class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def get_success_url(self):
        return reverse("project_detail", kwargs={
            "pk": self.object.project.pk,
        })
```

Lưu ý:

```txt
Cần đảm bảo self.object còn truy cập được thông tin cần thiết trước/sau khi delete tùy flow Django version.
Nếu logic phức tạp, có thể lưu project_pk trước khi gọi delete.
```

Ví dụ an toàn hơn:

```python
class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def form_valid(self, form):
        self.project_pk = self.object.project.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_detail", kwargs={
            "pk": self.project_pk,
        })
```

---

## 28. Custom DeleteView logic trước khi xóa

Nếu cần ghi log trước khi xóa:

```python
class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        # Ghi log trước khi object bị xóa
        # create_activity_log(self.request.user, self.object)

        return super().form_valid(form)
```

Dùng khi cần:

```txt
- Ghi activity log
- Gửi notification
- Lưu thông tin object trước khi xóa
```

---

## 29. Dùng `get_initial()` để set giá trị mặc định

`get_initial()` dùng để truyền initial data cho form.

Ví dụ khi tạo task, mặc định `is_done = False`:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_initial(self):
        initial = super().get_initial()
        initial["is_done"] = False
        return initial
```

Ví dụ lấy dữ liệu từ query params:

```python
def get_initial(self):
    initial = super().get_initial()
    title = self.request.GET.get("title")

    if title:
        initial["title"] = title

    return initial
```

URL:

```txt
/tasks/create/?title=Learn Django
```

Form sẽ được fill sẵn title.

---

## 30. Dùng `get_form_class()` khi muốn chọn form động

Ví dụ user thường dùng form khác, admin dùng form khác:

```python
class TaskCreateView(CreateView):
    model = Task
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminTaskForm

        return TaskForm
```

Dùng khi:

```txt
- Form phụ thuộc user role
- Form phụ thuộc loại object
- Form phụ thuộc query params
```

Nếu không cần form động, cứ dùng:

```python
form_class = TaskForm
```

---

## 31. Dùng `get_template_names()` khi muốn chọn template động

Ví dụ staff dùng template khác:

```python
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm

    def get_template_names(self):
        if self.request.user.is_staff:
            return ["tasks/staff_task_form.html"]

        return ["tasks/task_form.html"]
```

Dùng khi template cần thay đổi theo điều kiện.

Nếu không cần động, nên dùng:

```python
template_name = "tasks/task_form.html"
```

---

## 32. CreateView không nhất thiết cần `model` nếu có `form_class`

Nếu `form_class` là `ModelForm`, nhiều lúc Django có thể suy ra model từ form.

Ví dụ:

```python
class TaskCreateView(CreateView):
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")
```

Tuy nhiên, khi mới học hoặc viết docs nội bộ, nên khai báo rõ:

```python
model = Task
form_class = TaskForm
```

để người đọc dễ hiểu.

---

## 33. Dùng `get_queryset()` cho UpdateView và DeleteView

`UpdateView` và `DeleteView` đều cần lấy object.

Vì vậy có thể dùng `get_queryset()` để giới hạn object.

Ví dụ chỉ update task chưa hoàn thành:

```python
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_queryset(self):
        return Task.objects.filter(is_done=False)
```

Ví dụ chỉ xóa task của user hiện tại:

```python
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
```

Đây là cách rất quan trọng để bảo vệ dữ liệu.

---

## 34. Full example thực tế

```python
# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_message = "Task was created successfully."

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("task_detail", kwargs={
            "pk": self.object.pk,
        })


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    context_object_name = "task"
    success_message = "Task was updated successfully."

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse("task_detail", kwargs={
            "pk": self.object.pk,
        })


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    context_object_name = "task"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
```

URL:

```python
# urls.py
from django.urls import path
from .views import (
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]
```

---

## 35. Lỗi thường gặp

### 35.1. Quên `success_url`

Sai:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
```

Nếu model không có `get_absolute_url()`, có thể lỗi vì Django không biết redirect đi đâu.

Đúng:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_list")
```

Hoặc dùng:

```python
def get_success_url(self):
    return reverse("task_detail", kwargs={"pk": self.object.pk})
```

---

### 35.2. Dùng `reverse()` ở class attribute

Không nên:

```python
success_url = reverse("task_list")
```

Nên:

```python
success_url = reverse_lazy("task_list")
```

---

### 35.3. Dùng cả `fields` và `form_class`

Sai:

```python
class TaskCreateView(CreateView):
    model = Task
    fields = ["title"]
    form_class = TaskForm
```

Đúng:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
```

hoặc:

```python
class TaskCreateView(CreateView):
    model = Task
    fields = ["title"]
```

---

### 35.4. Quên gán user khi field không nằm trong form

Model có:

```python
created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

Form không có `created_by`.

Nếu không gán:

```python
form.instance.created_by = self.request.user
```

khi save có thể lỗi vì thiếu required field.

---

### 35.5. Chỉ ẩn nút edit/delete ở template nhưng không check backend

Không đủ an toàn:

```django
{% if task.created_by == request.user %}
    <a href="{% url 'task_update' task.pk %}">Edit</a>
{% endif %}
```

Vẫn phải check backend:

```python
def get_queryset(self):
    return Task.objects.filter(created_by=self.request.user)
```

---

### 35.6. Delete bằng GET

Không nên xóa object bằng GET.

Không nên:

```python
def get(self, request, *args, **kwargs):
    self.get_object().delete()
    return redirect("task_list")
```

Nên dùng flow mặc định của `DeleteView`:

```txt
GET → hiển thị confirm page
POST → delete object
```

---

## 36. Bảng tổng kết method/attribute nâng cao

| Method / Attribute     | Dùng trong                               | Vai trò                             |
| ---------------------- | ---------------------------------------- | ----------------------------------- |
| `form_valid()`         | `CreateView`, `UpdateView`               | Xử lý khi form hợp lệ               |
| `form_invalid()`       | `CreateView`, `UpdateView`               | Xử lý khi form lỗi                  |
| `get_success_url()`    | `CreateView`, `UpdateView`, `DeleteView` | Redirect động                       |
| `get_queryset()`       | `UpdateView`, `DeleteView`               | Giới hạn object được phép sửa/xóa   |
| `get_form_kwargs()`    | `CreateView`, `UpdateView`               | Truyền thêm dữ liệu vào form        |
| `get_initial()`        | `CreateView`, `UpdateView`               | Set giá trị mặc định cho form       |
| `get_form_class()`     | `CreateView`, `UpdateView`               | Chọn form động                      |
| `get_context_data()`   | `CreateView`, `UpdateView`, `DeleteView` | Thêm context cho template           |
| `get_template_names()` | `CreateView`, `UpdateView`, `DeleteView` | Chọn template động                  |
| `success_url`          | CRUD views                               | Redirect cố định sau khi thành công |
| `SuccessMessageMixin`  | Thường dùng với create/update            | Hiển thị message thành công         |

---

## 37. Nên dùng cách nào trong thực tế?

Với `CreateView`:

```txt
Create đơn giản
→ model + form_class + template_name + success_url

Cần gán user hoặc field tự động
→ override form_valid()

Redirect theo object vừa tạo
→ override get_success_url()

Form cần user/project hiện tại
→ override get_form_kwargs()
```

Với `UpdateView`:

```txt
Update đơn giản
→ model + form_class + template_name + success_url

Chỉ cho sửa object của user
→ override get_queryset()

Redirect về detail object
→ override get_success_url()

Cần thêm context
→ override get_context_data()
```

Với `DeleteView`:

```txt
Delete đơn giản
→ model + template_name + success_url

Chỉ cho xóa object của user
→ override get_queryset()

Redirect động sau khi xóa
→ override get_success_url()

Cần log trước khi xóa
→ override form_valid()
```

---

## 38. Kết luận

`CreateView`, `UpdateView`, `DeleteView` giúp xử lý CRUD nhanh hơn rất nhiều so với FBV.

Cách nhớ:

```txt
CreateView = tạo object

UpdateView = sửa object

DeleteView = xóa object
```

Với create/update, Django xử lý sẵn:

```txt
GET form
POST form
Validate
Save
Redirect
Render errors
```

Với delete, Django xử lý sẵn:

```txt
GET confirm page
POST delete
Redirect
```

Khi cần custom, thường override:

```txt
form_valid()
get_success_url()
get_queryset()
get_form_kwargs()
get_context_data()
```

---

## 39. Ghi nhớ nhanh

```txt
CreateView dùng để tạo object.

UpdateView dùng để sửa object.

DeleteView dùng để xóa object.

form_class dùng khi có ModelForm riêng.

fields dùng cho form đơn giản.

Không dùng đồng thời fields và form_class.

success_url dùng redirect cố định.

reverse_lazy() dùng ở class attribute.

get_success_url() dùng redirect động.

form_valid() dùng khi form hợp lệ.

get_queryset() dùng để giới hạn object được phép sửa/xóa.

DeleteView nên xóa bằng POST, không xóa bằng GET.
```

---
