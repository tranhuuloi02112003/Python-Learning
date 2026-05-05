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

Ở BƯỚC 4, View không thể trả về một biến Python thông thường (ví dụ `return "Hello"` là sẽ báo lỗi ngay). Nó BẮT BUỘC phải trả về một đối tượng họ hàng nhà `HttpResponse`. Django đã cung cấp sẵn các "Hộp đóng gói" cực kỳ xịn:

1.  **`render(request, 'file.html', context_dict)`**: 
    Hộp đóng gói phổ biến nhất. Nó lấy code HTML thô, "trộn" với cái từ điển `context_dict` bạn đưa cho, dịch mã ra HTML hoàn chỉnh rồi mới gửi về trình duyệt.
2.  **`redirect('/url-moi/')`**: 
    Hộp điều hướng. Nó chả trả về HTML gì cả, nó chỉ ra lệnh cho trình duyệt: *"Xong việc rồi, cút sang cái link này đi!"*. Dùng cực nhiều sau khi lưu form thành công (để tránh user F5 bị gửi form 2 lần).
3.  **`JsonResponse({'status': 'ok'})`**: 
    Hộp dành riêng cho API. Thay vì trả về HTML để người dùng đọc, nó trả về định dạng chuẩn JSON để các app Mobile (iOS/Android) hoặc React/Vue đọc.
4.  **`HttpResponse("Chữ thô")`**: 
    Trả về chữ trần trụi, không có thẻ HTML. Ít dùng trong thực tế.

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
