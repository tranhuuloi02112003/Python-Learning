# 07. Django & Database Migration

## 1. Lệnh `python manage.py migrate` là gì?

Lệnh này có bản chất là **đồng bộ hóa các Model trong code vào cơ sở dữ liệu thật** — tức là thực thi các file Migration để cập nhật cấu trúc Database (tạo bảng, sửa cột, thêm khóa ngoại...).

- **So sánh với Java (Spring Boot):** Tương tự như khi bạn dùng **Liquibase** hoặc **Flyway** để quản lý DB versioning.

### Phân tích cú pháp lệnh

| Thành phần | Vai trò |
|---|---|
| `python` | Trình thông dịch — dùng để chạy file `.py` |
| `manage.py` | File script điều hướng của Django (nằm trong thư mục gốc của dự án) |
| `migrate` | Lệnh con — bảo Django: *"Hãy đồng bộ hóa các Model trong code vào Database thật đi"* |

---



## 3. Quy trình Migration trong Django (Khác với Java)

Trong Java, bạn thường viết SQL thẳng hoặc file XML cho Flyway. Trong Django, quy trình theo hướng **"Code First"** — bạn viết Model bằng Python, Django tự sinh SQL.

### Hai bước bắt buộc

**Bước 1 — `python manage.py makemigrations`**
- Django quét các **Class (Model)** bạn vừa sửa/tạo trong `models.py`.
- Tự động tạo ra một **file script trung gian** (file `.py` trong thư mục `migrations/`).
- File này chứa toàn bộ thông tin về thay đổi cấu trúc DB (ví dụ: thêm cột, đổi tên bảng...).

**Bước 2 — `python manage.py migrate`**
- Django đọc các file script trong `migrations/` chưa được chạy.
- Thực thi SQL tương ứng lên Database.

### Sơ đồ luồng

```
Sửa models.py
      │
      ▼
makemigrations  →  Tạo file migrations/0001_initial.py  (file .py trung gian)
      │
      ▼
   migrate      →  Thực thi SQL lên Database  (bảng/cột được tạo thật)
```

---

## 4. So sánh với Java (Spring Boot)

| Tiêu chí | Django (Python) | Spring Boot (Java) |
|---|---|---|
| Phong cách | Code First (viết Model → sinh migration) | DB First hoặc Code First tùy công cụ |
| Công cụ quản lý | Django Migration (tích hợp sẵn) | Flyway hoặc Liquibase (thêm dependency) |
| File migration | File `.py` tự động sinh | File `.sql` hoặc `.xml` viết tay |
| Lệnh thực thi | `python manage.py migrate` | Tích hợp tự chạy khi start app (Flyway) |

---

## 5. Tổng kết

- **Thuộc về:** Django Framework (Python)
- **Mục đích:** Cập nhật cấu trúc Database từ code Model sang DB thật
- **Liên quan Docker:** Docker chỉ là "môi trường" thực thi lệnh này để tự động hóa quá trình triển khai — không phải điều kiện bắt buộc

### Luồng làm việc chuẩn

```bash
# 1. Sửa hoặc tạo Model trong models.py
# 2. Tạo file migration
python manage.py makemigrations

# 3. Áp dụng thay đổi vào Database
python manage.py migrate
```

---

## 6. Những câu hỏi quan trọng để hiểu sâu về Django

---

### 6.1 Migration Conflict là gì?

**Migration conflict** xảy ra khi **2 người cùng chạy `makemigrations`** từ cùng một file migration gốc, khiến Django tạo ra 2 file có cùng "cha" — tạo nên nhánh tách đôi trong lịch sử migration.

#### Ví dụ tình huống thực tế

```
# Trên main branch: file cuối cùng là
migrations/0003_add_status.py

# Dev A thêm field "priority" → chạy makemigrations
migrations/0004_add_priority.py   ← cha là 0003

# Dev B thêm field "due_date" → chạy makemigrations
migrations/0004_add_due_date.py   ← cha cũng là 0003 ← CONFLICT!
```

Khi merge code lên Git, Django thấy **2 file đều kế thừa từ 0003** → báo lỗi:

```
CommandError: Conflicting migrations detected; multiple leaf nodes
in the migration graph: (0004_add_priority, 0004_add_due_date).
```

#### Cách giải quyết

```bash
# Django tự tạo file "merge" để hợp 2 nhánh lại
python manage.py makemigrations --merge

# File mới được tạo ra:
migrations/0005_merge_0004_add_priority_0004_add_due_date.py
```

> **Quy tắc nhóm:** Sau khi merge, chạy `migrate` để đồng bộ. Nên **communicate** trong team trước khi sửa cùng một model.

---

### 6.2 Flag `--fake` trong `migrate` dùng để làm gì?

`--fake` báo Django: **"Hãy đánh dấu migration này là đã chạy, nhưng ĐỪNG thực sự thay đổi Database."**

#### Khi nào dùng?

| Tình huống | Giải thích |
|---|---|
| Import DB từ bên ngoài (dump SQL) | DB đã có đúng cấu trúc, nhưng Django chưa biết |
| Sửa thủ công DB trực tiếp | Bạn đã `ALTER TABLE` bằng tay, cần Django "công nhận" |
| Reset trạng thái migration sai | Đánh dấu lại điểm xuất phát mà không mất data |

#### Ví dụ thực tế

```bash
# Tình huống: bạn restore một DB backup đã có đầy đủ bảng,
# nhưng bảng django_migrations trống (Django không biết).

# SAI: chạy migrate bình thường sẽ lỗi "table already exists"
python manage.py migrate

# ĐÚNG: fake toàn bộ migrations để Django ghi nhận
python manage.py migrate --fake

# Hoặc fake từ một app cụ thể đến một điểm cụ thể
python manage.py migrate myapp 0003 --fake
```

> ⚠️ **Cẩn thận:** `--fake` chỉ ghi vào bảng `django_migrations`, không chạm vào cấu trúc DB thật. Dùng sai có thể khiến DB và code bị lệch nhau.

---

### 6.3 `squashmigrations` là gì?

Theo thời gian, thư mục `migrations/` có thể tích lũy **hàng trăm file** — mỗi lần sửa model là thêm 1 file. `squashmigrations` **gộp nhiều file migration thành 1 file duy nhất** để tối ưu.

#### Khi nào nên dùng?

- Dự án đã chạy lâu, có > 50 file migration trong 1 app.
- Thời gian chạy `migrate` khi deploy lên server mới ngày càng chậm.
- Cần "dọn dẹp" lịch sử migration cho gọn.

#### Cú pháp

```bash
# Gộp tất cả migration từ 0001 đến 0050 thành 1 file
python manage.py squashmigrations myapp 0001 0050

# Kết quả: tạo ra file mới
migrations/0001_squashed_0050_...py
```

#### Quy trình chuẩn sau khi squash

```
1. Chạy squashmigrations  →  file squashed được tạo
2. Commit file squashed lên Git
3. Deploy lên tất cả server, chạy migrate
4. Xóa các file cũ (0001 → 0050) sau khi xác nhận tất cả server đã migrate
5. Commit lần 2 xóa file cũ
```

> **Lưu ý:** Không xóa file cũ ngay vì các server khác có thể chưa chạy đến điểm squash.

---

### 6.4 `on_delete=CASCADE` vs `on_delete=SET_NULL` trong ForeignKey

Khi bạn xóa một **bản ghi cha** (parent record), Django cần biết làm gì với các **bản ghi con** (child records) đang trỏ vào nó.

#### So sánh trực quan

```python
# Ví dụ: Task thuộc về một Project
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # Nếu Project bị xóa → Task cũng bị xóa theo

class Task(models.Model):
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    # Nếu Project bị xóa → Task.project được set thành NULL (Task vẫn còn)
```

#### Bảng so sánh đầy đủ

| `on_delete` | Hành động khi xóa Parent | Dùng khi nào |
|---|---|---|
| `CASCADE` | Xóa luôn tất cả Child | Child không có nghĩa nếu không có Parent (VD: OrderItem → Order) |
| `SET_NULL` | Child.fk = NULL | Child vẫn có nghĩa độc lập (VD: Task → Project đã xóa) |
| `PROTECT` | Ném lỗi, ngăn xóa Parent | Muốn bảo vệ dữ liệu, bắt buộc xóa child trước |
| `SET_DEFAULT` | Child.fk = default value | Có giá trị mặc định hợp lý |
| `DO_NOTHING` | Không làm gì (nguy hiểm!) | Hiếm gặp, tự xử lý ở tầng DB |
| `RESTRICT` | Tương tự PROTECT nhưng thông minh hơn | Django 3.1+, kiểm tra cả cascade chain |

#### Ví dụ trong Todo Project

```python
class Task(models.Model):
    # Xóa Project → Xóa luôn các Task trong Project đó
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
```

---

### 6.5 Django ORM với nhiều Database cùng lúc

**Có!** Django hỗ trợ **multi-database** hoàn toàn, thông qua setting `DATABASES` và **Database Routers**.

#### Cấu hình trong `settings.py`

```python
DATABASES = {
    # Database mặc định (primary)
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'main_db',
    },
    # Database phụ (analytics, read replica...)
    'analytics': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'analytics_db',
    },
}
```

#### Cách dùng trong code

```python
# Chỉ định rõ database khi query
tasks = Task.objects.using('analytics').filter(status='done')

# Hoặc khi save
report = Report(title="Monthly")
report.save(using='analytics')
```

#### Database Router — Tự động điều hướng

```python
# routers.py
class AnalyticsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'analytics':
            return 'analytics'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'analytics':
            return 'analytics'
        return 'default'

# settings.py
DATABASE_ROUTERS = ['myapp.routers.AnalyticsRouter']
```

#### Chạy migrate cho từng database

```bash
# Migrate database mặc định
python manage.py migrate

# Migrate database phụ
python manage.py migrate --database=analytics
```

#### Ứng dụng thực tế

| Use Case | Giải pháp |
|---|---|
| Read Replica (giảm tải) | Đọc từ replica, ghi vào primary |
| Multi-tenant (mỗi khách một DB) | Router dựa trên request context |
| Tách DB Analytics | Ghi log/report riêng, không ảnh hưởng DB chính |

## 7. Gợi ý lộ trình học Django tiếp theo

- **Cơ bản:** Model, View, Template (MVT Pattern), URL routing, Django Admin.
- **Trung cấp:** Django REST Framework (DRF), Serializer, Authentication (Token/JWT).
- **Nâng cao:** Celery (background tasks), Django Channels (WebSocket), Custom Management Commands.
