# Phase 2: Hệ thống Phân luồng (URL Dispatcher)

Trong Django, file `urls.py` đóng vai trò như một **Cô Lễ Tân** của tòa nhà. Khi một gói tin Request đi vào, nó luôn gõ cửa Cô Lễ Tân đầu tiên để hỏi: *"Tôi muốn đi tới địa chỉ `/edit/5/`, tôi phải gặp ai?"*.

---

## 1. Cấu trúc cơ bản của một "Đường dẫn" (Path)

Hãy xem lại một dòng cơ bản trong `my_todo/urls.py`:
```python
path('delete/<int:pk>/', views.delete_task, name="delete_task"),
```
Cấu trúc của hàm `path` bao gồm 3 phần quan trọng:

### Phần 1: Mẫu URL (`'delete/<int:pk>/'`)
Đây là cái vỏ bọc mà Django dùng để "khớp" với đường link người dùng gõ.
Điểm kỳ diệu ở đây là **Path Converters** (Bộ chuyển đổi đường dẫn): `<int:pk>`.
*   Nó nói với Django rằng: *"Chỗ này sẽ là một con số (`int`). Hãy tóm lấy con số đó, đặt tên nó là biến `pk`"*.
*   Nếu người dùng gõ `/delete/100/`, Django sẽ trích xuất số `100`.
*   Nếu người dùng gõ `/delete/abc/`, nó sẽ **báo lỗi 404** ngay lập tức vì `abc` không phải là số (`int`).
*   *Các loại converter phổ biến:* `<int:id>` (số nguyên), `<str:username>` (chuỗi chữ), `<slug:title>` (chuỗi viết liền cách nhau bằng dấu gạch ngang giống link bài viết).

### Phần 2: Đích đến (`views.delete_task`)
*   Nếu cái "Vỏ bọc" ở Phần 1 khớp thành công, Cô Lễ Tân sẽ chộp lấy con số `pk` vừa lấy được, và quăng nó vào trong cái Đích đến (Bếp trưởng).
*   Đó là lý do tại sao hàm view của chúng ta luôn phải viết như sau: `def delete_task(request, pk):` (Phải hứng biến `pk` mà Lễ Tân ném sang).

### Phần 3: Đặt tên cho đường dẫn (`name="delete_task"`)
Tại sao chúng ta phải mất công đặt `name`? Sao không dùng luôn cái đường link `/delete/` cho nhanh?
Câu trả lời là: **Reverse Resolution (Giải quyết ngược).**

---

## 2. Quyền năng của việc Đặt Tên (`name`)

Trong file HTML `list.html`, thay vì viết cứng:
```html
<a href="/edit/{{ task.id }}/">Sửa</a>
```
Chúng ta đã viết:
```html
<a href="{% url 'edit_task' task.id %}">Sửa</a>
```

**Tại sao cách viết thứ 2 lại là "Thần chú" của Django?**
Giả sử một ngày đẹp trời, Giám đốc bảo bạn: *"Đổi hết đường link `/edit/` thành tiếng Việt là `/cap-nhat/` cho tôi!"*.
*   **Nếu viết cách 1:** Bạn sẽ phải lục tung 100 file HTML trong dự án lên, tìm chữ `/edit/` để sửa thành `/cap-nhat/`. Sửa sót 1 file là sập web.
*   **Nếu viết cách 2:** Bạn chỉ cần mở **duy nhất** file `urls.py`, đổi đường link, giữ nguyên cái `name`:
    ```python
    path('cap-nhat/<int:pk>/', views.edit_task, name="edit_task"),
    ```
    BÙM! Toàn bộ 100 file HTML sẽ tự động sinh ra link `/cap-nhat/` mới. Thẻ `{% url %}` sẽ tìm trong hệ thống cái path nào đang mang tên `edit_task` và tự động rải đường link mới nhất ra.

Đây được gọi là tính **DRY (Don't Repeat Yourself)** cốt lõi của mọi Framework.

### Mở rộng: Hàm `reverse()` trong file Python
Thẻ `{% url %}` ở trên chỉ dùng được bên trong file HTML (Template). Vậy nếu bạn đang code bằng Python trong file `views.py` và muốn lấy đường link từ cái Tên thì sao? Đó là lúc bạn cần dùng hàm `reverse()` (có nghĩa là "dịch ngược").

- **`reverse('home')`** đóng vai trò như một cuốn từ điển, tra xem tên `'home'` đang ứng với đường link nào trong `urls.py` và trả về đúng chuỗi text đó (ví dụ: `/`).
- **Ứng dụng siêu việt:** Kết hợp với hàm `redirect()` để dán thêm các biến phụ (Query Parameters) vào đuôi đường link.

**Ví dụ thực tế:**
Bạn muốn đẩy người dùng quay lại trang chủ (tên là `'home'`) nhưng phải dán thêm cái nhãn `?edit=1` vào mông để trang chủ biết đường hiện cái Form Sửa lên. Bạn **KHÔNG THỂ** viết `redirect('home?edit=1')` vì Django sẽ báo lỗi không tìm thấy tên lố bịch này. Bạn bắt buộc phải tự tay dịch cái tên ra thành chữ thô trước bằng `reverse()`, rồi mới nối chuỗi:

```python
from django.urls import reverse

# Bước 1: reverse('home') sẽ dịch ra thành chữ '/'
# Bước 2: f"{...}?edit={task.id}" sẽ tự động nối chữ thành '/?edit=1'
# Bước 3: Hàm redirect() sẽ làm nhiệm vụ cuối cùng: Bốc người dùng chở qua trang đó
return redirect(f"{reverse('home')}?edit={task.id}")
```

---

## 3. Quản lý luồng nâng cao (`include`)
Hiện tại dự án Todo của bạn chỉ có 1 App (`tasks`). Lỡ dự án bành trướng lên có App `users`, App `products`, App `payments` thì sao? Nếu nhét hết URL vào 1 file `my_todo/urls.py` thì file đó sẽ dài hàng nghìn dòng.

Cách giải quyết của Django: **Chia để trị (`include`)**.
Cô Lễ Tân ở Tổng công ty (`my_todo`) sẽ không quản lý chi tiết nữa, mà chỉ quản lý các Khu vực:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')), # Cứ cái gì bắt đầu bằng /tasks/ thì ném về cho Lễ tân của App tasks tự xử.
    path('users/', include('users.urls')),
]
```
Lúc này, bạn sẽ tự tạo một file `urls.py` mới nằm gọn trong thư mục `tasks/` để chuyên quản lý các luồng của riêng nó. Code sẽ cực kỳ gọn gàng và độc lập (Mô hình App-plugable).
