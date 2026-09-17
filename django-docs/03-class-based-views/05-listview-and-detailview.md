# 05. ListView and DetailView

## 1. Mục tiêu

File này học về 2 generic class-based views rất thường dùng trong Django:

```txt
ListView
DetailView
```

File được chia thành 2 phần:

```txt
Part 1: Basic
Dùng khi chỉ cần hiển thị danh sách object hoặc chi tiết object theo cách thông thường.

Part 2: Advanced / Mở rộng
Dùng khi cần custom queryset, filter, pagination, context, slug, get_object, tối ưu query.
```

Cách đọc đề xuất:

```txt
Nếu mới học hoặc chỉ cần dùng cơ bản:
Đọc Part 1.

Nếu gặp case mặc định không xử lý được:
Xem Part 2.
```

---

# Part 1: Basic

## 2. Model ví dụ dùng chung

Giả sử ta có model `Task`:

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

---

## 3. ListView là gì?

`ListView` dùng để hiển thị danh sách object.

Ví dụ:

```txt
/tasks/
```

hiển thị danh sách task.

Các case thường dùng `ListView`:

```txt
- Danh sách task
- Danh sách project
- Danh sách user
- Danh sách bài viết
- Danh sách sản phẩm
```

Nói ngắn gọn:

```txt
ListView = dùng khi muốn hiển thị nhiều object
```

---

## 4. DetailView là gì?

`DetailView` dùng để hiển thị chi tiết một object.

Ví dụ:

```txt
/tasks/1/
```

hiển thị chi tiết task có id là `1`.

Các case thường dùng `DetailView`:

```txt
- Chi tiết task
- Chi tiết project
- Chi tiết user
- Chi tiết bài viết
- Chi tiết sản phẩm
```

Nói ngắn gọn:

```txt
DetailView = dùng khi muốn hiển thị một object cụ thể
```

---

## 5. ListView cơ bản

### 5.1. Function-based view tương đương

Nếu viết bằng FBV:

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

Ở đây mình tự làm:

```txt
1. Query Task.objects.all()
2. Tạo context {"tasks": tasks}
3. Render template
4. Trả response
```

---

### 5.2. Viết bằng ListView

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

---

### 5.3. ListView đang làm thay mình những gì?

Khi user truy cập:

```txt
/tasks/
```

`ListView` tự làm:

```txt
1. Nhận request GET
2. Lấy danh sách object từ model Task
3. Tạo context
4. Render template_name
5. Trả response
```

Vì có:

```python
model = Task
```

nên mặc định `ListView` hiểu là cần lấy:

```python
Task.objects.all()
```

Vì có:

```python
context_object_name = "tasks"
```

nên trong template có thể dùng:

```django
{{ tasks }}
```

hoặc:

```django
{% for task in tasks %}
    {{ task.title }}
{% endfor %}
```

---

## 6. Template cho ListView

File:

```txt
templates/tasks/task_list.html
```

Ví dụ:

```django
<h1>Task List</h1>

<ul>
    {% for task in tasks %}
        <li>
            <a href="{% url 'task_detail' task.pk %}">
                {{ task.title }}
            </a>
        </li>
    {% empty %}
        <li>No tasks found.</li>
    {% endfor %}
</ul>
```

Ở đây `tasks` đến từ:

```python
context_object_name = "tasks"
```

---

## 7. Nếu không khai báo `context_object_name` trong ListView thì sao?

Nếu không viết:

```python
context_object_name = "tasks"
```

thì `ListView` vẫn chạy.

Ví dụ:

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
```

Khi đó Django mặc định truyền context với tên:

```txt
object_list
```

Ngoài ra, với model `Task`, Django cũng có thể tạo tên mặc định:

```txt
task_list
```

Trong template có thể dùng:

```django
{% for task in object_list %}
    {{ task.title }}
{% endfor %}
```

hoặc:

```django
{% for task in task_list %}
    {{ task.title }}
{% endfor %}
```

Tuy nhiên, trong project thực tế nên khai báo rõ:

```python
context_object_name = "tasks"
```

để template dễ đọc hơn.

---

## 8. DetailView cơ bản

### 8.1. Function-based view tương đương

Nếu viết bằng FBV:

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

Ở đây mình tự làm:

```txt
1. Nhận pk từ URL
2. Tự gọi get_object_or_404(Task, pk=pk)
3. Nếu không tìm thấy thì trả 404
4. Tạo context {"task": task}
5. Render template
```

---

### 8.2. Viết bằng DetailView

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

---

### 8.3. DetailView đang làm thay mình những gì?

Khi user truy cập:

```txt
/tasks/1/
```

`DetailView` tự làm:

```txt
1. Nhận pk từ URL
2. Tìm object Task có pk tương ứng
3. Nếu không tìm thấy thì trả 404
4. Tạo context
5. Render template_name
6. Trả response
```

Vì vậy ta không cần tự viết:

```python
get_object_or_404(Task, pk=pk)
```

`DetailView` đã xử lý phần đó.

---

## 9. Template cho DetailView

File:

```txt
templates/tasks/task_detail.html
```

Ví dụ:

```django
<h1>{{ task.title }}</h1>

<p>{{ task.description }}</p>

{% if task.is_done %}
    <p>Status: Done</p>
{% else %}
    <p>Status: Not done</p>
{% endif %}

<a href="{% url 'task_list' %}">Back to list</a>
```

Ở đây `task` đến từ:

```python
context_object_name = "task"
```

---

## 10. Nếu không khai báo `context_object_name` trong DetailView thì sao?

Nếu không viết:

```python
context_object_name = "task"
```

thì `DetailView` vẫn chạy.

Ví dụ:

```python
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
```

Khi đó Django mặc định truyền object với tên:

```txt
object
```

Ngoài ra, với model `Task`, Django cũng có thể tạo tên mặc định:

```txt
task
```

Trong template có thể dùng:

```django
{{ object.title }}
```

hoặc:

```django
{{ task.title }}
```

Tuy nhiên, nên khai báo rõ:

```python
context_object_name = "task"
```

để template dễ đọc hơn.

---

## 11. URL với `pk`

`DetailView` mặc định tìm object dựa trên `pk`.

Vì vậy URL thường viết:

```python
path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail")
```

Trong đó:

```txt
<int:pk>
```

là id của object.

Ví dụ:

```txt
/tasks/1/
```

thì:

```txt
pk = 1
```

`DetailView` sẽ tìm object tương ứng.

Nếu object không tồn tại, Django trả 404.

---

## 12. Template mặc định của ListView và DetailView

Nếu không khai báo:

```python
template_name = "tasks/task_list.html"
```

Django sẽ cố tìm template theo convention mặc định.

Với `ListView` của model `Task`, template mặc định thường là:

```txt
<app_name>/<model_name>_list.html
```

Ví dụ app tên `tasks`, model tên `Task`:

```txt
tasks/task_list.html
```

Với `DetailView`, template mặc định thường là:

```txt
<app_name>/<model_name>_detail.html
```

Ví dụ:

```txt
tasks/task_detail.html
```

Nghĩa là nếu file template đúng convention, có thể viết ngắn:

```python
class TaskListView(ListView):
    model = Task
```

```python
class TaskDetailView(DetailView):
    model = Task
```

Tuy nhiên, khi mới học hoặc khi làm project cần rõ ràng, nên khai báo:

```python
template_name = "tasks/task_list.html"
```

và:

```python
template_name = "tasks/task_detail.html"
```

---

## 13. Flow tổng quan

### 13.1. Flow của ListView

```txt
User truy cập /tasks/
    ↓
Django gọi TaskListView.as_view()
    ↓
dispatch() gọi get()
    ↓
ListView lấy danh sách Task
    ↓
Tạo context
    ↓
Render tasks/task_list.html
    ↓
Trả response
```

---

### 13.2. Flow của DetailView

```txt
User truy cập /tasks/1/
    ↓
Django gọi TaskDetailView.as_view()
    ↓
dispatch() gọi get()
    ↓
DetailView lấy pk từ URL
    ↓
Tìm object Task có pk = 1
    ↓
Nếu không có thì 404
    ↓
Nếu có thì tạo context
    ↓
Render tasks/task_detail.html
    ↓
Trả response
```

---

## 14. Các attribute cơ bản cần nhớ

| Attribute             | Dùng trong               | Vai trò                      |
| --------------------- | ------------------------ | ---------------------------- |
| `model`               | `ListView`, `DetailView` | Model cần lấy dữ liệu        |
| `template_name`       | `ListView`, `DetailView` | Template cần render          |
| `context_object_name` | `ListView`, `DetailView` | Tên biến truyền vào template |

Ví dụ:

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
```

```python
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
```

---

## 15. Lỗi thường gặp ở phần Basic

### 15.1. Quên `.as_view()`

Sai:

```python
path("tasks/", TaskListView, name="task_list")
```

Đúng:

```python
path("tasks/", TaskListView.as_view(), name="task_list")
```

CBV phải dùng `.as_view()` trong URL.

---

### 15.2. Template dùng sai tên context

View:

```python
class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
```

Template sai:

```django
{% for task in task_list %}
    {{ task.title }}
{% endfor %}
```

Template đúng:

```django
{% for task in tasks %}
    {{ task.title }}
{% endfor %}
```

Vì view đã khai báo:

```python
context_object_name = "tasks"
```

---

### 15.3. DetailView URL không có `pk`

Sai:

```python
path("tasks/detail/", TaskDetailView.as_view(), name="task_detail")
```

Với URL này, `DetailView` không biết cần lấy task nào.

Đúng:

```python
path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail")
```

---

### 15.4. Sai template path

View:

```python
class TaskListView(ListView):
    template_name = "tasks/task_list.html"
```

Nhưng file thật lại nằm ở:

```txt
templates/task_list.html
```

Kết quả có thể gặp lỗi template not found.

Cần đảm bảo path đúng:

```txt
templates/tasks/task_list.html
```

---

# Part 2: Advanced / Mở rộng

## 16. Khi nào cần xem phần Advanced?

Phần Basic đủ dùng khi:

```txt
- Lấy toàn bộ object
- Hiển thị list đơn giản
- Hiển thị detail theo pk
- Không cần filter
- Không cần pagination
- Không cần thêm context
```

Cần xem phần Advanced khi gặp case như:

```txt
- Chỉ lấy task của user hiện tại
- Filter task theo trạng thái
- Search theo keyword trên query params
- Sắp xếp dữ liệu
- Phân trang
- Truyền thêm dữ liệu phụ vào template
- DetailView lấy object theo slug
- DetailView cần custom cách tìm object
- Tối ưu query tránh N+1
```

---

## 17. Custom queryset với `get_queryset()`

`get_queryset()` là method dùng để quyết định danh sách object mà `ListView` sẽ hiển thị.

Mặc định, nếu khai báo:

```python
class TaskListView(ListView):
    model = Task
```

Django sẽ lấy gần giống:

```python
Task.objects.all()
```

Nếu muốn thay đổi danh sách này, override `get_queryset()`.

Ví dụ chỉ lấy task chưa hoàn thành:

```python
from django.views.generic import ListView
from .models import Task

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(is_done=False)
```

Khi đó template chỉ nhận danh sách task chưa hoàn thành.

---

## 18. Filter theo user hiện tại

Ví dụ model có field:

```python
created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

Muốn chỉ hiển thị task của user đang login:

```python
class MyTaskListView(ListView):
    model = Task
    template_name = "tasks/my_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
```

Điểm quan trọng:

```python
self.request.user
```

Trong CBV, khi muốn lấy request hiện tại ở các method như `get_queryset()`, thường dùng `self.request`.

---

## 19. Filter theo query params

Ví dụ URL:

```txt
/tasks/?status=done
```

Muốn filter theo `status`.

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.all()

        status = self.request.GET.get("status")

        if status == "done":
            queryset = queryset.filter(is_done=True)

        if status == "todo":
            queryset = queryset.filter(is_done=False)

        return queryset
```

Giải thích:

```python
self.request.GET.get("status")
```

lấy query param `status` từ URL.

Ví dụ:

```txt
/tasks/?status=done
```

thì:

```txt
status = "done"
```

---

## 20. Search theo keyword

Ví dụ URL:

```txt
/tasks/?q=django
```

Muốn tìm task có title chứa keyword.

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.all()

        q = self.request.GET.get("q")

        if q:
            queryset = queryset.filter(title__icontains=q)

        return queryset
```

Template search form:

```django
<form method="get">
    <input type="text" name="q" value="{{ request.GET.q }}">
    <button type="submit">Search</button>
</form>
```

Lưu ý: để dùng `request` trong template, cần đảm bảo template context processors có `django.template.context_processors.request`.

---

## 21. Ordering

Có 2 cách sắp xếp dữ liệu trong `ListView`.

### 21.1. Dùng attribute `ordering`

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    ordering = ["-id"]
```

Ví dụ:

```python
ordering = ["-id"]
```

nghĩa là task mới nhất lên trước.

---

### 21.2. Ordering trong `get_queryset()`

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(is_done=False).order_by("-id")
```

Cách này phù hợp khi vừa filter vừa sort.

---

## 22. Pagination với `paginate_by`

Nếu danh sách nhiều dữ liệu, dùng pagination.

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10
```

Khi đó mỗi page hiển thị 10 task.

URL sẽ có dạng:

```txt
/tasks/?page=1
/tasks/?page=2
```

Template pagination đơn giản:

```django
{% if is_paginated %}
    <div>
        {% if page_obj.has_previous %}
            <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
        {% endif %}

        <span>
            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Next</a>
        {% endif %}
    </div>
{% endif %}
```

Các biến hay dùng:

| Biến                    | Ý nghĩa                  |
| ----------------------- | ------------------------ |
| `is_paginated`          | Có đang phân trang không |
| `page_obj`              | Page hiện tại            |
| `paginator`             | Object phân trang        |
| `page_obj.has_previous` | Có trang trước không     |
| `page_obj.has_next`     | Có trang sau không       |
| `page_obj.number`       | Số trang hiện tại        |

---

## 23. Thêm context bằng `get_context_data()`

`get_context_data()` dùng để thêm dữ liệu phụ vào template.

Ví dụ ngoài danh sách task, muốn truyền thêm số lượng task đã hoàn thành:

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_tasks"] = Task.objects.count()
        context["completed_tasks"] = Task.objects.filter(is_done=True).count()

        return context
```

Template:

```django
<p>Total: {{ total_tasks }}</p>
<p>Completed: {{ completed_tasks }}</p>
```

Điểm cần nhớ:

```python
context = super().get_context_data(**kwargs)
```

Nên gọi `super()` để giữ context mặc định của `ListView`.

---

## 24. Dùng `get_context_data()` trong DetailView

Ví dụ ở trang chi tiết task, muốn hiển thị thêm danh sách task liên quan.

```python
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["related_tasks"] = Task.objects.exclude(pk=self.object.pk)[:5]

        return context
```

Ở `DetailView`, object hiện tại thường có thể truy cập qua:

```python
self.object
```

---

## 25. DetailView với slug

Mặc định `DetailView` lấy object theo `pk`.

Nhưng nhiều app dùng slug cho URL đẹp hơn.

Ví dụ:

```txt
/posts/my-first-post/
```

Thay vì:

```txt
/posts/1/
```

Giả sử model có field:

```python
slug = models.SlugField(unique=True)
```

View:

```python
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    slug_field = "slug"
    slug_url_kwarg = "slug"
```

URL:

```python
path("tasks/<slug:slug>/", TaskDetailView.as_view(), name="task_detail")
```

Ý nghĩa:

```python
slug_field = "slug"
```

Django sẽ tìm object bằng field `slug` trong model.

```python
slug_url_kwarg = "slug"
```

Django sẽ lấy giá trị slug từ URL kwarg tên `slug`.

---

## 26. Custom `pk_url_kwarg`

Mặc định `DetailView` tìm URL kwarg tên:

```txt
pk
```

Ví dụ:

```python
path("tasks/<int:pk>/", TaskDetailView.as_view())
```

Nếu URL dùng tên khác, ví dụ:

```python
path("tasks/<int:task_id>/", TaskDetailView.as_view(), name="task_detail")
```

thì cần khai báo:

```python
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    pk_url_kwarg = "task_id"
```

Nếu không khai báo `pk_url_kwarg`, `DetailView` sẽ không biết lấy id từ đâu.

---

## 27. Custom `get_object()`

`get_object()` dùng để custom cách lấy object trong `DetailView`.

Ví dụ muốn chỉ cho user xem task của chính họ:

```python
from django.shortcuts import get_object_or_404

class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Task,
            pk=self.kwargs["pk"],
            created_by=self.request.user,
        )
```

Như vậy nếu user cố truy cập task của người khác, hệ thống sẽ trả 404.

Tuy nhiên, nhiều case có thể xử lý bằng `get_queryset()` gọn hơn.

Ví dụ:

```python
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
```

Khi đó `DetailView` vẫn dùng logic `get_object()` mặc định, nhưng object chỉ được tìm trong queryset đã filter theo user.

Cách này thường sạch hơn.

---

## 28. Nên custom `get_queryset()` hay `get_object()`?

Quy tắc đơn giản:

```txt
Muốn giới hạn tập dữ liệu được phép tìm kiếm
→ custom get_queryset()

Muốn thay đổi hoàn toàn cách lấy object
→ custom get_object()
```

Ví dụ nên dùng `get_queryset()`:

```python
def get_queryset(self):
    return Task.objects.filter(created_by=self.request.user)
```

Ví dụ cần dùng `get_object()`:

```python
def get_object(self, queryset=None):
    task = super().get_object(queryset)
    # custom logic đặc biệt
    return task
```

Hoặc:

```python
def get_object(self, queryset=None):
    return get_object_or_404(Task, code=self.kwargs["code"])
```

Nhưng nếu chỉ filter theo user, status, project, thì ưu tiên `get_queryset()`.

---

## 29. Tối ưu query với `select_related`

Nếu `Task` có ForeignKey tới `Project`:

```python
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
```

Trong template:

```django
{% for task in tasks %}
    {{ task.title }} - {{ task.project.name }}
{% endfor %}
```

### ❌ Vấn đề N+1 Query (Không tối ưu)

Giả sử có 50 task. Khi template gọi `task.project.name`, Django sẽ:

```txt
Query 1: SELECT * FROM task                          ← Lấy 50 task
Query 2: SELECT * FROM project WHERE id = 3          ← Lấy project cho task #1
Query 3: SELECT * FROM project WHERE id = 7          ← Lấy project cho task #2
Query 4: SELECT * FROM project WHERE id = 3          ← Lấy project cho task #3 (trùng!)
...
Query 51: SELECT * FROM project WHERE id = 12        ← Lấy project cho task #50

→ Tổng: 1 + 50 = 51 queries! (N+1 problem)
```

Mỗi vòng lặp `{% for task in tasks %}`, khi gặp `{{ task.project.name }}`, Django lại chạy 1 query riêng xuống DB để lấy project. **50 task = 50 query thừa.**

### ✅ Giải pháp: `select_related()` – Gộp bằng SQL JOIN

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.select_related("project").all()
```

Bây giờ Django chỉ chạy **1 query duy nhất** với JOIN:

```sql
SELECT task.*, project.*
FROM task
INNER JOIN project ON task.project_id = project.id

→ Tổng: 1 query! (Giảm từ 51 → 1)
```

**`select_related()` dùng cho:**

```txt
ForeignKey       (Task → Project)
OneToOneField    (User → UserProfile)
```

> Cơ chế: Dùng SQL `JOIN` để kéo data của bảng liên quan về cùng 1 query. Chỉ hoạt động với quan hệ "1" (mỗi task chỉ có 1 project).

---

## 30. Tối ưu query với `prefetch_related`

Nếu `Task` có ManyToMany với `Tag`:

```python
class Task(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
```

Template:

```django
{% for task in tasks %}
    <h3>{{ task.title }}</h3>

    {% for tag in task.tags.all %}
        {{ tag.name }}
    {% endfor %}
{% endfor %}
```

### ❌ Không tối ưu (N+1 lại xuất hiện)

```txt
Query 1: SELECT * FROM task                                          ← 50 task
Query 2: SELECT * FROM tag JOIN task_tags WHERE task_id = 1          ← Tags cho task #1
Query 3: SELECT * FROM tag JOIN task_tags WHERE task_id = 2          ← Tags cho task #2
...
Query 51: SELECT * FROM tag JOIN task_tags WHERE task_id = 50

→ Tổng: 51 queries!
```

### ✅ Giải pháp: `prefetch_related()` – Tách thành 2 query rồi ghép trong Python

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.prefetch_related("tags").all()
```

Django chạy **đúng 2 queries**:

```sql
-- Query 1: Lấy tất cả task
SELECT * FROM task

-- Query 2: Lấy TẤT CẢ tag liên quan trong 1 lần
SELECT * FROM tag
INNER JOIN task_tags ON tag.id = task_tags.tag_id
WHERE task_tags.task_id IN (1, 2, 3, ..., 50)

→ Tổng: 2 queries! (Giảm từ 51 → 2)
```

Sau đó Django tự **ghép tag vào đúng task** trong bộ nhớ Python. Template truy cập `task.tags.all` sẽ không query thêm nữa.

**`prefetch_related()` dùng cho:**

```txt
ManyToManyField       (Task ↔ Tag)
Reverse ForeignKey    (project.tasks.all() – chiều ngược)
```

> Cơ chế: Chạy query riêng rồi ghép bằng Python. Khác `select_related` (dùng JOIN), `prefetch_related` phù hợp với quan hệ "nhiều" (1 task có nhiều tag).

### 📊 So sánh nhanh

| | `select_related()` | `prefetch_related()` |
|:--|:--|:--|
| **Cơ chế** | SQL `JOIN` | 2 query riêng + ghép trong Python |
| **Quan hệ** | ForeignKey, OneToOne | ManyToMany, Reverse FK |
| **Số query** | 1 | 2 (hoặc N+1 nếu có nested) |
| **Khi nào dùng** | Quan hệ "1" | Quan hệ "nhiều" |

---

## 31. Kết hợp filter, ordering, select_related

Ví dụ thực tế:

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.select_related("project")

        status = self.request.GET.get("status")
        q = self.request.GET.get("q")

        if status == "done":
            queryset = queryset.filter(is_done=True)

        if status == "todo":
            queryset = queryset.filter(is_done=False)

        if q:
            queryset = queryset.filter(title__icontains=q)

        return queryset.order_by("-id")
```

View này xử lý:

```txt
- Tối ưu project bằng select_related
- Filter theo status
- Search theo q
- Sắp xếp mới nhất trước
- Phân trang 10 item/page
```

---

## 32. Giữ query params khi pagination

Nếu đang filter:

```txt
/tasks/?status=done&q=django&page=2
```

Khi render link pagination, nếu chỉ viết:

```django
<a href="?page={{ page_obj.next_page_number }}">Next</a>
```

thì sẽ mất `status` và `q`.

Cách đơn giản trong template:

```django
{% if page_obj.has_next %}
    <a href="?status={{ request.GET.status }}&q={{ request.GET.q }}&page={{ page_obj.next_page_number }}">
        Next
    </a>
{% endif %}
```

Cách này đủ hiểu, nhưng chưa tối ưu nếu có nhiều query params.

Trong project thực tế, có thể viết custom template tag để giữ toàn bộ query params và chỉ thay `page`.

---

## 33. Kết hợp LoginRequiredMixin

Nếu chỉ user đã login mới được xem danh sách task:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Task

class MyTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/my_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
```

Thứ tự kế thừa nên là:

```python
class MyTaskListView(LoginRequiredMixin, ListView):
```

Không nên viết ngược:

```python
class MyTaskListView(ListView, LoginRequiredMixin):
```

Mixin thường đặt bên trái generic view.

---

## 34. Custom empty message trong template

Với `ListView`, có thể dùng `{% empty %}` trong template:

```django
<ul>
    {% for task in tasks %}
        <li>{{ task.title }}</li>
    {% empty %}
        <li>No tasks found.</li>
    {% endfor %}
</ul>
```

Đây là cách đơn giản để xử lý danh sách rỗng.

---

## 35. Bảng tổng kết method/attribute mở rộng

| Method / Attribute   | Dùng trong               | Vai trò                            |
| -------------------- | ------------------------ | ---------------------------------- |
| `get_queryset()`     | `ListView`, `DetailView` | Custom tập dữ liệu                 |
| `get_context_data()` | `ListView`, `DetailView` | Thêm dữ liệu vào context           |
| `get_object()`       | `DetailView`             | Custom cách lấy object             |
| `paginate_by`        | `ListView`               | Phân trang                         |
| `ordering`           | `ListView`               | Sắp xếp dữ liệu                    |
| `slug_field`         | `DetailView`             | Field trong model dùng làm slug    |
| `slug_url_kwarg`     | `DetailView`             | Tên slug param trong URL           |
| `pk_url_kwarg`       | `DetailView`             | Tên pk param trong URL             |
| `select_related()`   | QuerySet                 | Tối ưu ForeignKey/OneToOne         |
| `prefetch_related()` | QuerySet                 | Tối ưu ManyToMany/reverse relation |

---

## 36. Lỗi thường gặp ở phần Advanced

### 36.1. Override `get_queryset()` nhưng quên return

Sai:

```python
def get_queryset(self):
    Task.objects.filter(is_done=False)
```

Đúng:

```python
def get_queryset(self):
    return Task.objects.filter(is_done=False)
```

---

### 36.2. Dùng `self.request.GET` nhưng không xử lý giá trị rỗng

Có thể viết:

```python
q = self.request.GET.get("q")

if q:
    queryset = queryset.filter(title__icontains=q)
```

Không nên filter trực tiếp khi `q` rỗng nếu logic không mong muốn.

---

### 36.3. Dùng `get_context_data()` nhưng quên `super()`

Không nên:

```python
def get_context_data(self, **kwargs):
    return {
        "total_tasks": Task.objects.count(),
    }
```

Nên:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["total_tasks"] = Task.objects.count()
    return context
```

---

### 36.4. DetailView dùng URL param khác `pk` nhưng quên `pk_url_kwarg`

URL:

```python
path("tasks/<int:task_id>/", TaskDetailView.as_view())
```

View sai:

```python
class TaskDetailView(DetailView):
    model = Task
```

View đúng:

```python
class TaskDetailView(DetailView):
    model = Task
    pk_url_kwarg = "task_id"
```

---

### 36.5. Filter theo user nhưng quên LoginRequiredMixin

Không nên:

```python
class MyTaskListView(ListView):
    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
```

Nếu user chưa login, `self.request.user` có thể là AnonymousUser.

Nên dùng:

```python
class MyTaskListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
```

---

## 37. Nên dùng cách nào trong thực tế?

Với `ListView`:

```txt
List đơn giản
→ dùng model + template_name + context_object_name

List cần filter/search
→ override get_queryset()

List cần thêm dữ liệu phụ
→ override get_context_data()

List nhiều dữ liệu
→ dùng paginate_by

List có quan hệ ForeignKey/ManyToMany
→ cân nhắc select_related/prefetch_related
```

Với `DetailView`:

```txt
Detail theo pk
→ dùng mặc định

Detail theo slug
→ dùng slug_field + slug_url_kwarg

Detail cần giới hạn quyền xem
→ custom get_queryset() theo user

Detail cần logic lấy object đặc biệt
→ custom get_object()
```

---

## 38. Kết luận

`ListView` và `DetailView` rất mạnh vì chúng xử lý sẵn các flow phổ biến:

```txt
ListView:
Lấy danh sách object → tạo context → render template

DetailView:
Lấy một object → tạo context → render template
```

Phần Basic đủ dùng cho các case đơn giản.

Phần Advanced dùng khi cần custom behavior:

```txt
get_queryset()
get_context_data()
get_object()
pagination
ordering
slug
query optimization
```

Khi gặp một yêu cầu mới, hãy tự hỏi:

```txt
Mình chỉ cần đổi danh sách object?
→ get_queryset()

Mình cần thêm dữ liệu cho template?
→ get_context_data()

Mình cần đổi cách lấy object detail?
→ get_object() hoặc get_queryset()

Mình cần phân trang?
→ paginate_by

Mình cần URL đẹp bằng slug?
→ slug_field + slug_url_kwarg
```

---

## 39. Ghi nhớ nhanh

```txt
ListView = nhiều object.

DetailView = một object.

model = model cần lấy dữ liệu.

template_name = template cần render.

context_object_name = tên biến trong template.

get_queryset() = custom dữ liệu được lấy.

get_context_data() = thêm dữ liệu vào template.

get_object() = custom cách lấy object detail.

paginate_by = phân trang.

ordering = sắp xếp.

slug_field + slug_url_kwarg = lấy detail bằng slug.

pk_url_kwarg = đổi tên URL param của pk.

select_related = tối ưu ForeignKey/OneToOne.

prefetch_related = tối ưu ManyToMany/reverse relation.
```

---
