# Giải Phẫu Django Admin Panel & Quản Trị Hệ Thống

Django cung cấp sẵn một công cụ cực kỳ mạnh mẽ mang tên **Admin Panel** (trang quản trị). Nó được sinh ra để bạn không phải tự code giao diện quản lý dữ liệu (CRUD) từ con số 0.

---

## 1. Lệnh `createsuperuser` là gì?

Lệnh `python manage.py createsuperuser` là cách để bạn tạo ra một **"Chúa tể hệ thống" (Superuser)**.

- **Bản chất:** Nó tạo 1 user mới và lưu vào bảng `auth_user` (hoặc custom user model) trong Database.
- **Quyền lực:** User này được cấp cờ `is_superuser=True` và `is_staff=True`. Nghĩa là nó có quyền đăng nhập vào đường dẫn `/admin/` và thao tác với mọi dữ liệu, mọi quyền hạn trong hệ thống mà không bị cản trở.
- **Mục đích:** Giúp bạn có tài khoản "chủ nhà" để setup dữ liệu ban đầu, quản lý tài khoản thành viên, và phân quyền mà không cần tự viết UI quản lý user.

---

## 2. Giải phẫu Giao diện (UI) Django Admin

Khi bạn truy cập `http://127.0.0.1:8000/admin/`, bạn sẽ thấy một "Back-office" được thiết kế rất khoa học dành cho admin/ops/support. Dưới đây là phân tích cấu trúc UI của nó:

### A. Dashboard (Bảng điều khiển chính)

- **Cấu trúc:** Phân chia rõ ràng theo từng **App** (ví dụ: `Tasks`, `Authentication and Authorization`). Mỗi App sẽ chứa các **Models** (bảng dữ liệu) bên trong.
- **Chức năng:** Giúp bạn nhìn tổng quan hệ thống có những luồng dữ liệu nào và thao tác nhanh để Thêm mới (Add) hoặc Đổi (Change).

### B. List View (Màn hình danh sách)

- Khi click vào một Model (vd: `Tasks`), bạn sẽ thấy màn hình danh sách các bản ghi (records).
- **UI Mặc định:** Chỉ hiển thị 1 cột duy nhất là tên object (dựa vào hàm `__str__` bạn định nghĩa trong file `models.py`).
- **Sức mạnh ngầm:** Bạn có thể dễ dàng biến màn hình này thành một bảng dữ liệu chuyên nghiệp với tính năng Lọc (Filter), Tìm kiếm (Search), Sắp xếp (Sort) chỉ bằng vài dòng code trong `admin.py`.

### C. Change Form (Màn hình Thêm/Sửa)

- Khi bấm vào nút "Thêm" hoặc click vào một bản ghi, Django tự động đọc cấu trúc Model và sinh ra Form nhập liệu tương ứng.
- **Sự thông minh:** Django tự động chọn giao diện form (UI Widget) phù hợp với kiểu dữ liệu của Database:
  - `BooleanField` -> Hiện ô Checkbox.
  - `DateTimeField` -> Hiện Bảng chọn ngày tháng (Date/Time picker) và nút "Today", "Now".
  - `ForeignKey` -> Hiện Menu thả xuống (Dropdown) để chọn khóa ngoại.

---

## 3. Cách "Độ" (Customize) Giao diện Admin

Để Admin Panel đẹp, hữu dụng và hiển thị nhiều thông tin thay vì chỉ 1 cột mặc định, bạn phải cấu hình trong file `admin.py` của từng App.

**Ví dụ cấu hình cho bảng Task:**

```python
from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    # 1. Các cột muốn hiển thị thành bảng
    list_display = ('title', 'completed', 'created_at')

    # 2. Tạo bộ lọc bên tay phải màn hình
    list_filter = ('completed', 'created_at')

    # 3. Thêm thanh tìm kiếm ở trên cùng
    search_fields = ('title',)

    # 4. Có thể click vào checkbox 'completed' để sửa trực tiếp ngoài danh sách
    list_editable = ('completed',)

# Đăng ký Model đi kèm với class cấu hình
admin.site.register(Task, TaskAdmin)
```

---

## 4. Phân tích việc có nên dùng Django Admin không?

Mặc dù nó không phải trang dành cho người dùng cuối (end-user), nó giúp công ty tiết kiệm hàng tháng trời code chức năng quản trị nội bộ.

- **Dự án Todo:** Không cần viết màn hình "Quản lý Task" riêng cho Admin, cứ vào `/admin/` để xem/sửa Task trực tiếp.
- **Hệ thống HR (ví dụ: Workify):** Support có thể vào chỉnh sửa dữ liệu lỗi, tạo account, kiểm tra record.

### Quy tắc "Kỷ luật thép" khi đưa Admin lên Production:

Vì giao diện này có quyền lực chạm thẳng vào Database, các công ty áp dụng các quy tắc bảo mật nghiêm ngặt sau:

1.  **Đổi URL:** Không dùng `/admin/` mặc định (để tránh bot quét). Thường đổi thành tên khó đoán như `/secure-backend-admin/`.
2.  **Giới hạn truy cập mạng:** Bắt buộc phải kết nối VPN công ty hoặc chỉ cho phép các IP nội bộ mới mở được trang này.
3.  **Bật 2FA:** Xác thực 2 bước (Mật khẩu + Mã OTP điện thoại qua plugin hoặc SSO).
4.  **Bắt buộc dùng HTTPS:** Để chống bị nghe lén mật khẩu khi truyền qua mạng.
5.  **Phân quyền chặt chẽ (Permissions):**
    - Không phải ai cũng là `Superuser`.
    - Nhân viên Support/Ops chỉ được cấp tài khoản `Staff` với quyền hạn giới hạn thông qua cơ chế Group và Permission (Ví dụ: Chỉ có quyền Xem và Sửa Task, bị cấm Xóa).

> **Tổng kết:** Django Admin là một "vũ khí hạng nặng" dạng Back-office. Nó sinh ra để Quản trị viên điều hành hệ thống dữ liệu một cách trực quan, nhanh chóng và cực kỳ tiết kiệm chi phí phát triển.
