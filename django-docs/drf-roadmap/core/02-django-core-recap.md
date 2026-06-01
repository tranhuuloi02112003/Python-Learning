# 🔄 Ôn Lại Django Core – Nhớ Nhanh Trước Khi Học DRF

> Phase 0 của Roadmap. Đọc lướt 15 phút để nhớ lại toàn bộ xương sống Django.

---

## 1. Project vs App – "Công ty" vs "Phòng ban"

```txt
Project = Cả công ty (todo_project/)
App     = Phòng ban   (tasks/, projects/)
```

**Project** chứa cấu hình chung: `settings.py`, `urls.py` tổng, `manage.py`.
**App** chứa logic nghiệp vụ: `models.py`, `views.py`, `urls.py` riêng, `serializers.py`...

```txt
todo_project/                  ← Project (công ty)
├── manage.py                  ← "Cái remote" – chạy mọi lệnh Django
├── todo_project/              ← Config folder
│   ├── settings.py            ← "Luật công ty" – cấu hình toàn bộ
│   ├── urls.py                ← "Bảng chỉ dẫn tổng" – route vào app nào
│   └── wsgi.py / asgi.py      ← Entry point khi deploy
├── tasks/                     ← App (phòng ban Tasks)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py / serializers.py
│   ├── selectors.py
│   ├── services.py
│   └── migrations/
└── projects/                  ← App (phòng ban Projects)
    ├── models.py
    └── ...
```

> **Quy tắc nhớ:** 1 App = 1 chức năng độc lập. Nếu `models.py` quá dài → tách App mới.

---

## 2. `settings.py` – "Luật Công Ty"

Mọi thứ Django cần biết đều nằm ở đây. Các mục quan trọng nhất:

```python
# ── App nào được dùng? ──
INSTALLED_APPS = [
    # Apps mặc định của Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps bên thứ 3 (VD: DRF)
    "rest_framework",

    # Apps của mình
    "tasks",
    "projects",
]
# → Tạo app mới mà quên thêm vào đây = Django không nhận ra app đó.

# ── URL tổng ở đâu? ──
ROOT_URLCONF = "todo_project.urls"
# → Django đọc file này đầu tiên khi có request đến.

# ── Database nào? ──
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",    # Loại DB
        "NAME": "todo_db",                       # Tên database
        "USER": "root",
        "PASSWORD": "12345678",
        "HOST": "localhost",                     # Hoặc tên Docker service
        "PORT": "3306",
    }
}

# ── Middleware (các lớp xử lý request/response) ──
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",         # DRF API có thể tắt
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
# → Request đi qua Middleware TRƯỚC khi vào View.
# → Response đi qua Middleware TRƯỚC khi trả về client.
```

**Middleware hoạt động như thế nào:**

```txt
Client Request
    ↓
[SecurityMiddleware]      ← Lớp 1: Check HTTPS, headers
    ↓
[SessionMiddleware]       ← Lớp 2: Gắn session vào request
    ↓
[AuthenticationMiddleware]← Lớp 3: Gắn request.user
    ↓
[CsrfViewMiddleware]     ← Lớp 4: Check CSRF token (Template dùng, API có thể tắt)
    ↓
→ VIEW xử lý logic ←
    ↓
[Quay ngược các Middleware]
    ↓
Client Response
```

---

## 3. `urls.py` – "Bảng Chỉ Dẫn"

Request đến → Django đọc `ROOT_URLCONF` → match URL → gọi view tương ứng.

### Cấu trúc 2 tầng: Root → App

```python
# ── todo_project/urls.py (Root – Bảng chỉ dẫn tổng) ──
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),          # Chuyển sang app tasks
    path("projects/", include("projects.urls")),    # Chuyển sang app projects
    path("api/", include("api.urls")),              # DRF sẽ thêm prefix api/
]
```

```python
# ── tasks/urls.py (App – Bảng chỉ dẫn phòng ban) ──
from django.urls import path
from . import views

app_name = "tasks"     # Namespace – tránh trùng tên giữa các app

urlpatterns = [
    path("", views.task_list, name="list"),                    # /tasks/
    path("<int:pk>/", views.task_detail, name="detail"),       # /tasks/5/
    path("create/", views.task_create, name="create"),         # /tasks/create/
]
```

### Đường đi của request

```txt
GET /tasks/5/

1. Django đọc ROOT_URLCONF → todo_project/urls.py
2. Match "tasks/" → include("tasks.urls")
3. Phần còn lại "5/" → match "<int:pk>/" → gọi views.task_detail(request, pk=5)
```

### Sang DRF – urls.py vẫn y như vậy, chỉ thêm `.as_view()`

```python
# DRF urls.py
urlpatterns = [
    path("list", views.TaskViewSet.as_view({"get": "list"})),
    path("create", views.TaskViewSet.as_view({"post": "create"})),
    path("<int:pk>/", views.TaskViewSet.as_view({"get": "retrieve", "put": "update"})),
]
```

---

## 4. `models.py` – "Bản Thiết Kế Database"

Mỗi class Model = 1 bảng trong DB. Mỗi field = 1 cột.

```python
from django.db import models

class Task(models.Model):
    # ── Fields = Cột trong DB ──
    title = models.CharField(max_length=200)               # VARCHAR(200)
    description = models.TextField(blank=True)              # LONGTEXT, cho phép rỗng
    is_done = models.BooleanField(default=False)            # BOOLEAN, mặc định False
    due_date = models.DateField(null=True, blank=True)      # DATE, cho phép NULL
    created_at = models.DateTimeField(auto_now_add=True)    # Tự ghi lúc tạo
    updated_at = models.DateTimeField(auto_now=True)        # Tự ghi lúc update

    # ── Quan hệ = ForeignKey, M2M, O2O ──
    project = models.ForeignKey(
        "projects.Project",            # Lazy reference – tránh circular import
        on_delete=models.CASCADE,      # Xóa Project → xóa luôn Task
        related_name="tasks",          # project.tasks.all() – chiều ngược
        null=True, blank=True,
    )

    # ── Meta = Cấu hình bảng ──
    class Meta:
        db_table = "task"              # Tên bảng trong DB
        ordering = ["-created_at"]     # Sắp xếp mặc định

    # ── __str__ = Tên hiển thị ──
    def __str__(self):
        return self.title              # Admin/shell hiện "Học Django" thay vì "Task object (1)"
```

**Nhớ nhanh các field type:**

```txt
CharField(max_length=N)    → Chuỗi ngắn (VARCHAR)
TextField()                → Chuỗi dài (TEXT)
IntegerField()             → Số nguyên (INT)
BooleanField()             → True/False
DateField()                → Ngày (YYYY-MM-DD)
DateTimeField()            → Ngày + giờ
EmailField()               → CharField + validate email
ForeignKey()               → Khóa ngoại (N-1)
ManyToManyField()          → Quan hệ N-N
OneToOneField()            → Quan hệ 1-1
```

**Nhớ nhanh field options:**

```txt
null=True       → DB cho phép NULL (dùng cho Date, FK, Int...)
blank=True      → Form/API cho phép để trống (validation level)
default=value   → Giá trị mặc định
unique=True     → Không trùng trong toàn bảng
choices=[...]   → Giới hạn giá trị hợp lệ
related_name="" → Tên truy cập chiều ngược (project.tasks.all())
```

> **Dù Template hay DRF**, `models.py` viết **y hệt nhau**. Đây là phần không đổi.

---

## 5. `migrations/` – "Lịch Sử Thay Đổi Database"

Migration = file ghi lại mỗi lần bạn thay đổi `models.py` → Django dùng nó để update bảng DB.

### Quy trình 2 bước

```txt
Bước 1: Bạn sửa models.py (thêm field, đổi tên, xóa field...)
            ↓
Bước 2: python manage.py makemigrations
            ↓
        Django tạo file migration: tasks/migrations/0003_add_priority_field.py
        File này MÔ TẢ thay đổi (chưa chạy vào DB)
            ↓
Bước 3: python manage.py migrate
            ↓
        Django ĐỌC file migration → chạy ALTER TABLE/CREATE TABLE vào DB
```

### Các lệnh cần nhớ

```bash
# Tạo file migration từ thay đổi models.py
python manage.py makemigrations

# Chạy migration vào DB
python manage.py migrate

# Xem danh sách migration + trạng thái (đã chạy / chưa chạy)
python manage.py showmigrations

# Xem SQL mà migration sẽ chạy (debug)
python manage.py sqlmigrate tasks 0003
```

### Ví dụ thực tế

```python
# Trước: models.py
class Task(models.Model):
    title = models.CharField(max_length=200)

# Sau: thêm field priority
class Task(models.Model):
    title = models.CharField(max_length=200)
    priority = models.CharField(max_length=10, default="medium")  # MỚI
```

```bash
$ python manage.py makemigrations
# → tasks/migrations/0003_task_priority.py  (file được tạo)

$ python manage.py migrate
# → ALTER TABLE task ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
```

### Lỗi hay gặp

```txt
❌ Sửa models.py nhưng quên makemigrations → DB không đổi → lỗi "column not found"
❌ makemigrations nhưng quên migrate → file migration có nhưng DB chưa update
❌ Xóa file migration rồi migrate → Django bị lệch state → phải fake hoặc reset
```

> **Dù Template hay DRF**, migration hoạt động **y hệt nhau**. Đây là phần không đổi.

---

## 6. `apps.py` – "CMND Của App"

File nhỏ nhưng quan trọng – khai báo metadata của app:

```python
# tasks/apps.py
from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"   # Kiểu ID mặc định
    name = "tasks"                                          # Tên app (phải khớp folder)
    verbose_name = "Quản lý công việc"                     # Tên hiển thị trong Admin
```

Khi khai báo trong `INSTALLED_APPS`, có thể viết:

```python
INSTALLED_APPS = [
    "tasks",                          # Django tự tìm TasksConfig
    # hoặc
    "tasks.apps.TasksConfig",         # Chỉ rõ config class
]
```

---

## 7. `admin.py` – "Trang Quản Trị"

Đăng ký model để quản lý data qua giao diện web `/admin/`:

```python
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "project", "created_at"]    # Cột hiện
    list_filter = ["status", "project"]                            # Bộ lọc bên phải
    search_fields = ["title"]                                      # Ô tìm kiếm
    list_per_page = 20                                             # Phân trang
```

> **Với DRF**, Admin vẫn có giá trị: dùng để xem/sửa data nhanh khi debug, không cần viết API.

---

## 8. Tổng Hợp: Request Đi Từ Đâu Đến Đâu

```txt
Client gửi: GET /tasks/5/
                ↓
┌─────────────────────────────────────────────────┐
│  settings.py                                     │
│  ROOT_URLCONF = "todo_project.urls"              │
│  MIDDLEWARE = [Security, Session, Auth, CSRF]    │
│  DATABASES = {mysql...}                          │
│  INSTALLED_APPS = [tasks, projects, ...]         │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  todo_project/urls.py                            │
│  path("tasks/", include("tasks.urls"))           │
│         ↓ match "tasks/" → chuyển vào app        │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  tasks/urls.py                                   │
│  path("<int:pk>/", views.task_detail)             │
│         ↓ match "5/" → pk=5                      │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  tasks/views.py                                  │
│  def task_detail(request, pk):                   │
│      task = get_object_or_404(Task, pk=pk)       │  ← ORM query
│      ...                                         │
│                                                  │
│  Template: return render(request, "detail.html") │  ← Cách cũ
│  DRF:      return Response(serializer.data)      │  ← Cách mới
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  tasks/models.py (+ migrations/)                 │
│  class Task(models.Model):                       │
│      title = models.CharField(max_length=200)    │
│      project = models.ForeignKey(Project, ...)   │
│                                                  │
│  DB: SELECT * FROM task WHERE id = 5             │
└─────────────────────────────────────────────────┘
```

---

## 9. Checklist Tự Kiểm Tra

> Tự trả lời trước, rồi click **"👉 Xem đáp án"** để kiểm tra.

---

### Câu 1: Project vs App khác nhau thế nào?

<details>
<summary>👉 Xem đáp án</summary>

**Project** = Toàn bộ dự án. Chứa cấu hình chung (`settings.py`, `urls.py` tổng, `manage.py`). Mỗi dự án chỉ có **1 Project**.

**App** = Một module chức năng cụ thể (`tasks/`, `projects/`). Chứa logic riêng (`models.py`, `views.py`, `urls.py`). Một Project có **nhiều App**.

```txt
todo_project/          ← Project (1 cái duy nhất)
├── todo_project/      ← Config: settings.py, urls.py tổng
├── tasks/             ← App #1: quản lý task
└── projects/          ← App #2: quản lý project
```

> Nhớ: Project = "Công ty". App = "Phòng ban".

</details>

---

### Câu 2: App mới tạo xong phải làm gì trong `settings.py`?

<details>
<summary>👉 Xem đáp án</summary>

**Thêm tên app vào `INSTALLED_APPS`:**

```python
INSTALLED_APPS = [
    # ...
    "tasks",       # ← Thêm dòng này
]
```

Nếu quên → Django **không nhận ra** app đó. Model không tạo bảng, migration không chạy, template không tìm thấy.

</details>

---

### Câu 3: `ROOT_URLCONF` dùng để làm gì?

<details>
<summary>👉 Xem đáp án</summary>

Chỉ cho Django biết **file urls.py nào là điểm bắt đầu** khi có request đến:

```python
ROOT_URLCONF = "todo_project.urls"
```

Nghĩa là: mỗi request đến, Django đọc file `todo_project/urls.py` **đầu tiên**, rồi từ đó `include()` vào các app urls.

```txt
Request đến → Django hỏi: "ROOT_URLCONF ở đâu?"
           → Mở todo_project/urls.py
           → Match URL pattern → chuyển vào app tương ứng
```

</details>

---

### Câu 4: Request đi từ root urls.py vào app urls.py như thế nào?

<details>
<summary>👉 Xem đáp án</summary>

Bằng hàm `include()`:

```python
# Root: todo_project/urls.py
urlpatterns = [
    path("tasks/", include("tasks.urls")),      # "tasks/" → chuyển sang tasks/urls.py
]

# App: tasks/urls.py
urlpatterns = [
    path("", views.task_list, name="list"),           # Match /tasks/
    path("<int:pk>/", views.task_detail, name="detail"),  # Match /tasks/5/
]
```

Khi user truy cập `/tasks/5/`:
1. Root urls.py: match `"tasks/"` → cắt bỏ phần `tasks/`, chuyển phần còn lại `"5/"` sang `tasks/urls.py`
2. App urls.py: match `"<int:pk>/"` → `pk=5` → gọi `views.task_detail(request, pk=5)`

</details>

---

### Câu 5: `<int:pk>` trong URL pattern nghĩa là gì?

<details>
<summary>👉 Xem đáp án</summary>

Đó là **path converter** – bắt một phần URL và chuyển thành tham số cho view:

```python
path("<int:pk>/", views.task_detail)
#     ^^^  ^^
#     |    └── Tên biến (truyền vào view)
#     └─────── Kiểu dữ liệu (int = số nguyên)
```

Khi URL là `/tasks/5/`:
- `<int:pk>` bắt giá trị `5`
- View nhận: `def task_detail(request, pk=5)`

Các converter có sẵn:

```txt
<int:pk>        → Số nguyên:  /tasks/5/
<str:slug>      → Chuỗi:     /posts/hello-world/
<slug:slug>     → Slug:      /posts/hello-world-123/
<uuid:id>       → UUID:      /items/550e8400-e29b-41d4-a716-446655440000/
```

</details>

---

### Câu 6: `null=True` khác `blank=True` chỗ nào?

<details>
<summary>👉 Xem đáp án</summary>

**Khác nhau ở tầng hoạt động:**

| | `null=True` | `blank=True` |
|:--|:--|:--|
| **Tầng** | Database | Validation (Form/Serializer) |
| **Ý nghĩa** | Cho phép lưu `NULL` trong DB | Cho phép gửi giá trị rỗng |
| **Không có** | DB bắt buộc `NOT NULL` | Form/API bắt buộc phải điền |

```python
# Trường hợp thường gặp:
bio = models.TextField(blank=True)                   # Chuỗi rỗng "" trong DB, form cho bỏ trống
due_date = models.DateField(null=True, blank=True)   # NULL trong DB, form cho bỏ trống
title = models.CharField(max_length=200)             # NOT NULL, form bắt buộc điền
```

**Quy tắc nhớ:**
- `CharField` / `TextField` → dùng `blank=True` (lưu `""` thay vì `NULL`)
- `DateField`, `IntegerField`, `ForeignKey`... → dùng `null=True, blank=True` (lưu `NULL`)

</details>

---

### Câu 7: `related_name` dùng để làm gì?

<details>
<summary>👉 Xem đáp án</summary>

Đặt **tên truy cập chiều ngược** cho quan hệ ForeignKey:

```python
class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
```

```python
# Chiều thuận (từ Task → Project):
task.project              # Lấy project của task

# Chiều ngược (từ Project → tất cả Task):
project.tasks.all()       # Lấy tất cả task thuộc project
#       ^^^^^
#       related_name
```

Nếu **không đặt** `related_name`, Django tự tạo tên mặc định:

```python
project.task_set.all()    # tên_model_viết_thường + _set
```

> `related_name="tasks"` tự nhiên và chuyên nghiệp hơn `task_set`.

</details>

---

### Câu 8: `makemigrations` khác `migrate` như thế nào?

<details>
<summary>👉 Xem đáp án</summary>

**2 bước riêng biệt:**

| Lệnh | Làm gì | Kết quả |
|:------|:-------|:--------|
| `makemigrations` | Đọc `models.py`, **tạo file migration** mô tả thay đổi | File `.py` trong `migrations/` |
| `migrate` | Đọc file migration, **chạy SQL vào DB** | Bảng/cột trong database được tạo/sửa |

```txt
models.py thay đổi
        ↓
makemigrations   →  tạo file: migrations/0003_add_priority.py (chưa đụng DB)
        ↓
migrate          →  chạy SQL: ALTER TABLE task ADD COLUMN priority... (DB thay đổi)
```

**Ví von:** `makemigrations` = viết đơn xin sửa nhà. `migrate` = thợ xây đến sửa thật.

</details>

---

### Câu 9: Middleware xử lý request ở thời điểm nào?

<details>
<summary>👉 Xem đáp án</summary>

**Trước và sau View:**

```txt
Client Request
    ↓
┌── Middleware (lượt đi) ──┐
│  SecurityMiddleware       │  ← Check bảo mật
│  SessionMiddleware        │  ← Gắn session vào request
│  AuthenticationMiddleware │  ← Gắn request.user
│  CsrfViewMiddleware      │  ← Check CSRF token
└───────────┬───────────────┘
            ↓
      ★ VIEW xử lý ★
            ↓
┌── Middleware (lượt về) ──┐
│  (Đi ngược lại)          │  ← Xử lý response trước khi trả client
└───────────┬───────────────┘
            ↓
Client Response
```

**Nhớ:** Request đi qua middleware **trước** khi đến view. Response đi qua middleware **sau** khi view trả về. Thứ tự trong `MIDDLEWARE` list = thứ tự xử lý.

</details>

---

### Câu 10: Sửa models.py xong mà quên chạy migration thì sao?

<details>
<summary>👉 Xem đáp án</summary>

**Lỗi xảy ra khi runtime:** Code Python nói field `priority` tồn tại, nhưng DB chưa có cột đó.

```txt
Triệu chứng:
→ OperationalError: (1054, "Unknown column 'priority' in 'field list'")
→ ProgrammingError: column "priority" does not exist
```

**Cách fix:**

```bash
# Bước 1: Tạo migration
python manage.py makemigrations

# Bước 2: Chạy vào DB
python manage.py migrate
```

**Kiểm tra trạng thái:**

```bash
python manage.py showmigrations
# [X] = đã chạy, [ ] = chưa chạy
# tasks
#  [X] 0001_initial
#  [X] 0002_add_status
#  [ ] 0003_add_priority     ← Chưa chạy! Cần migrate
```

> **Tip:** Mỗi lần sửa `models.py`, **luôn chạy 2 lệnh** ngay: `makemigrations` → `migrate`. Đừng để dồn.

</details>

---

> ✅ **Nếu hiểu được cả 10 câu** → bạn đã sẵn sàng sang Phase 1 (ORM).


