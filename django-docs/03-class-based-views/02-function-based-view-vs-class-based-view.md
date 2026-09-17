# 02. Function-based View vs Class-based View

## 1. Mục tiêu

Mục tiêu của phần này là so sánh cùng một bài toán khi viết bằng:

- Function-based view
- Class-based view cơ bản
- Generic class-based view

Qua đó hiểu được:

- Với FBV, mình phải tự xử lý những gì
- Với CBV, Django xử lý thay mình những gì
- Generic CBV hoạt động như thế nào ở mức thực tế
- Khi nào dùng FBV sẽ rõ ràng hơn
- Khi nào dùng CBV sẽ gọn và dễ maintain hơn

---

## 2. Model ví dụ dùng chung

Trong các ví dụ bên dưới, giả sử ta có model `Task`:

```python
# models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

Và form:

```python
# forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "is_done"]
```

---

## 3. Case 1: Hiển thị danh sách Task

### 3.1. Bài toán

User truy cập:

```text
/tasks/
```

Hệ thống hiển thị danh sách task.

### 3.2. Viết bằng Function-based View

```python
# views.py
from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
    })
```

URL:

```python
# urls.py
from django.urls import path
from .views import task_list

urlpatterns = [
    path("tasks/", task_list, name="task_list"),
]
```

### 3.3. FBV đang tự xử lý những gì?

Với FBV, mình tự làm toàn bộ các bước:

1. Nhận request
2. Query danh sách task bằng `Task.objects.all()`
3. Tạo context `{"tasks": tasks}`
4. Chỉ định template `"tasks/task_list.html"`
5. Gọi `render()`
6. Trả response về cho user

Nghĩa là ta kiểm soát trực tiếp từng bước.

### 3.4. Viết bằng Class-based View cơ bản

```python
# views.py
from django.views import View
from django.shortcuts import render
from .models import Task

class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all()

        return render(request, "tasks/task_list.html", {
            "tasks": tasks,
        })
```

URL:

```python
# urls.py
from django.urls import path
from .views import TaskListView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task_list"),
]
```

### 3.5. CBV cơ bản khác gì FBV?

Ở bản này, logic vẫn gần giống FBV.

Điểm khác là request GET được tách vào method:

```python
def get(self, request):
```

Thay vì viết function trực tiếp:

```python
def task_list(request):
```

CBV cơ bản chưa giúp giảm code nhiều, nhưng giúp tách rõ logic theo HTTP method.

### 3.6. Viết bằng Generic CBV: `ListView`

```python
# views.py
from django.views.generic import ListView
from .models import Task

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
```

URL:

```python
# urls.py
from django.urls import path
from .views import TaskListView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task_list"),
]
```

### 3.7. `ListView` đang làm thay mình những gì?

Khi dùng `ListView`, Django tự xử lý:

1. Nhận request GET
2. Gọi `get_queryset()`
3. Mặc định `get_queryset()` lấy `Task.objects.all()`
4. Tạo context cho template
5. Vì `context_object_name = "tasks"`, template sẽ dùng biến `tasks`
6. Render `template_name`
7. Trả response

Nghĩa là với `ListView`, ta không cần tự viết:

```python
tasks = Task.objects.all()

return render(request, "tasks/task_list.html", {
    "tasks": tasks,
})
```

Django đã làm phần đó thông qua `ListView`.

### 3.8. Nếu muốn custom queryset thì sao?

Ví dụ chỉ lấy task chưa hoàn thành:

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(is_done=False)
```

Điểm quan trọng:

```python
def get_queryset(self):
```

là method dùng để quyết định danh sách object nào sẽ được hiển thị.

### 3.9. Tổng kết case List

FBV:
Mình tự query, tự tạo context, tự render.

CBV cơ bản:
Tách logic GET vào method `get()`, nhưng vẫn tự query và render.

`ListView`:
Django tự query, tự tạo context, tự render.
Mình chỉ cấu hình `model`, `template_name`, `context_object_name`.

---

## 4. Case 2: Hiển thị chi tiết một Task

### 4.1. Bài toán

User truy cập:

```text
/tasks/1/
```

Hệ thống hiển thị chi tiết task có `id = 1`.

### 4.2. Viết bằng Function-based View

```python
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Task

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    return render(request, "tasks/task_detail.html", {
        "task": task,
    })
```

URL:

```python
# urls.py
from django.urls import path
from .views import task_detail

urlpatterns = [
    path("tasks/<int:pk>/", task_detail, name="task_detail"),
]
```

### 4.3. FBV đang tự xử lý những gì?

Với FBV, mình tự làm:

1. Nhận `pk` từ URL
2. Gọi `get_object_or_404(Task, pk=pk)`
3. Nếu object tồn tại thì render template
4. Nếu object không tồn tại thì trả `404`
5. Tự tạo context `{"task": task}`
6. Tự gọi `render()`

Phần quan trọng nhất là:

```python
task = get_object_or_404(Task, pk=pk)
```

Mình tự viết logic lấy object.

### 4.4. Viết bằng Generic CBV: `DetailView`

```python
# views.py
from django.views.generic import DetailView
from .models import Task

class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
```

URL:

```python
# urls.py
from django.urls import path
from .views import TaskDetailView

urlpatterns = [
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
]
```

### 4.5. `DetailView` đang làm thay mình những gì?

Khi user truy cập:

```text
/tasks/1/
```

`DetailView` sẽ tự xử lý:

1. Nhận `pk` từ URL
2. Đọc `pk` từ `self.kwargs`
3. Gọi `get_queryset()`
4. Gọi `get_object()`
5. Tìm object `Task` có `pk` tương ứng
6. Nếu không tìm thấy thì trả `404`
7. Tạo context
8. Render `template_name`

Vì vậy ta không cần tự viết:

```python
get_object_or_404(Task, pk=pk)
```

`DetailView` đã có sẵn logic lấy object.

### 4.6. Nếu muốn custom object lookup thì sao?

Mặc định `DetailView` lấy object theo `pk`.

Nếu URL dùng `slug`:

```python
# urls.py
path("tasks/<slug:slug>/", TaskDetailView.as_view(), name="task_detail")
```

Thì view có thể viết:

```python
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    slug_field = "slug"
    slug_url_kwarg = "slug"
```

Khi đó `DetailView` sẽ lấy object theo `slug` thay vì `pk`.

### 4.7. Tổng kết case Detail

FBV:
Mình tự lấy object bằng `get_object_or_404()`.

`DetailView`:
Django tự lấy object bằng `get_object()`.
Mặc định object được lấy theo `pk` trong URL.

---

## 5. Case 3: Tạo mới Task

### 5.1. Bài toán

User truy cập:

```text
/tasks/create/
```

Nếu GET:

Hiển thị form tạo task.

Nếu POST:

Validate form, lưu task, redirect.

### 5.2. Viết bằng Function-based View

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

URL:

```python
# urls.py
from django.urls import path
from .views import task_create

urlpatterns = [
    path("tasks/create/", task_create, name="task_create"),
]
```

### 5.3. FBV đang tự xử lý những gì?

Với FBV, mình tự làm:

1. Kiểm tra `request.method`
2. Nếu GET thì tạo form rỗng
3. Nếu POST thì bind dữ liệu `request.POST` vào form
4. Kiểm tra `form.is_valid()`
5. Nếu valid thì `form.save()`
6. Redirect về `task_list`
7. Nếu invalid thì render lại form kèm lỗi

Code này rõ ràng, nhưng lặp lại khá nhiều ở các form create khác.

### 5.4. Viết bằng CBV cơ bản

```python
# views.py
from django.views import View
from django.shortcuts import render, redirect
from .forms import TaskForm

class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()

        return render(request, "tasks/task_form.html", {
            "form": form,
        })

    def post(self, request):
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("task_list")

        return render(request, "tasks/task_form.html", {
            "form": form,
        })
```

Ở bản này, GET và POST được tách rõ hơn:

- GET -> `get()`
- POST -> `post()`

Nhưng logic tạo form, validate, save, redirect vẫn tự viết.

### 5.5. Viết bằng Generic CBV: `CreateView`

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

### 5.6. `CreateView` đang làm thay mình những gì?

`CreateView` tự xử lý:

Khi GET:
1. Tạo form rỗng
2. Render template

Khi POST:
1. Bind `request.POST` vào form
2. Validate form
3. Nếu form hợp lệ thì save object
4. Redirect tới `success_url`
5. Nếu form lỗi thì render lại template kèm lỗi

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

### 5.7. Vì sao dùng `reverse_lazy()`?

Trong CBV, thường dùng:

```python
success_url = reverse_lazy("task_list")
```

thay vì:

```python
success_url = reverse("task_list")
```

Lý do đơn giản:

`reverse_lazy()` chỉ resolve URL khi cần dùng.

Điều này an toàn hơn khi khai báo URL ở class level.

### 5.8. Nếu muốn can thiệp trước khi save thì sao?

Ví dụ muốn gán user hiện tại cho task:

```python
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
```

Điểm quan trọng:

```python
def form_valid(self, form):
```

được gọi khi form hợp lệ.

Nếu muốn thêm logic trước khi object được lưu, thường override `form_valid()`.

### 5.9. Tổng kết case Create

FBV:
Mình tự kiểm tra GET/POST, tự tạo form, tự validate, tự save, tự redirect.

CBV cơ bản:
Tách GET/POST thành `get()` và `post()`, nhưng vẫn tự xử lý form.

`CreateView`:
Django tự xử lý toàn bộ flow form create.
Mình chỉ cấu hình `model`, `form_class`, `template_name`, `success_url`.

---

## 6. Case 4: Cập nhật Task

### 6.1. Bài toán

User truy cập:

```text
/tasks/1/edit/
```

Nếu GET:

Hiển thị form với dữ liệu task hiện tại.

Nếu POST:

Validate form, cập nhật task, redirect.

### 6.2. Viết bằng Function-based View

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

### 6.3. FBV đang tự xử lý những gì?

Với FBV, mình tự làm:

1. Lấy task theo `pk`
2. Nếu không có task thì trả `404`
3. Nếu GET thì tạo form với `instance=task`
4. Nếu POST thì bind `request.POST` với `instance=task`
5. Validate form
6. Save object đã update
7. Redirect
8. Nếu lỗi thì render lại form

### 6.4. Viết bằng Generic CBV: `UpdateView`

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
path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_update")
```

### 6.5. `UpdateView` đang làm thay mình những gì?

`UpdateView` tự xử lý:

1. Lấy object theo `pk`
2. Nếu không tìm thấy thì trả `404`
3. Nếu GET thì tạo form với instance hiện tại
4. Nếu POST thì bind dữ liệu mới vào form
5. Validate form
6. Save object đã update
7. Redirect tới `success_url`
8. Nếu form lỗi thì render lại template

Vì vậy ta không cần tự viết:

```python
task = get_object_or_404(Task, pk=pk)
form = TaskForm(request.POST, instance=task)
```

### 6.6. Tổng kết case Update

FBV:
Mình tự lấy object, tự bind form với instance, tự save.

`UpdateView`:
Django tự lấy object, tự tạo form với instance, tự validate, tự save.

---

## 7. Case 5: Xóa Task

### 7.1. Bài toán

User truy cập:

```text
/tasks/1/delete/
```

Nếu GET:

Hiển thị màn confirm delete.

Nếu POST:

Xóa task và redirect.

### 7.2. Viết bằng Function-based View

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

### 7.3. FBV đang tự xử lý những gì?

Với FBV, mình tự làm:

1. Lấy task theo `pk`
2. Nếu không có task thì trả `404`
3. Nếu GET thì render confirm page
4. Nếu POST thì gọi `task.delete()`
5. Redirect về `task_list`

### 7.4. Viết bằng Generic CBV: `DeleteView`

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
path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete")
```

### 7.5. `DeleteView` đang làm thay mình những gì?

`DeleteView` tự xử lý:

1. Lấy object theo `pk`
2. Nếu không tìm thấy thì trả `404`
3. Nếu GET thì render confirm page
4. Nếu POST thì xóa object
5. Redirect tới `success_url`

### 7.6. Tổng kết case Delete

FBV:
Mình tự lấy object, tự check POST, tự gọi `delete()`.

`DeleteView`:
Django tự lấy object, tự xử lý confirm page, tự delete khi POST.

---

## 8. Bảng tổng kết: FBV tự làm gì, CBV làm thay gì?

| Bài toán | FBV mình tự làm | Generic CBV làm thay |
| --- | --- | --- |
| List object | Query object, tạo context, render | `ListView` gọi `get_queryset()`, tạo context, render |
| Detail object | `get_object_or_404()` | `DetailView` gọi `get_object()` |
| Create object | Tạo form, validate, save, redirect | `CreateView` xử lý GET/POST/form/save |
| Update object | Lấy object, bind form với instance, save | `UpdateView` xử lý object + form |
| Delete object | Lấy object, confirm, delete, redirect | `DeleteView` xử lý confirm + delete |

---

## 9. Nhìn theo mức độ tự động hóa

Có thể hiểu theo 3 mức:

### Mức 1: Function-based View

Mình tự viết gần như toàn bộ flow.

Phù hợp khi logic đơn giản hoặc rất custom.

### Mức 2: Class-based View cơ bản

Mình vẫn tự viết logic, nhưng tách theo method `get()`, `post()`.

Phù hợp khi muốn tách HTTP method rõ ràng nhưng chưa muốn dùng generic view.

### Mức 3: Generic Class-based View

Django viết sẵn flow phổ biến.
Mình chỉ cấu hình và override khi cần.

Phù hợp với CRUD, form, list/detail object.

---

## 10. Cách chọn thực tế

Nên dùng FBV khi:

- View ngắn
- Logic custom đặc biệt
- Không phải CRUD tiêu chuẩn
- Viết bằng function dễ đọc hơn

Nên dùng generic CBV khi:

- View thuộc dạng list/detail/create/update/delete
- Form xử lý theo flow phổ biến
- Muốn code ngắn hơn
- Muốn tận dụng logic có sẵn của Django

Nên dùng CBV cơ bản khi:

- Muốn tách GET/POST rõ ràng
- Logic không hoàn toàn khớp với generic view
- Nhưng vẫn muốn tổ chức bằng class

---

## 11. Kết luận

Điểm khác biệt quan trọng không phải là cú pháp function hay class.

Điểm quan trọng là:

FBV: mình tự điều khiển toàn bộ flow.

Generic CBV: Django đã viết sẵn flow phổ biến, mình chỉ cấu hình hoặc override phần cần thay đổi.

Vì vậy, khi học CBV, cần luôn hỏi:

- Class này đang làm thay mình việc gì?
- Nếu muốn thay đổi hành vi mặc định, mình cần override method nào?

Ví dụ:

| Class view | Method thường override |
| --- | --- |
| `ListView` | `get_queryset()` |
| `DetailView` | `get_object()` nếu cần custom cách lấy object |
| `CreateView` | `form_valid()` nếu cần can thiệp trước khi save |
| `UpdateView` | `form_valid()` nếu cần custom update |
| `DeleteView` | `get_success_url()` nếu cần redirect động |
