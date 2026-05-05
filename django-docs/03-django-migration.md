# Django & Database Migration

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

## 2. Tại sao hay thấy nó đi chung với Docker?

Khi đóng gói ứng dụng Backend vào Docker, lệnh này thường được viết trong `docker-compose.yml` hoặc `Dockerfile` (phần `entrypoint` hoặc `cmd`) để **tự động hóa** quá trình triển khai.

**Mục tiêu:** Mỗi khi Container khởi chạy, Database sẽ tự động được cập nhật lên phiên bản mới nhất mà không cần thao tác thủ công.

> **Lưu ý:** Bạn hoàn toàn có thể chạy lệnh này trên máy local (không cần Docker) nếu đã cài Python và Django.

### Ví dụ cấu hình trong `docker-compose.yml`

```yaml
services:
  web:
    build: .
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    depends_on:
      - db
  db:
    image: postgres:15
```

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

- **Migration conflict** là gì và xảy ra khi nào (làm việc nhóm nhiều người cùng sửa model)?
- **`--fake` flag** trong `migrate` dùng để làm gì?
- **`squashmigrations`** là gì và khi nào nên dùng để tối ưu số lượng file migration?
- Sự khác biệt giữa **`on_delete=CASCADE`** và **`on_delete=SET_NULL`** trong Django ForeignKey?
- Django ORM có thể hoạt động với **nhiều database** cùng lúc không?

## 7. Gợi ý lộ trình học Django tiếp theo

- **Cơ bản:** Model, View, Template (MVT Pattern), URL routing, Django Admin.
- **Trung cấp:** Django REST Framework (DRF), Serializer, Authentication (Token/JWT).
- **Nâng cao:** Celery (background tasks), Django Channels (WebSocket), Custom Management Commands.
