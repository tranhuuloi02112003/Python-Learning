# Lộ trình học Web Fullstack "Cổ điển" (Django + Django Templates)

Đây là lộ trình hoàn hảo nhất dành cho người mới bắt đầu làm Web với Python. Bằng cách sử dụng **Django Templates**, bạn sẽ tự tay xây dựng được một trang web hoàn chỉnh (cả Backend lẫn Frontend) mà không cần phải cài đặt quá nhiều công cụ phức tạp.

Để làm được một dự án hoàn chỉnh (có Thêm, Sửa, Xóa, Đăng nhập...), bạn cần đi qua các cột mốc sau:

---

## 1. Hiểu kiến trúc M-V-T (Model - View - Template)
Đây là "linh hồn" của Django. Mọi luồng xử lý đều đi qua 3 trạm này.
*   **Urls (Routing):** Nhận link từ người dùng (vd: `/home/`) và chuyển cho View xử lý.
*   **V (View):** Bộ não. Chứa code Python logic. Nhận request, hỏi Database, và ném dữ liệu cho Template. *Nên học Function-Based Views (viết bằng hàm) trước cho dễ hiểu, sau đó mới học Class-Based Views.*
*   **M (Model):** Đại diện cho Database. Dùng code Python (OOP) để tạo bảng dữ liệu thay vì phải viết câu lệnh SQL rườm rà.
*   **T (Template):** Giao diện HTML hiển thị cho người dùng.

## 2. Làm chủ Django Templates
Bạn cần học cú pháp đặc biệt của Django để trộn dữ liệu Python vào file HTML:
*   **Biến (Variables):** Dùng `{{ ten_bien }}` để in dữ liệu ra HTML.
*   **Thẻ điều khiển (Tags):** Vòng lặp `{% for %}` để in danh sách, lệnh điều kiện `{% if %}` để ẩn/hiện thành phần.
*   **Kế thừa Giao diện (Template Inheritance):** Cực kỳ quan trọng! Học cách dùng `{% block %}` và `{% extends 'base.html' %}` để tạo một cái khung (Header, Footer) dùng chung cho mọi trang, giúp bạn không phải copy-paste code HTML nhiều lần.

## 3. Form và Xử lý dữ liệu đầu vào
Đây là phần khó nhưng quan trọng nhất để làm các chức năng Thêm/Sửa/Xóa (CRUD).
*   **Django Forms & ModelForms:** Công cụ tự động tạo ra các ô nhập liệu HTML từ Class của Python và tự động kiểm tra lỗi (validate) cho bạn.
*   **Xử lý POST request:** Cách nhận dữ liệu khi người dùng bấm nút "Submit", kiểm tra tính hợp lệ và lưu vào Database.
*   **CSRF Token:** Học cách dùng `{% csrf_token %}` trong form HTML. Đây là cơ chế bảo mật bắt buộc của Django để chống hacker giả mạo form.

## 4. Tương tác Database (Django ORM)
Bạn không cần học SQL, chỉ cần dùng code Python để thao tác dữ liệu:
*   **Truy vấn cơ bản:** `Model.objects.all()`, `.get()`, `.filter()`, `.create()`.
*   **Migrations:** Hiểu rõ lệnh `makemigrations` (chụp ảnh sự thay đổi model) và `migrate` (áp dụng sự thay đổi đó vào Database thật).

## 5. Hệ thống User & Xác thực (Authentication)
Đừng tự viết hệ thống Đăng nhập! Django đã làm sẵn cho bạn rồi.
*   Sử dụng User model có sẵn của Django.
*   Biết cách dùng các view có sẵn để làm chức năng Đăng nhập (Login), Đăng xuất (Logout).
*   Học cách chặn người lạ: Dùng decorator `@login_required` để cấm người chưa đăng nhập vào các trang nội bộ.

## 6. Static files & Media files (Làm đẹp và Upload ảnh)
*   **Static files:** Biết cách nạp file CSS, Javascript, ảnh logo vào Template (Dùng `{% load static %}`).
*   **Media files:** Biết cách cấu hình để người dùng có thể upload hình đại diện (Avatar) và lưu vào server.

---

### 🔥 Gợi ý Project luyện tập:
Đừng học nhồi nhét lý thuyết. Hãy vừa học vừa làm **"Todo List App" (Ứng dụng Quản lý công việc)**:
1. Tạo danh sách công việc (Dùng Model, View, Template).
2. Thêm nút "Tạo việc mới" (Dùng ModelForm).
3. Thêm nút "Xóa" và "Sửa" việc.
4. Thêm chức năng Đăng ký / Đăng nhập (Mỗi người chỉ thấy danh sách việc của riêng mình).
5. Thêm chút CSS (Bootstrap/Tailwind) cho đẹp mắt.

Làm xong cái Todo List này là bạn chính thức "tốt nghiệp" khóa Django cơ bản và sẵn sàng chiến dự án lớn!
