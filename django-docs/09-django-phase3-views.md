# Phase 3: Bộ não xử lý (Views)

Trong kiến trúc M-V-T (Model-View-Template) của Django, **View** đóng vai trò là "Chữ V quyền lực". Nó chính là "Bộ não" trung tâm, nơi chứa toàn bộ logic nghiệp vụ (Business Logic) của ứng dụng.

Nhiệm vụ cốt lõi của một View rất đơn giản: **Nhận vào một Web Request và Trả về một Web Response.**

---

## 1. Mổ xẻ Function-Based Views (FBV - View viết bằng Hàm)

Đây là cách bạn đang viết trong dự án Todo hiện tại. Nó rất trực quan và dễ hiểu cho người mới.

Một FBV tiêu chuẩn luôn tuân theo công thức 4 bước:

```python
def example_view(request, id):
    # BƯỚC 1: Rút trích dữ liệu từ Request
    # (Lấy dữ liệu từ URL, từ form POST, hoặc từ User đang đăng nhập)
    user_name = request.user.username
    search_query = request.GET.get('q')

    # BƯỚC 2: Tương tác với Cở sở dữ liệu (Models)
    # (Hỏi Model để lấy dữ liệu, lưu dữ liệu mới, xóa dữ liệu cũ)
    task = Task.objects.get(id=id)

    # BƯỚC 3: Xử lý Logic (Thuật toán)
    # (Tính toán, kiểm tra quyền hạn, gửi email...)
    if task.completed:
        status_message = "Đã xong"
    else:
        status_message = "Chưa xong"

    # BƯỚC 4: Đóng gói và Trả về (Response)
    return render(request, 'template.html', {'msg': status_message})
```

---

## 2. Các loại Đóng gói (Return) thường gặp

Hàm View BẮT BUỘC phải trả về một đối tượng Response. Django cung cấp 2 "hộp đóng gói" quan trọng nhất:

### A. `render(request, 'file.html', context)` — "Nấu tại chỗ"
- **Cách hoạt động:** Django tự đọc file HTML, trộn dữ liệu vào và bưng thẳng cho trình duyệt hiển thị.
- **Dùng khi:** Bạn muốn hiển thị một trang web (thường là yêu cầu **GET**).

### B. `redirect('url')` — "Chỉ đường đi chỗ khác"
- **Cách hoạt động:** Django không trả về HTML. Nó gửi lệnh bắt trình duyệt phải tự chạy sang một địa chỉ khác.
- **Dùng khi:** Sau khi xử lý xong dữ liệu (thường là yêu cầu **POST** như Thêm/Sửa/Xóa).
- **Cơ chế thông minh (resolve_url):** Khi bạn ném 1 giá trị vào `redirect()`, Django sẽ dò tìm theo đúng thứ tự ưu tiên sau:
    1. **Là một Object (Model):** (Ví dụ: `redirect(task)`) - Nó sẽ tự động gọi hàm `get_absolute_url()` của object đó để lấy link.
    2. **Là Tên URL (Named URL):** (Ví dụ: `redirect('home')`) - Nó lục trong danh bạ `urls.py` xem có ai tên 'home' không để lắp ráp link. *(Khuyên dùng)*
    3. **Là Link cứng (Hardcoded):** (Ví dụ: `redirect('/dashboard/')`) - Nếu 2 bước trên thất bại, nó coi đây là cái link thô và ép trình duyệt chuyển tới đúng đoạn text đó.

### C. `HttpResponse("Chữ thô")` — "Trả về chữ trần trụi"
- **Cách hoạt động:** Chỉ đơn giản là trả về một đoạn văn bản thô, không có thẻ HTML trang trí, không có giao diện.
- **Dùng khi:** Thường dùng để test nhanh một View xem nó có hoạt động không, hoặc trả về một thông báo cực kỳ đơn giản (rất ít dùng trong thực tế khi làm web hoàn chỉnh).
- **Ví dụ:** `return HttpResponse("Xin chào, tôi là văn bản thô!")`

### D. `JsonResponse({'status': 'ok'})` — "Dành riêng cho API"
- **Cách hoạt động:** Thay vì trả về mã HTML cho trình duyệt đọc, nó trả về dữ liệu chuẩn JSON (như một Dictionary).
- **Dùng khi:** Khi bạn viết API để cho các ứng dụng khác (như Mobile App Android/iOS, hoặc Frontend như React/Vue) gọi tới và lấy dữ liệu chứ không cần giao diện.
- **Ví dụ:** `return JsonResponse({'message': 'Thành công', 'code': 200})`

---

### 💡 Bí kíp thực chiến: Quy tắc POST/Redirect/GET
Đây là quy tắc giúp web của bạn chuyên nghiệp và không bị lỗi dữ liệu:

| Tình huống | Dùng lệnh | Tại sao? |
| :--- | :--- | :--- |
| **Hiển thị trang** | `render` | Cần trả về giao diện ngay lập tức cho người dùng xem. |
| **Xử lý POST xong** | `redirect` | **Cực kỳ quan trọng:** Để tránh việc người dùng bấm **F5 (Refresh)** khiến dữ liệu bị gửi lại và lưu trùng lặp vào Database. |

**Ví dụ logic chuẩn:**
1. User gửi POST (Thêm task) -> Django lưu Database thành công.
2. Django gọi `redirect('/')`.
3. Trình duyệt tự động chuyển sang trang chủ bằng yêu cầu GET.
4. Bây giờ nếu User bấm F5, nó chỉ load lại trang chủ (GET), không hề gửi lại lệnh Thêm task nữa.

---


---

## 3. Tương lai: Class-Based Views (CBV)

Khi dự án của bạn phình to, bạn sẽ nhận ra một điều đau khổ: Việc viết các tính năng CRUD (Thêm - Sửa - Xóa - Đọc) lặp đi lặp lại rất nhàm chán. Hàm nào cũng check POST, check form.is_valid(), save(), rồi redirect.

Vì Python là ngôn ngữ Hướng đối tượng (OOP) cực mạnh, những người tạo ra Django đã viết sẵn các Class khổng lồ để làm thay bạn phần việc lặp đi lặp lại đó.

Ví dụ, để viết tính năng "Liệt kê danh sách Task", thay vì phải tự rút dữ liệu rồi render như hàm `home_page`, bạn chỉ cần viết ĐÚNG 2 DÒNG CODE:

```python
from django.views.generic import ListView
from .models import Task

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/list.html'
```
Bùm! 2 dòng code trên hoàn toàn tương đương với 10 dòng code trong Function-Based View. 
Django đã đóng gói sẵn các Class cực xịn:
*   **`ListView`**: Chuyên trị hiển thị danh sách (có sẵn chức năng chia trang - pagination).
*   **`DetailView`**: Chuyên hiển thị thông tin 1 đối tượng.
*   **`CreateView`, `UpdateView`, `DeleteView`**: Bao thầu trọn gói việc check POST, check Form, báo lỗi đỏ, lưu Database.

**Lộ trình học:** Bạn cứ rèn luyện thật nhuần nhuyễn FBV (Hàm) để hiểu bản chất luồng đi đã. Khi nào thấy chán ngán với việc viết code lặp đi lặp lại, đó là lúc bạn sẵn sàng "giác ngộ" CBV.
