# 03. View, as_view, dispatch, get, post

## 1. Mục tiêu

File này tập trung vào cơ chế chạy bên trong của Class-based View.

Sau khi học xong phần này, cần hiểu được:

- `View` base class là gì
- Vì sao URL phải dùng `ClassName.as_view()`
- `as_view()` làm gì
- `setup()` làm gì
- `dispatch()` làm gì
- Vì sao Django tự gọi `get()` hoặc `post()`
- Request đi qua CBV theo flow như thế nào

---

## 2. Vấn đề cần hiểu

Ở Function-based View, ta truyền function trực tiếp vào URL.

```python
# views.py
from django.http import HttpResponse

def hello_view(request):
    return HttpResponse("Hello Django")
```

```python
# urls.py
from django.urls import path
from .views import hello_view

urlpatterns = [
    path("hello/", hello_view, name="hello"),
]
```

Ở đây `hello_view` là một function.

Django có thể gọi trực tiếp:

```python
hello_view(request)
```

Nhưng với Class-based View, ta không truyền class trực tiếp vào URL.

```python
# views.py
from django.http import HttpResponse
from django.views import View

class HelloView(View):
    def get(self, request):
        return HttpResponse("Hello Django")
```

Trong URL, ta phải viết:

```python
# urls.py
from django.urls import path
from .views import HelloView

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
]
```

Điểm quan trọng là:

```python
HelloView.as_view()
```

Không phải:

```python
HelloView
```

Vì Django URL resolver cần một callable function-like object để gọi khi có request. Class-based views dùng `as_view()` để trả về một callable function xử lý request. Theo Django docs, function do `as_view()` trả về sẽ tạo instance của class, gọi `setup()`, rồi gọi `dispatch()`. `dispatch()` sau đó nhìn vào HTTP method như GET, POST, v.v. để chuyển request tới method tương ứng.

---

## 3. `View` base class là gì?

`View` là class nền tảng nhất của Class-based View.

Khi viết:

```python
from django.views import View

class HelloView(View):
    def get(self, request):
        ...
```

nghĩa là `HelloView` đang kế thừa từ `View`.

`View` cung cấp các cơ chế cơ bản:

- `as_view()`
- `setup()`
- `dispatch()`
- xử lý HTTP methods như `GET`, `POST`, `PUT`, `DELETE`
- trả `HttpResponseNotAllowed` nếu method không được hỗ trợ

Vì vậy, khi tự viết CBV cơ bản, thường bắt đầu bằng:

```python
from django.views import View
```

Ví dụ:

```python
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request):
        return HttpResponse("GET request")
```

---

## 4. Vì sao phải dùng `as_view()`?

Django URL cần một callable.

Với FBV:

```python
path("hello/", hello_view)
```

`hello_view` đã là callable.

Nhưng với CBV:

```python
class HelloView(View):
    ...
```

`HelloView` là class, không phải view function mà Django sẽ gọi trực tiếp theo kiểu thông thường.

Vì vậy cần:

```python
HelloView.as_view()
```

Có thể hiểu đơn giản:

```text
HelloView.as_view()
    ↓
Tạo ra một function trung gian
    ↓
Django gọi function đó khi có request
```

Tức là:

```python
path("hello/", HelloView.as_view())
```

gần giống như nói:

Khi user vào `/hello/`,
hãy gọi function được tạo ra từ `HelloView.as_view()`.

---

## 5. Flow tổng quan của một request trong CBV

Giả sử có view:

```python
from django.http import HttpResponse
from django.views import View

class HelloView(View):
    def get(self, request):
        return HttpResponse("Hello GET")

    def post(self, request):
        return HttpResponse("Hello POST")
```

URL:

```python
urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
]
```

Khi user truy cập `/hello/`, flow chạy như sau:

1. User gửi request tới `/hello/`
2. Django URL resolver match path `"hello/"`
3. Django gọi callable được tạo bởi `HelloView.as_view()`
4. Callable này tạo instance của `HelloView`
5. Gọi `setup()`
6. Gọi `dispatch()`
7. `dispatch()` kiểm tra `request.method`
8. Nếu `request.method == "GET"` thì gọi `get()`
9. Nếu `request.method == "POST"` thì gọi `post()`
10. Method `get()` hoặc `post()` trả về `HttpResponse`
11. Django trả response về cho user

Flow ngắn gọn:

```text
URL
 ↓
as_view()
 ↓
setup()
 ↓
dispatch()
 ↓
get() / post() / put() / delete()
 ↓
HttpResponse
```

---

## 6. `as_view()` hiểu đơn giản như thế nào?

Ta không cần nhớ implementation chi tiết của Django ngay từ đầu.

Chỉ cần hiểu ý tưởng:

```python
HelloView.as_view()
```

sẽ tạo ra một function tương tự như:

```python
def view(request, *args, **kwargs):
    self = HelloView()
    self.setup(request, *args, **kwargs)
    return self.dispatch(request, *args, **kwargs)
```

Đây chỉ là mô phỏng để dễ hiểu, không phải code đầy đủ của Django.

Điểm cần nhớ:

`as_view()` không xử lý logic chính của view.

`as_view()` tạo entry point để Django gọi được CBV.

Nói cách khác:

`as_view()` biến class thành view function.

---

## 7. `setup()` làm gì?

Sau khi tạo instance của class view, Django gọi `setup()`.

`setup()` dùng để gắn các thông tin request vào instance.

Có thể hiểu đơn giản:

`setup()` chuẩn bị dữ liệu ban đầu cho view instance.

Ví dụ sau `setup()`, view instance có thể truy cập:

- `self.request`
- `self.args`
- `self.kwargs`

Ví dụ:

```python
class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        print(self.request)
        print(self.kwargs)
```

Nếu URL là:

```python
path("tasks/<int:pk>/", TaskDetailView.as_view())
```

Khi user vào:

```text
/tasks/1/
```

thì trong view có thể có:

```python
self.kwargs["pk"]
```

Kết quả:

```python
1
```

---

## 8. `dispatch()` là gì?

`dispatch()` là method quyết định request sẽ được chuyển tới method nào.

Ví dụ request là GET:

```python
request.method = "GET"
```

thì `dispatch()` sẽ tìm method:

```python
get()
```

Request là POST:

```python
request.method = "POST"
```

thì `dispatch()` sẽ tìm method:

```python
post()
```

Django docs mô tả rằng `dispatch()` kiểm tra request là GET, POST, v.v. rồi chuyển tới method tương ứng nếu method đó được định nghĩa; nếu không có method phù hợp thì trả `HttpResponseNotAllowed`.

Ví dụ:

```python
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request):
        return HttpResponse("This is GET")
```

Nếu user mở trang bằng browser:

```text
GET /my-view/
```

Django gọi:

```python
MyView.get()
```

Nếu user gửi POST tới view này, nhưng class không có `post()`:

```text
POST /my-view/
```

Django sẽ trả response dạng:

```text
405 Method Not Allowed
```

Vì view này không hỗ trợ POST.

---

## 9. `get()` dùng khi nào?

`get()` xử lý request GET.

GET thường xảy ra khi user:

- mở một page trên browser
- click một link
- truy cập URL trực tiếp
- xem danh sách dữ liệu
- xem chi tiết object
- mở form tạo hoặc sửa dữ liệu

Ví dụ:

```python
from django.shortcuts import render
from django.views import View
from .models import Task

class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all()

        return render(request, "tasks/task_list.html", {
            "tasks": tasks,
        })
```

Khi user truy cập:

```text
/tasks/
```

Django gọi:

```python
TaskListView.get()
```

---

## 10. `post()` dùng khi nào?

`post()` xử lý request POST.

POST thường xảy ra khi user:

- submit form
- tạo dữ liệu mới
- cập nhật dữ liệu
- xóa dữ liệu
- gửi dữ liệu lên server

Ví dụ:

```python
from django.shortcuts import render, redirect
from django.views import View
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

dùng để hiển thị form rỗng.

```python
def post(self, request):
```

dùng để xử lý dữ liệu khi user submit form.

---

## 11. So sánh FBV và CBV ở flow GET/POST

### Function-based View

```python
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

Flow:

1. Django gọi `task_create(request)`
2. Bên trong function tự check `request.method`
3. Nếu POST thì xử lý submit form
4. Nếu không phải POST thì hiển thị form

### Class-based View

```python
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

Flow:

1. Django gọi callable tạo từ `TaskCreateView.as_view()`
2. `as_view()` tạo instance
3. `dispatch()` kiểm tra `request.method`
4. Nếu GET thì gọi `get()`
5. Nếu POST thì gọi `post()`

Điểm khác biệt chính:

FBV:
Mình tự viết `if request.method == "POST"`.

CBV:
`dispatch()` tự route request tới `get()` hoặc `post()`.

---

## 12. `*args` và `**kwargs` trong CBV

Nhiều ví dụ CBV viết như sau:

```python
class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        ...
```

Lý do là URL có thể truyền thêm tham số.

Ví dụ:

```python
path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail")
```

Khi user truy cập:

```text
/tasks/1/
```

Django truyền:

```python
kwargs = {"pk": 1}
```

Vì vậy trong view có thể lấy:

```python
pk = self.kwargs["pk"]
```

hoặc:

```python
pk = kwargs["pk"]
```

Ví dụ đầy đủ:

```python
from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import Task

class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])

        return render(request, "tasks/task_detail.html", {
            "task": task,
        })
```

---

## 13. `self.request`, `self.args`, `self.kwargs`

Trong CBV, sau khi `setup()` chạy, ta có thể dùng:

- `self.request`
- `self.args`
- `self.kwargs`

Ví dụ:

```python
class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        print(self.request.method)
        print(self.kwargs["pk"])
```

Có thể dùng trực tiếp `request` hoặc `self.request`.

Ví dụ này:

```python
def get(self, request, *args, **kwargs):
    print(request.user)
```

và:

```python
def get(self, request, *args, **kwargs):
    print(self.request.user)
```

trong nhiều trường hợp đều dùng được.

Tuy nhiên, khi viết các method khác như `get_queryset()`, `get_context_data()`, `form_valid()`, thường ta dùng:

- `self.request`
- `self.kwargs`

Ví dụ:

```python
def get_queryset(self):
    return Task.objects.filter(created_by=self.request.user)
```

---

## 14. Configure class attributes qua `as_view()`

Thông thường ta cấu hình CBV bằng class attributes:

```python
class GreetingView(View):
    greeting = "Hello"

    def get(self, request):
        return HttpResponse(self.greeting)
```

Nhưng cũng có thể truyền attribute qua `as_view()`:

```python
urlpatterns = [
    path(
        "hello/",
        GreetingView.as_view(greeting="Hello from urls.py"),
        name="hello",
    ),
]
```

Django docs có nói class attributes có thể được cấu hình bằng cách subclass và override attribute, hoặc truyền keyword arguments vào `as_view()` trong URLconf. Tuy nhiên, class được instantiate cho mỗi request, còn attributes truyền qua `as_view()` được cấu hình một lần khi URL được import.

Ví dụ:

```python
from django.http import HttpResponse
from django.views import View

class GreetingView(View):
    greeting = "Hello"

    def get(self, request):
        return HttpResponse(self.greeting)
```

URL:

```python
urlpatterns = [
    path("morning/", GreetingView.as_view(greeting="Good morning")),
    path("evening/", GreetingView.as_view(greeting="Good evening")),
]
```

Cùng một class, nhưng có thể dùng cho nhiều URL với cấu hình khác nhau.

---

## 15. Return trong CBV có khác FBV không?

Không khác.

Trong FBV, view trả về `HttpResponse`.

```python
def hello_view(request):
    return HttpResponse("Hello")
```

Trong CBV, method `get()` hoặc `post()` cũng trả về `HttpResponse`.

```python
class HelloView(View):
    def get(self, request):
        return HttpResponse("Hello")
```

Django docs cũng nói method trong CBV trả về giống như FBV, tức là một dạng `HttpResponse`; các shortcut như `render()`, `redirect()` hoặc `TemplateResponse` đều có thể dùng trong CBV.

Ví dụ dùng `render()`:

```python
class AboutView(View):
    def get(self, request):
        return render(request, "about.html")
```

Ví dụ dùng `redirect()`:

```python
class GoHomeView(View):
    def get(self, request):
        return redirect("home")
```

---

## 16. Ví dụ mô phỏng đầy đủ flow

View:

```python
from django.http import HttpResponse
from django.views import View

class DebugView(View):
    def dispatch(self, request, *args, **kwargs):
        print("1. dispatch is called")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("2. get is called")
        return HttpResponse("GET response")

    def post(self, request, *args, **kwargs):
        print("2. post is called")
        return HttpResponse("POST response")
```

URL:

```python
urlpatterns = [
    path("debug/", DebugView.as_view(), name="debug"),
]
```

Khi user mở `/debug/` bằng browser:

```text
GET /debug/
```

Console:

```text
1. dispatch is called
2. get is called
```

Response:

```text
GET response
```

Khi user submit POST tới `/debug/`:

```text
POST /debug/
```

Console:

```text
1. dispatch is called
2. post is called
```

Response:

```text
POST response
```

---

## 17. Override `dispatch()` khi nào?

Thông thường không cần override `dispatch()`.

Nhưng có thể override khi muốn xử lý logic chung trước tất cả HTTP methods.

Ví dụ:

```python
from django.shortcuts import redirect
from django.views import View

class LoginRequiredView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        return super().dispatch(request, *args, **kwargs)
```

View con:

```python
class TaskListView(LoginRequiredView):
    def get(self, request):
        ...
```

Khi request vào, `dispatch()` sẽ check login trước.

Nếu user chưa login:

`redirect("login")`

Nếu user đã login:

tiếp tục gọi `get()` hoặc `post()`.

Tuy nhiên, trong thực tế Django đã có sẵn `LoginRequiredMixin`, nên ta thường dùng mixin thay vì tự viết như trên.

Ví dụ:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
```

---

## 18. Lưu ý khi override `dispatch()`

Khi override `dispatch()`, thường phải gọi:

```python
return super().dispatch(request, *args, **kwargs)
```

Nếu quên dòng này, request sẽ không được chuyển tiếp đến `get()` hoặc `post()`.

Ví dụ sai:

```python
class MyView(View):
    def dispatch(self, request, *args, **kwargs):
        print("Before request")
```

View này không return response hợp lệ.

Ví dụ đúng:

```python
class MyView(View):
    def dispatch(self, request, *args, **kwargs):
        print("Before request")
        return super().dispatch(request, *args, **kwargs)
```

---

## 19. Thứ tự method trong CBV cơ bản

Với một CBV kế thừa `View`, thứ tự chạy thường là:

1. `as_view()`
2. `setup()`
3. `dispatch()`
4. `get()` hoặc `post()` hoặc `put()` hoặc `delete()`
5. return `HttpResponse`

Cần nhớ nhất là:

- `as_view()` là cổng vào
- `dispatch()` là bộ điều hướng HTTP method
- `get()` và `post()` là nơi viết logic xử lý request

---

## 20. Lỗi thường gặp

### 20.1. Quên `.as_view()`

Sai:

```python
urlpatterns = [
    path("hello/", HelloView, name="hello"),
]
```

Đúng:

```python
urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
]
```

CBV phải dùng `.as_view()` trong URL.

### 20.2. Viết `get()` thiếu `self`

Sai:

```python
class HelloView(View):
    def get(request):
        return HttpResponse("Hello")
```

Đúng:

```python
class HelloView(View):
    def get(self, request):
        return HttpResponse("Hello")
```

Vì đây là instance method của class, nên tham số đầu tiên là `self`.

### 20.3. Chỉ viết `get()` nhưng lại submit form bằng POST

Ví dụ:

```python
class TaskCreateView(View):
    def get(self, request):
        ...
```

Nếu form submit POST tới view này, Django không tìm thấy `post()`.

Kết quả có thể là:

```text
405 Method Not Allowed
```

Cần thêm:

```python
def post(self, request):
    ...
```

### 20.4. Override `dispatch()` nhưng không gọi `super()`

Sai:

```python
class MyView(View):
    def dispatch(self, request, *args, **kwargs):
        print("Check something")
```

Đúng:

```python
class MyView(View):
    def dispatch(self, request, *args, **kwargs):
        print("Check something")
        return super().dispatch(request, *args, **kwargs)
```

---

## 21. Bảng tổng kết

| Thành phần | Vai trò |
| --- | --- |
| `View` | Base class nền tảng của CBV |
| `as_view()` | Biến class thành callable để URL gọi được |
| `setup()` | Gắn request, args, kwargs vào instance |
| `dispatch()` | Điều hướng request tới method phù hợp |
| `get()` | Xử lý HTTP GET |
| `post()` | Xử lý HTTP POST |
| `put()` | Xử lý HTTP PUT |
| `delete()` | Xử lý HTTP DELETE |
| `self.request` | Request hiện tại |
| `self.args` | Positional args từ URL |
| `self.kwargs` | Keyword args từ URL, ví dụ `pk`, `slug` |

---

## 22. Ghi nhớ nhanh

- CBV không được truyền trực tiếp vào URL
- Phải dùng `ClassName.as_view()`
- `as_view()` tạo callable function
- Khi có request, Django tạo instance của class
- `setup()` chuẩn bị `request`, `args`, `kwargs`
- `dispatch()` kiểm tra HTTP method
- GET gọi `get()`
- POST gọi `post()`
- Method `get()` và `post()` vẫn phải trả về `HttpResponse` giống FBV

---

## 23. Kết luận

Phần quan trọng nhất của CBV là hiểu flow:

```text
URL
 ↓
ClassName.as_view()
 ↓
setup()
 ↓
dispatch()
 ↓
get() / post()
 ↓
HttpResponse
```

Nếu hiểu được flow này, các generic views như `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` sẽ dễ hiểu hơn nhiều.

Vì thực chất các generic views cũng dựa trên cùng cơ chế đó.

Chúng chỉ viết sẵn nhiều logic hơn ở các method như:

- `get_queryset()`
- `get_object()`
- `get_context_data()`
- `form_valid()`
- `form_invalid()`
- `get_success_url()`
