# Django Runserver & Common Commands

## 0. `python` vs `python3` & `manage.py`

### `python` hay `python3`?

- **Bản chất:** Trên Mac/Linux hiện đại, lệnh `python3` là gọi đích danh Python phiên bản 3.
- **Phép thuật của `venv`:** Một khi bạn đã kích hoạt môi trường ảo (hiện chữ `(.venv)` ở đầu terminal), hệ thống đã ngầm tự động trỏ lệnh `python` về đúng `python3`. Vậy nên, khi ở trong `venv`, bạn cứ gõ `python` cho ngắn gọn nhé!

### File `manage.py` là gì?

Hãy coi `manage.py` nằm ở thư mục ngoài cùng của bạn như một cái **Điều khiển từ xa (Remote Control)** của dự án. Bản thân nó không làm gì cả, nó chỉ chờ bạn bấm nút lệnh từ Terminal.

- **Công thức chuẩn:** `[Gọi ngôn ngữ Python] chạy file [Điều khiển manage.py] với [Tên lệnh]`

---

## 1. Lệnh `runserver` là gì?

Lệnh `python manage.py runserver [port]` được dùng để khởi chạy **Development Server**. Đây là một web server nhẹ, tích hợp sẵn giúp lập trình viên kiểm tra code nhanh chóng.

### Phân tích cú pháp:

- **`python manage.py runserver`**: Chạy mặc định tại `http://127.0.0.1:8000/`.
- **`python manage.py runserver 8080`**: Thay đổi cổng (port) thành 8080.
- **`python manage.py runserver 0.0.0.0:8000`**:
  - Lắng nghe trên mọi IP (thường dùng trong **Docker**).
  - Giúp các thiết bị khác trong cùng mạng hoặc máy Host (nếu chạy Docker) có thể truy cập vào.

> **[IMPORTANT]**
> Không bao giờ dùng `runserver` cho môi trường thực tế (Production). Nó không an toàn và không chịu được tải lớn. Hãy dùng **Gunicorn** hoặc **Uvicorn**.

---

## 2. Các lệnh khởi tạo (Dùng 1 lần khi bắt đầu)

| Lệnh                              | Chức năng                | Lưu ý                                                                        |
| --------------------------------- | ------------------------ | ---------------------------------------------------------------------------- |
| `django-admin startproject [tên]` | Tạo bộ khung dự án mới   | Chạy lệnh này khi bạn chưa có gì cả. Nó sinh ra file `manage.py`.            |
| `python manage.py startapp [tên]` | Tạo một module (app) mới | Một dự án lớn nên chia thành nhiều App nhỏ (ví dụ: `blog`, `users`, `cart`). |

## 3. Các lệnh vận hành thường xuyên (Daily Commands)

| Nhóm           | Lệnh              | Chức năng                                                |
| -------------- | ----------------- | -------------------------------------------------------- |
| **Khởi chạy**  | `runserver`       | Chạy server demo để xem kết quả code.                    |
| **Database**   | `makemigrations`  | Tạo file kịch bản thay đổi DB dựa trên Model.            |
|                | `migrate`         | Áp dụng thay đổi vào Database thật.                      |
| **Quản trị**   | `createsuperuser` | Tạo tài khoản admin có quyền cao nhất.                   |
| **Phát triển** | `startapp [tên]`  | Tạo một module/app mới trong project.                    |
|                | `shell`           | Vào môi trường tương tác Python để test code nhanh.      |
| **Deployment** | `collectstatic`   | Tập hợp tất cả CSS/JS/Images vào thư mục tĩnh để deploy. |

### Tiêu điểm: Lệnh `createsuperuser`

Đây là lệnh tương tác. Khi bạn chạy, Django sẽ hỏi bạn từng thông tin một:

```bash
python manage.py createsuperuser
```

**Kết quả trên Terminal sẽ như sau:**

1. `Username`: (Nhập tên admin, ví dụ: `admin`)
2. `Email address`: (Có thể để trống và nhấn Enter)
3. `Password`: (Nhập mật khẩu - **Lưu ý:** Khi nhập mật khẩu, màn hình sẽ không hiện dấu `*` hay ký tự nào, bạn cứ nhập bình thường rồi nhấn Enter)
4. `Password (again)`: (Nhập lại mật khẩu)
5. `Superuser created successfully.`

### Kiểm tra & Debug Migration

Khi bạn gặp lỗi về Database, 2 lệnh này là "cứu cánh":

- **`python manage.py showmigrations`**:
  - Hiển thị danh sách tất cả các file migration.
  - Những file có dấu `[X]` là đã chạy thành công, dấu `[ ]` là chưa chạy.
- **`python manage.py sqlmigrate [app_name] [migration_number]`**:
  - Ví dụ: `python manage.py sqlmigrate users 0001`
  - Nó sẽ không chạy gì cả, mà chỉ **hiển thị câu lệnh SQL** (CREATE TABLE...) mà nó định chạy. Rất hữu ích khi bạn muốn copy SQL này gửi cho đội DBA (Database Administrator).

---

## 4. Các lệnh Python cơ bản cho Backend Engineer

### Quản lý Dependencies (Thư viện)

Trong Java bạn dùng Maven/Gradle, trong Python bạn dùng `pip`:

- `pip install django`: Cài đặt thư viện Django.
- `pip freeze > requirements.txt`: Ghi lại toàn bộ thư viện và version vào file (giống file `pom.xml`).
- `pip install -r requirements.txt`: Cài đặt mọi thứ từ file có sẵn (dùng khi clone dự án về).

### Quản lý môi trường (Virtual Environment)

Để tránh tình trạng Project A cài Django 3, Project B cài Django 4 gây xung đột:

- `python -m venv venv`: Tạo môi trường ảo tên là `venv`.
- `source venv/bin/activate` (Mac/Linux) hoặc `venv\Scripts\activate` (Windows): Kích hoạt môi trường ảo.

---

## 4. Mẹo nhỏ (Pro-tips)

### Tự động load code (Hot Reload)

Lệnh `runserver` có tính năng **Auto-reload**. Mỗi khi bạn nhấn `Ctrl + S` (Save) file code, server sẽ tự khởi động lại để cập nhật thay đổi. Bạn không cần phải tắt đi bật lại thủ công.

### Kiểm tra lỗi cấu trúc

Trước khi chạy, bạn có thể dùng:

```bash
python manage.py check
```

Lệnh này sẽ quét toàn bộ dự án để tìm các lỗi cấu hình tiềm ẩn mà không cần chạy server.

### Đổi mật khẩu Admin

Nếu quên mật khẩu admin đã tạo:

```bash
python manage.py changepassword [username]
```
