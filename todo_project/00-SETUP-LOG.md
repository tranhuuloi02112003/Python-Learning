# Nhật ký Xây dựng Todo App (Django)

File này lưu trữ toàn bộ các bước đã thực hiện từ con số 0 để xây dựng dự án Todo App bằng Django. Bạn có thể dùng file này làm "phao cứu sinh" để tự khởi tạo lại bất kỳ dự án Django nào sau này.

---

## PHẦN 1: Cài đặt Môi trường (Environment Setup)

**1. Tạo thư mục chứa dự án và di chuyển vào đó:**
```bash
mkdir todo_project
cd todo_project
```

**2. Tạo môi trường ảo (Virtual Environment):**
*Lý do: Giữ cho các thư viện (như Django) cài trong này không bị xung đột với các dự án khác trên máy tính.*
```bash
python3 -m venv venv
```

**3. Kích hoạt môi trường ảo:**
*Lưu ý: Bạn phải luôn chạy lệnh này mỗi khi mở Terminal mới để làm việc với dự án.*
```bash
source venv/bin/activate
```

**4. Cài đặt Django:**
```bash
pip install django
```

---

## PHẦN 2: Khởi tạo Cấu trúc (Project & App)

**5. Tạo bộ khung Project (Tòa nhà chính):**
*Lưu ý dấu `.` ở cuối để báo Django cài đặt ngay tại thư mục hiện tại.*
```bash
django-admin startproject my_todo .
```

**6. Tạo App `tasks` (Căn hộ phụ trách công việc):**
```bash
python manage.py startapp tasks
```

**7. Đăng ký App với Ban Quản lý (Project):**
* Mở file: `my_todo/settings.py`
* Tìm mảng `INSTALLED_APPS` và thêm `'tasks',` vào cuối:
```python
INSTALLED_APPS = [
    # ... code mặc định ...
    'tasks',
]
```

---

## PHẦN 3: Code Logic đầu tiên (Hello World)

**8. Tạo một View (Hàm xử lý):**
* Mở file `tasks/views.py`
```python
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return HttpResponse("<h1>Chào mừng đến với Todo List của tôi!</h1>")
```

**9. Cấu hình Đường dẫn (URL Routing):**
* Mở file `my_todo/urls.py`
```python
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'), 
]
```

---

## PHẦN 4: Thiết kế Cơ sở dữ liệu (Models)

**10. Tạo Model `Task` (Định nghĩa bảng dữ liệu):**
* Mở file `tasks/models.py`
```python
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

**11. Cập nhật Database (Migrations):**
*Chạy 2 lệnh này mỗi khi bạn chỉnh sửa file `models.py`:*
```bash
python manage.py makemigrations # Chụp bản nháp
python manage.py migrate        # Áp dụng nháp vào DB thật
```

**12. Đăng ký hiển thị Model lên trang Quản trị (Admin):**
* Mở file `tasks/admin.py`
```python
from django.contrib import admin
from .models import Task

admin.site.register(Task)
```

**13. Tạo tài khoản Giám đốc (Superuser):**
*Dùng để đăng nhập vào đường dẫn `/admin/`*
```bash
python manage.py createsuperuser
# Sau đó nhập Username, Email (bỏ trống được), Password (không hiện chữ khi gõ).
```

---

## PHẦN 5: Vận hành

**14. Khởi động Server:**
```bash
python manage.py runserver
```
* Vào trình duyệt truy cập: `http://127.0.0.1:8000/` để xem trang chủ.
* Truy cập `http://127.0.0.1:8000/admin/` để vào trang quản trị và thêm dữ liệu.

---

## PHỤ LỤC: Giải phẫu thư mục Project (`my_todo/`)

Khi bạn chạy lệnh `startproject my_todo`, Django tạo ra một thư mục `my_todo` chứa các file cốt lõi đóng vai trò là "Ban Quản lý" của toàn bộ dự án. Dưới đây là ý nghĩa của từng file:

1.  **`__init__.py`** (Initialize)
    *   *Ý nghĩa:* Đây là một file trống. Sự tồn tại của nó báo cho Python biết rằng thư mục `my_todo` này là một "Package" hợp lệ và có thể được import vào các nơi khác.

2.  **`settings.py`** (Cài đặt)
    *   *Ý nghĩa:* Đây là file **Trái tim** của dự án. Mọi cấu hình quan trọng nhất đều nằm ở đây: Kết nối Database gì (`DATABASES`), các App nào đang chạy (`INSTALLED_APPS`), ngôn ngữ và múi giờ (`LANGUAGE_CODE`, `TIME_ZONE`), hay cấu hình file tĩnh (CSS/JS/Images).

3.  **`urls.py`** (Uniform Resource Locator)
    *   *Ý nghĩa:* Đây là **Trạm Kiểm Soát Giao Thông** (Bộ định tuyến). Khi người dùng gõ một đường link (vd: `facebook.com/profile`), file này sẽ tiếp nhận và quyết định xem đường link đó sẽ được giao cho hàm nào (View nào) để xử lý. Nó giống như "Mục lục" của trang web vậy.

4.  **`wsgi.py`** (Web Server Gateway Interface)
    *   *Ý nghĩa:* WSGI (đọc là *wiz-gee*). Đây là file dùng để **Đưa web lên mạng (Deploy)**. Nó đóng vai trò là cầu nối giao tiếp giữa Python và các Server thực tế trên mạng (như Apache, Nginx, Gunicorn) theo mô hình "Đồng bộ" (Xử lý từng yêu cầu một). Lúc bạn code trên máy tính thì không bao giờ đụng tới file này.

5.  **`asgi.py`** (Asynchronous Server Gateway Interface)
    *   *Ý nghĩa:* Đây là "người anh em hiện đại" của `wsgi`. ASGI dùng để xử lý các kết nối "Bất đồng bộ" (Asynchronous). Nếu web của bạn có tính năng chat realtime (chat trực tiếp nhắn phát thấy ngay), web socket, thì bạn sẽ cần dùng tới file này để cấu hình khi đưa web lên mạng.
