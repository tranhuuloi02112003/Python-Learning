# 01. Overview Class-based Views

## 1. Mục tiêu

Sau khi đọc phần này, cần hiểu được:

- Class-based view là gì
- Vì sao Django có class-based view
- Class-based view giải quyết vấn đề gì
- Khi nào nên dùng class-based view
- Khi nào nên dùng function-based view
- Class-based view khác gì với function-based view ở mức tổng quan

---

## 2. View trong Django là gì?

Trong Django, **view** là nơi nhận request từ user và trả về response.

Ví dụ:

```python
from django.http import HttpResponse

def hello_view(request):
    return HttpResponse("Hello Django")
```

Khi user truy cập một URL, Django sẽ tìm view tương ứng trong `urls.py`, gọi view đó, truyền vào `request`, sau đó view trả về `HttpResponse`.

Nói đơn giản:

```text
User request
    ↓
URL pattern
    ↓
View
    ↓
Response
```

Theo Django docs, một view là một callable nhận `request` và trả về response. Callable này không nhất thiết phải là function, nên Django cho phép dùng class để viết view.

---

## 3. Function-based view là gì?

Function-based view, viết tắt là **FBV**, là cách viết view bằng function.

Ví dụ:

```python
from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
    })
```

Đây là cách dễ hiểu nhất khi mới học Django.

Một function nhận `request`, xử lý logic, rồi return response.

---

## 4. Class-based view là gì?

Class-based view, viết tắt là **CBV**, là cách viết view bằng class Python thay vì function.

Ví dụ:

```python
from django.http import HttpResponse
from django.views import View

class HelloView(View):
    def get(self, request):
        return HttpResponse("Hello Django")
```

Trong `urls.py`:

```python
from django.urls import path
from .views import HelloView

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
]
```

Điểm quan trọng:

```python
HelloView.as_view()
```

Vì Django URL cần một callable giống function, nên class-based view phải dùng `.as_view()` để biến class thành một view có thể được Django gọi.

---

## 5. Vì sao cần class-based view?

Function-based view rất dễ hiểu, nhưng khi view bắt đầu phức tạp, code dễ bị dài.

Ví dụ một view vừa xử lý GET vừa xử lý POST:

```python
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

View này vẫn đúng, nhưng có một vấn đề:

GET logic và POST logic đang nằm chung trong một function.

Nếu sau này view có thêm permission, validate, save, send notification, custom context, custom redirect, thì function sẽ ngày càng dài.

Class-based view giúp tách logic theo HTTP method:

```python
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

Ở đây:

```python
def get(self, request):
```

xử lý khi user mở trang.

```python
def post(self, request):
```

xử lý khi user submit form.

---

## 6. Class-based view giải quyết vấn đề gì?

Class-based view giúp giải quyết các vấn đề chính sau:

### 6.1. Tách logic theo HTTP method

Thay vì viết:

```python
if request.method == "POST":
    ...
else:
    ...
```

CBV cho phép viết:

```python
def get(self, request):
    ...

def post(self, request):
    ...
```

Code dễ đọc hơn khi view có nhiều logic.

### 6.2. Tái sử dụng code tốt hơn

Vì CBV là class, nên có thể dùng:

- inheritance
- mixin
- override method
- class attributes

Ví dụ nhiều view cần login:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
```

Thay vì mỗi view đều tự check user đã login hay chưa.

### 6.3. Tận dụng generic views có sẵn của Django

Django cung cấp sẵn nhiều class-based generic views cho các case phổ biến.

Ví dụ:

| Generic view | Mục đích |
| --- | --- |
| `TemplateView` | Render một template |
| `RedirectView` | Redirect URL |
| `ListView` | Hiển thị danh sách object |
| `DetailView` | Hiển thị chi tiết object |
| `CreateView` | Tạo object |
| `UpdateView` | Sửa object |
| `DeleteView` | Xóa object |
| `FormView` | Xử lý form custom |

Django docs nói tất cả class-based views đều kế thừa từ `View`; `View` xử lý việc liên kết view với URL, dispatch HTTP method và các tính năng chung khác. Ngoài ra `TemplateView` dùng để render template, còn `RedirectView` dùng để redirect HTTP.

Ví dụ `TemplateView`:

```python
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"
```

Trong `urls.py`:

```python
from django.urls import path
from .views import AboutView

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
]
```

---

## 7. So sánh nhanh FBV và CBV

### Function-based view

```python
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
    })
```

Ưu điểm:

- Dễ hiểu
- Dễ debug
- Phù hợp với view đơn giản
- Luồng xử lý rõ ràng từ trên xuống dưới

Nhược điểm:

- Khi logic nhiều, function dễ dài
- Khó tái sử dụng logic giữa nhiều view
- GET, POST, permission, context, form handling dễ bị gom chung

### Class-based view

```python
from django.views.generic import ListView

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
```

Ưu điểm:

- Tách logic tốt hơn
- Dễ tái sử dụng bằng inheritance và mixin
- Có nhiều generic views giúp viết CRUD nhanh
- Phù hợp với app có nhiều màn hình list, detail, create, update, delete

Nhược điểm:

- Khó hiểu hơn lúc mới học
- Phải hiểu `.as_view()`, `dispatch()`, `get_queryset()`, `get_context_data()`
- Nếu lạm dụng mixin hoặc override quá nhiều method, code có thể khó đọc

---

## 8. Khi nào nên dùng function-based view?

Nên dùng FBV khi view đơn giản.

Ví dụ:

```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "ok",
    })
```

Hoặc:

```python
from django.shortcuts import render

def dashboard(request):
    stats = get_dashboard_stats()

    return render(request, "dashboard.html", {
        "stats": stats,
    })
```

Nên dùng FBV khi:

- View ngắn
- Logic đơn giản
- Không cần tái sử dụng nhiều
- Không cần CRUD generic
- Muốn code rõ ràng, đọc từ trên xuống dưới

---

## 9. Khi nào nên dùng class-based view?

Nên dùng CBV khi:

- View có cả GET và POST
- Có nhiều CRUD: list, detail, create, update, delete
- Muốn tái sử dụng logic bằng mixin
- Muốn tận dụng generic views của Django
- App có nhiều màn hình quản lý object

Ví dụ app Todo/Task Manager:

| Màn hình | View phù hợp |
| --- | --- |
| Task list | `ListView` |
| Task detail | `DetailView` |
| Task create | `CreateView` |
| Task update | `UpdateView` |
| Task delete | `DeleteView` |
| Project list | `ListView` |
| Project detail | `DetailView` |
| Project create | `CreateView` |
| Project update | `UpdateView` |
| Project delete | `DeleteView` |

Với các case này, CBV thường giúp code ngắn hơn và có cấu trúc hơn.

---

## 10. Ví dụ tổng quan với Task

### Function-based view

```python
from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
    })
```

### Class-based view

```python
from django.views.generic import ListView
from .models import Task

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
```

### URL

```python
from django.urls import path
from .views import TaskListView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task_list"),
]
```

Ở ví dụ này, `ListView` đã xử lý sẵn việc lấy danh sách object và render template.

---

## 11. Cách hiểu đơn giản nhất

Có thể hiểu ngắn gọn như sau:

- FBV = tự viết toàn bộ logic view bằng function
- CBV = viết view bằng class, chia logic thành method
- Generic CBV = Django viết sẵn nhiều class view cho các case phổ biến

Ví dụ:

| Muốn làm gì? | Dùng gì? |
| --- | --- |
| Muốn render page tĩnh | `TemplateView` |
| Muốn redirect | `RedirectView` |
| Muốn hiển thị danh sách | `ListView` |
| Muốn hiển thị chi tiết | `DetailView` |
| Muốn tạo object | `CreateView` |
| Muốn sửa object | `UpdateView` |
| Muốn xóa object | `DeleteView` |
| Muốn xử lý form custom | `FormView` |

---

## 12. Kết luận

Class-based view là cách tổ chức view bằng class trong Django.

Nó không thay thế hoàn toàn function-based view.

Thay vào đó, CBV phù hợp khi view có cấu trúc rõ ràng, có nhiều logic tái sử dụng, hoặc làm CRUD nhiều.

Quy tắc thực tế:

- View đơn giản → dùng function-based view
- CRUD hoặc form/model nhiều → dùng class-based generic view
- Logic GET/POST rõ ràng, cần tách method → dùng `View` hoặc generic CBV

---

## 13. Ghi nhớ nhanh

- View = nhận request, trả response
- FBV = function nhận request, trả response
- CBV = class có method `get()`, `post()`, ... để xử lý request
- `as_view()` = biến class thành callable để Django URL gọi được
- Generic View = class view Django viết sẵn cho các case phổ biến
- Mixin = class nhỏ để tái sử dụng behavior như login, permission
