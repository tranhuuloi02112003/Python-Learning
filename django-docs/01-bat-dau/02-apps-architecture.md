# Django Apps Architecture (Kiến trúc Module)

Trong Django, chúng ta không gọi là "Module" mà gọi là **App**. Một dự án Django (Project) là tập hợp của nhiều App nhỏ liên kết với nhau.

## 1. Sự khác biệt giữa Project và App

Để không bị nhầm lẫn, bạn hãy nhớ quy tắc này:
- **Project (Dự án):** Là toàn bộ trang web/hệ thống của bạn. Nó chứa các file cấu hình chung (như `settings.py`, `urls.py` tổng).
- **App (Ứng dụng/Module):** Là một bộ phận độc lập thực hiện một chức năng cụ thể. Một Project có thể có 1 hoặc rất nhiều App.

> **Triết lý của Django:** "Write once, use everywhere". Một App được viết tốt có thể được rút ra và gắn vào một Project khác mà vẫn chạy được.

---

## 2. Khi nào thì cần tạo một Module (App) mới?

Sai lầm lớn nhất của người mới là viết tất cả mọi thứ vào một App duy nhất. Bạn nên tạo một App mới khi:

1. **Khác biệt về logic:** Chức năng đó thực hiện một nhiệm vụ hoàn toàn khác với phần còn lại.
2. **Có thể tái sử dụng:** Bạn nghĩ rằng chức năng này sau này có thể dùng lại cho dự án khác (ví dụ: module Gửi Email, module Quản lý User).
3. **Dễ bảo trì:** Khi file `models.py` hoặc `views.py` của bạn quá dài (hàng nghìn dòng), đó là lúc nên tách App.

---

## 3. Ví dụ cụ thể (Scenario)

Giả sử bạn đang xây dựng một trang **Thương mại điện tử**:

Thay vì tạo một thư mục "Code" chung chung, bạn sẽ chia thành các App (Module) như sau:

| Tên App | Nhiệm vụ (Logic) | Tại sao tách? |
|---|---|---|
| **`users`** | Đăng ký, đăng nhập, phân quyền, hồ sơ khách hàng. | Vì quản lý người dùng là phần riêng biệt, cần bảo mật cao. |
| **`products`** | Danh sách sản phẩm, kho hàng, danh mục (Category). | Vì nó tập trung vào việc hiển thị và quản lý dữ liệu hàng hóa. |
| **`orders`** | Giỏ hàng, thanh toán, trạng thái đơn hàng. | Logic về thanh toán và tính toán tiền bạc rất phức tạp, cần tách riêng để dễ test. |
| **`blog`** | Bài viết tin tức về sản phẩm. | Phần này không liên quan trực tiếp đến việc bán hàng, có thể tắt đi mà không hỏng web. |

---

## 4. Cấu trúc bên trong một Module (App)

Khi bạn chạy lệnh `python manage.py startapp products`, Django sinh ra:
```text
products/
├── migrations/    # Lưu lịch sử thay đổi Database của module này
├── admin.py      # Cấu hình giao diện Admin cho module này
├── apps.py       # Cấu hình tên module
├── models.py     # NƠI QUAN TRỌNG NHẤT: Định nghĩa cấu trúc dữ liệu
├── tests.py      # Viết code kiểm thử cho module này
└── views.py      # Xử lý logic và hiển thị dữ liệu
```

---

## 5. Lưu ý quan trọng khi tạo App

Để Project của bạn không bị "lộn xộn" như bạn lo lắng:

1. **Đăng ký App:** Sau khi dùng lệnh `startapp`, bạn **bắt buộc** phải khai báo tên App đó vào mục `INSTALLED_APPS` trong file `settings.py`. Nếu không, Django sẽ không nhận ra module bạn vừa tạo.
2. **Mỗi App một URL:** Hãy tạo file `urls.py` riêng bên trong mỗi App và "include" nó vào file `urls.py` tổng của Project. Điều này giúp code cực kỳ sạch và dễ quản lý đường dẫn.
