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

## 4. Bốn case còn lại: Detail, Create, Update, Delete

Case 1 ở trên đã cho thấy đủ ba mức tư duy (FBV → CBV cơ bản → Generic CBV).
Bốn case còn lại đi theo **đúng khuôn đó**, chỉ đổi generic view và phần việc Django làm thay.
Nên ở đây chỉ tóm tắt; code đầy đủ nằm ở bài 05 và 06.

| Case | FBV mình phải tự làm | Generic CBV | Django làm thay | Chi tiết |
| --- | --- | --- | --- | --- |
| Detail | `get_object_or_404(Task, pk=pk)`, tạo context, render | `DetailView` | Lấy object theo `pk`/`slug`, đặt vào context, render | `05-listview-and-detailview.md` |
| Create | Tạo form rỗng khi GET, bind `request.POST` khi POST, `is_valid()`, `save()`, `redirect()` | `CreateView` | Toàn bộ flow GET/POST + form + save + redirect | `06-createview-updateview-deleteview.md` |
| Update | Lấy object, bind form với `instance=`, `is_valid()`, `save()`, `redirect()` | `UpdateView` | Lấy object + bind instance + save + redirect | `06-createview-updateview-deleteview.md` |
| Delete | Lấy object, render trang confirm khi GET, `delete()` khi POST, `redirect()` | `DeleteView` | Trang confirm + xóa + redirect | `06-createview-updateview-deleteview.md` |

### Điểm móc nối cần nhớ

Ở cả bốn case, câu hỏi luôn là *"muốn đổi hành vi mặc định thì override method nào?"*:

| Muốn đổi | Override |
| --- | --- |
| Cách lấy object (theo `slug`, theo owner...) | `get_object()` |
| Can thiệp trước khi `save()` (gán `request.user`...) | `form_valid()` |
| Trang redirect sau khi thành công | `get_success_url()`, hoặc khai `success_url = reverse_lazy(...)` |

> Bài 05 và 06 đều mở đầu mỗi generic view bằng mục **"Function-based view tương đương"**,
> nên bản FBV của từng case vẫn có đầy đủ ở đó — không cần chép lại tại đây.

## 5. Bảng tổng kết: FBV tự làm gì, CBV làm thay gì?

| Bài toán | FBV mình tự làm | Generic CBV làm thay |
| --- | --- | --- |
| List object | Query object, tạo context, render | `ListView` gọi `get_queryset()`, tạo context, render |
| Detail object | `get_object_or_404()` | `DetailView` gọi `get_object()` |
| Create object | Tạo form, validate, save, redirect | `CreateView` xử lý GET/POST/form/save |
| Update object | Lấy object, bind form với instance, save | `UpdateView` xử lý object + form |
| Delete object | Lấy object, confirm, delete, redirect | `DeleteView` xử lý confirm + delete |

---

## 6. Nhìn theo mức độ tự động hóa

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

## 7. Cách chọn thực tế

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

## 8. Kết luận

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

---

**Điều hướng:** ← `01-overview-class-based-views.md` · `00-lo-trinh-doc.md` · `03-view-as-view-dispatch-get-post.md` →
