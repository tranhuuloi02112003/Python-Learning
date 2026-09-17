# 04. TemplateView and RedirectView

## 1. Mục tiêu

File này tập trung vào 2 generic class-based views đơn giản nhất trong Django:

```txt
TemplateView
RedirectView
```

Sau khi học xong phần này, cần hiểu được:

- `TemplateView` dùng để làm gì
- Khi nào nên dùng `TemplateView`
- Cách truyền `template_name`
- Cách truyền thêm context bằng `get_context_data()`
- `RedirectView` dùng để làm gì
- Khi nào nên dùng `RedirectView`
- Cách redirect bằng `url`
- Cách redirect bằng `pattern_name`
- Khi nào không nên dùng 2 view này

Theo Django docs, tất cả class-based views đều kế thừa từ `View`. Trong nhóm base views, `TemplateView` mở rộng `View` để render template, còn `RedirectView` dùng để tạo HTTP redirect.

---

## 2. Cách học phần này

Để dễ nhớ, phần này chia thành 2 nhóm:

- Phần cơ bản, nên nắm trước:
  `TemplateView`, `template_name`, `get_context_data()`, `RedirectView`, `url`, `pattern_name`
- Phần ít dùng hơn:
  URL kwargs trong `TemplateView`, `query_string`, `get_redirect_url()`, `permanent=True`

Nếu chỉ muốn nắm phần quan trọng nhất, hãy tập trung từ mục `3` đến mục `9` trước.

---

## 3. `TemplateView` là gì?

`TemplateView` là generic class-based view dùng để render một template.

Nó phù hợp với các page đơn giản, ít logic backend.

Ví dụ:

- `/about/`
- `/contact/`
- `/terms/`
- `/privacy/`
- `/dashboard/`

Nếu page chỉ cần render template, không cần query phức tạp, không cần xử lý form, thì `TemplateView` là lựa chọn tốt.

---

## 4. `TemplateView` cơ bản

### 4.1. Function-based view tương đương

Giả sử muốn render page About.

```python
# views.py
from django.shortcuts import render

def about_view(request):
    return render(request, "pages/about.html")
```

URL:

```python
# urls.py
from django.urls import path
from .views import about_view

urlpatterns = [
    path("about/", about_view, name="about"),
]
```

Ở đây mình tự gọi:

```python
render(request, "pages/about.html")
```

### 4.2. Viết bằng `TemplateView` trực tiếp trong `urls.py`

```python
# urls.py
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
]
```

Với cách này, ta không cần viết `views.py`.

Django docs cũng có ví dụ dùng `TemplateView.as_view(template_name="about.html")` trực tiếp trong URLconf khi chỉ cần thay đổi một vài attribute đơn giản.

### 4.3. Viết bằng subclass `TemplateView`

```python
# views.py
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "pages/about.html"
```

URL:

```python
# urls.py
from django.urls import path
from .views import AboutView

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
]
```

Đây là cách nên dùng khi page có khả năng cần mở rộng thêm context hoặc logic sau này.

### 4.4. `TemplateView` đang làm thay mình những gì?

Với FBV, mình tự viết:

```python
return render(request, "pages/about.html")
```

Với `TemplateView`, Django tự xử lý flow render template.

Có thể hiểu flow như sau:

1. User truy cập `/about/`
2. Django gọi `AboutView.as_view()`
3. `dispatch()` route request GET tới `get()`
4. `TemplateView` xác định `template_name`
5. `TemplateView` tạo context
6. `TemplateView` render template
7. Trả response

Nói đơn giản:

FBV:
Mình tự gọi `render()`.

`TemplateView`:
Django tự render template dựa trên `template_name`.

---

## 5. Khi nào nên và không nên dùng `TemplateView`

### 5.1. Nên dùng `TemplateView` khi

- About page
- Contact information page
- Terms of service page
- Privacy policy page
- Landing page đơn giản
- Dashboard page chỉ cần truyền vài biến context đơn giản

Ví dụ:

```python
from django.views.generic import TemplateView

class TermsView(TemplateView):
    template_name = "pages/terms.html"
```

### 5.2. Không nên dùng `TemplateView` khi

Không nên dùng `TemplateView` nếu page chủ yếu là danh sách object hoặc chi tiết object.

Ví dụ:

- `/tasks/` -> nên dùng `ListView`
- `/tasks/1/` -> nên dùng `DetailView`
- `/tasks/create/` -> nên dùng `CreateView`
- `/tasks/1/edit/` -> nên dùng `UpdateView`

Không nên cố dùng `TemplateView` rồi tự query quá nhiều trong `get_context_data()`.

Ví dụ vẫn làm được:

```python
class TaskPageView(TemplateView):
    template_name = "tasks/task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.all()
        return context
```

Nhưng nếu mục đích chính là hiển thị list `Task`, thì dùng `ListView` hợp lý hơn.

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
```

Quy tắc đơn giản:

- Page tĩnh hoặc ít dữ liệu -> `TemplateView`
- Danh sách object -> `ListView`
- Chi tiết object -> `DetailView`
- Form tạo hoặc sửa -> `CreateView` hoặc `UpdateView`

---

## 6. Thêm context trong `TemplateView`

### 6.1. Bài toán

Muốn render dashboard và truyền thêm dữ liệu:

- `total_tasks`
- `completed_tasks`

### 6.2. FBV

```python
# views.py
from django.shortcuts import render
from .models import Task

def dashboard_view(request):
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_done=True).count()

    return render(request, "pages/dashboard.html", {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
    })
```

### 6.3. `TemplateView`

```python
# views.py
from django.views.generic import TemplateView
from .models import Task

class DashboardView(TemplateView):
    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_tasks"] = Task.objects.count()
        context["completed_tasks"] = Task.objects.filter(is_done=True).count()

        return context
```

URL:

```python
# urls.py
from django.urls import path
from .views import DashboardView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
```

### 6.4. `get_context_data()` là gì?

`get_context_data()` là method dùng để thêm dữ liệu vào context trước khi render template.

Trong CBV, thay vì tự viết:

```python
return render(request, "template.html", context)
```

ta thường override:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["key"] = value
    return context
```

Điểm quan trọng:

```python
context = super().get_context_data(**kwargs)
```

Dòng này lấy context mặc định từ class cha.

Sau đó mình thêm dữ liệu riêng:

```python
context["total_tasks"] = Task.objects.count()
```

Cuối cùng return context:

```python
return context
```

### 6.5. Vì sao nên gọi `super().get_context_data()`?

Nên gọi:

```python
context = super().get_context_data(**kwargs)
```

vì class cha có thể đã chuẩn bị sẵn context mặc định.

Nếu không gọi `super()`, ta có thể vô tình làm mất context mặc định của CBV hoặc mixin khác.

Ví dụ nên viết:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["page_title"] = "Dashboard"
    return context
```

Không nên viết:

```python
def get_context_data(self, **kwargs):
    return {
        "page_title": "Dashboard",
    }
```

Vì cách này bỏ qua context từ class cha.

### 6.6. `TemplateView` có xử lý POST không?

Mặc định, `TemplateView` chủ yếu dùng để render template qua GET.

Nếu cần xử lý form POST, thường không nên dùng `TemplateView`.

Nên dùng:

- `FormView`
- `CreateView`
- `UpdateView`

Ví dụ nếu có contact form:

```text
/contact/
```

Không nên xử lý bằng `TemplateView` nếu form có validate và submit logic.

Nên dùng `FormView`.

```python
from django.views.generic.edit import FormView

class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = "/thanks/"
```

Quy tắc:

- Render page đơn giản -> `TemplateView`
- Xử lý form -> `FormView`, `CreateView`, `UpdateView`

---

## 7. `RedirectView` là gì?

`RedirectView` là generic class-based view dùng để redirect từ URL này sang URL khác.

Ví dụ:

- `/old-about/` -> `/about/`
- `/home/` -> `/`

Theo Django docs, `RedirectView` cung cấp HTTP redirect, và có thể cấu hình `url` trực tiếp hoặc dùng `pattern_name`.

---

## 8. `RedirectView` cơ bản

### 8.1. Redirect bằng FBV

```python
# views.py
from django.shortcuts import redirect

def old_about_redirect(request):
    return redirect("about")
```

URL:

```python
# urls.py
from django.urls import path
from .views import old_about_redirect

urlpatterns = [
    path("old-about/", old_about_redirect, name="old_about"),
]
```

### 8.2. Redirect bằng `RedirectView` với `url`

```python
# urls.py
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        "old-about/",
        RedirectView.as_view(url="/about/"),
        name="old_about",
    ),
]
```

Khi user vào:

```text
/old-about/
```

Django redirect sang:

```text
/about/
```

### 8.3. Redirect bằng subclass `RedirectView`

```python
# views.py
from django.views.generic import RedirectView

class OldAboutRedirectView(RedirectView):
    url = "/about/"
```

URL:

```python
# urls.py
from django.urls import path
from .views import OldAboutRedirectView

urlpatterns = [
    path("old-about/", OldAboutRedirectView.as_view(), name="old_about"),
]
```

### 8.4. Redirect bằng `pattern_name`

Thay vì redirect bằng URL cứng:

```python
url = "/about/"
```

có thể redirect bằng route name:

```python
pattern_name = "about"
```

Ví dụ:

```python
# views.py
from django.views.generic import RedirectView

class GoToAboutView(RedirectView):
    pattern_name = "about"
```

URL:

```python
# urls.py
from django.urls import path
from .views import GoToAboutView, AboutView

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("go-about/", GoToAboutView.as_view(), name="go_about"),
]
```

Khi user vào:

```text
/go-about/
```

Django redirect tới URL có `name="about"`.

### 8.5. `RedirectView` đang làm thay mình những gì?

Với FBV, mình tự viết:

```python
return redirect("about")
```

Với `RedirectView`, Django tự xử lý redirect dựa trên config.

Flow đơn giản:

1. User truy cập `/old-about/`
2. Django gọi `OldAboutRedirectView.as_view()`
3. `RedirectView` xác định URL cần redirect
4. Trả HTTP redirect response
5. Browser chuyển user sang URL mới

---

## 9. Khi nào nên và không nên dùng `RedirectView`

### 9.1. Nên dùng `RedirectView` khi

- Đổi URL cũ sang URL mới
- Tạo alias URL
- Redirect landing route
- Redirect dựa trên route name
- Redirect đơn giản không cần xử lý nhiều logic

Ví dụ:

- `/old-about/` -> `/about/`
- `/home/` -> `/`
- `/profile/` -> `/users/me/`

### 9.2. Không nên dùng `RedirectView` khi

Không nên dùng `RedirectView` nếu redirect cần nhiều logic nghiệp vụ phức tạp.

Ví dụ:

- Check nhiều điều kiện permission
- Xử lý form rồi redirect
- Ghi log phức tạp
- Query nhiều model trước khi redirect

Với case phức tạp, có thể dùng FBV hoặc override CBV rõ ràng hơn.

Ví dụ FBV:

```python
from django.shortcuts import redirect

def smart_redirect(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")

    return redirect("user_dashboard")
```

Code này dùng FBV có thể dễ đọc hơn.

---

## 10. Phần ít dùng hơn nhưng nên biết

Phần này gom các ví dụ ít gặp hơn để tài liệu không bị dàn đều trọng tâm. Khi mới học, không cần nhớ hết ngay.

### 10.1. `TemplateView` với URL kwargs

URL:

```text
/users/loi/
```

Muốn lấy `username` từ URL và truyền vào template.

```python
# urls.py
from django.urls import path
from .views import UserProfilePageView

urlpatterns = [
    path("users/<str:username>/", UserProfilePageView.as_view(), name="user_profile"),
]
```

```python
# views.py
from django.views.generic import TemplateView

class UserProfilePageView(TemplateView):
    template_name = "pages/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.kwargs["username"]
        return context
```

Nếu user truy cập `/users/loi/` thì:

```python
username = "loi"
```

### 10.2. `RedirectView` với URL kwargs

URL cũ:

```text
/old-tasks/1/
```

Muốn redirect sang:

```text
/tasks/1/
```

```python
# urls.py
from django.urls import path
from .views import OldTaskRedirectView, TaskDetailView

urlpatterns = [
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("old-tasks/<int:pk>/", OldTaskRedirectView.as_view(), name="old_task_detail"),
]
```

```python
# views.py
from django.views.generic import RedirectView

class OldTaskRedirectView(RedirectView):
    pattern_name = "task_detail"
```

Khi user vào `/old-tasks/1/`, `RedirectView` nhận:

```python
kwargs = {"pk": 1}
```

Sau đó dùng `pattern_name = "task_detail"` để reverse URL `/tasks/1/`.

### 10.3. `permanent = True` và `permanent = False`

Trong `RedirectView`, mặc định:

```python
permanent = False
```

Nghĩa là redirect tạm thời.

Ví dụ:

```python
class OldAboutRedirectView(RedirectView):
    url = "/about/"
    permanent = False
```

Nếu muốn redirect vĩnh viễn:

```python
class OldAboutRedirectView(RedirectView):
    url = "/about/"
    permanent = True
```

Ý nghĩa thực tế:

- `permanent = False` -> redirect tạm thời
- `permanent = True` -> redirect vĩnh viễn

Cẩn thận với `permanent = True`, vì browser và search engine có thể cache redirect này.

### 10.4. Giữ query string khi redirect

Mặc định, `RedirectView` không nhất thiết giữ query string.

Nếu muốn giữ query string, dùng:

```python
query_string = True
```

Ví dụ:

```python
from django.views.generic import RedirectView

class SearchRedirectView(RedirectView):
    url = "/search/"
    query_string = True
```

Nếu user vào:

```text
/old-search/?q=django
```

thì redirect sang:

```text
/search/?q=django
```

### 10.5. Custom redirect bằng `get_redirect_url()`

Nếu redirect cần logic động, override:

```python
get_redirect_url()
```

Ví dụ:

```python
from django.views.generic import RedirectView

class TaskRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs["pk"]
        return f"/tasks/{pk}/"
```

Hoặc dùng `reverse()` cho tốt hơn:

```python
from django.urls import reverse
from django.views.generic import RedirectView

class TaskRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("task_detail", kwargs={
            "pk": kwargs["pk"],
        })
```

Dùng `get_redirect_url()` khi URL đích phụ thuộc vào logic custom.

---

## 11. So sánh nhanh

### 11.1. `TemplateView` và `RedirectView`

| View | Mục đích | Cấu hình chính | Thường dùng cho |
| --- | --- | --- | --- |
| `TemplateView` | Render template | `template_name` | About, Terms, Dashboard đơn giản |
| `RedirectView` | Redirect URL | `url`, `pattern_name` | URL cũ sang URL mới, alias route |

### 11.2. So sánh với FBV

`TemplateView`

FBV:

```python
def about_view(request):
    return render(request, "pages/about.html")
```

CBV:

```python
class AboutView(TemplateView):
    template_name = "pages/about.html"
```

Điểm khác:

FBV:
Mình tự gọi `render()`.

`TemplateView`:
Django render dựa trên `template_name`.

`RedirectView`

FBV:

```python
def old_about_redirect(request):
    return redirect("about")
```

CBV:

```python
class OldAboutRedirectView(RedirectView):
    pattern_name = "about"
```

Điểm khác:

FBV:
Mình tự gọi `redirect()`.

`RedirectView`:
Django redirect dựa trên `url` hoặc `pattern_name`.

---

## 12. Lỗi thường gặp

### 12.1. Quên `template_name`

Sai:

```python
class AboutView(TemplateView):
    pass
```

Nếu không có template mặc định phù hợp, Django sẽ không biết render file nào.

Đúng:

```python
class AboutView(TemplateView):
    template_name = "pages/about.html"
```

### 12.2. Dùng `TemplateView` cho list object phức tạp

Không nên:

```python
class TaskPageView(TemplateView):
    template_name = "tasks/task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.all()
        return context
```

Nên dùng:

```python
class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
```

### 12.3. Dùng URL hard-code quá nhiều trong `RedirectView`

Có thể dùng:

```python
url = "/about/"
```

Nhưng nếu URL có name, thường nên dùng:

```python
pattern_name = "about"
```

Vì khi đổi path thật, route name vẫn giúp code ổn định hơn.

### 12.4. Dùng `permanent = True` quá sớm

Không nên bật permanent redirect nếu URL mới chưa chắc cố định.

```python
class OldPageRedirectView(RedirectView):
    url = "/new-page/"
    permanent = True
```

Chỉ nên dùng `permanent = True` khi chắc chắn URL cũ đã được thay thế vĩnh viễn.

---

## 13. Bảng tổng kết

| Thành phần | Vai trò |
| --- | --- |
| `TemplateView` | Render một template |
| `template_name` | Tên template cần render |
| `get_context_data()` | Thêm dữ liệu vào context |
| `RedirectView` | Redirect tới URL khác |
| `url` | URL đích dạng hard-code |
| `pattern_name` | URL name dùng để reverse |
| `permanent` | Redirect tạm thời hoặc vĩnh viễn |
| `query_string` | Có giữ query string khi redirect không |
| `get_redirect_url()` | Custom URL redirect động |

---

## 14. Ghi nhớ nhanh

- `TemplateView` = render template
- `RedirectView` = redirect URL
- `TemplateView` phù hợp page tĩnh hoặc page ít logic
- `RedirectView` phù hợp URL cũ sang URL mới
- Thêm context trong `TemplateView` bằng `get_context_data()`
- Redirect động trong `RedirectView` bằng `get_redirect_url()`
- Nếu list object -> dùng `ListView`
- Nếu detail object -> dùng `DetailView`
- Nếu form -> dùng `FormView`, `CreateView`, `UpdateView`

---

## 15. Kết luận

`TemplateView` và `RedirectView` là hai generic views đơn giản nhất nhưng rất hữu ích.

Chúng giúp mình tránh viết lại các FBV đơn giản như:

```python
return render(...)
```

hoặc:

```python
return redirect(...)
```

Tuy nhiên, không nên lạm dụng.

Quy tắc thực tế:

- Page chỉ render template -> `TemplateView`
- URL chỉ redirect -> `RedirectView`
- Page hiển thị object, list, form -> dùng generic view phù hợp hơn
