# Phase 5: Rào chắn An ninh (Forms & Validations)

Trong Web, người dùng có thể nhập bất cứ thứ gì vào ô input:
- Tên công việc bình thường: "Đi học"
- Chữ rỗng tuếch: ""
- Script nguy hiểm: `<script>alert('Hacked!')</script>`

**Forms** của Django đóng vai trò như một "Trạm kiểm soát an ninh sân bay". Mọi dữ liệu từ người dùng gửi lên đều PHẢI đi qua đây trước khi được phép vào Database.

---

## 1. Hai loại Form trong Django

### A. `forms.Form` - Form thủ công
Bạn tự tay định nghĩa từng trường. Dùng khi form không liên quan trực tiếp đến một Model cụ thể (ví dụ: Form Đăng nhập, Form Liên hệ).

```python
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
```

### B. `forms.ModelForm` - Form thông minh (Đang dùng trong Todo App)
Bạn chỉ cần nói: *"Tôi muốn làm form cho Model Task, lấy 1 trường title"*. Django tự động "đọc" Model và sinh ra form tương ứng. Cực kỳ DRY (Don't Repeat Yourself).

```python
# File forms.py hiện tại của bạn
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']  # Chỉ dùng field 'title' thôi
```

**Tại sao `ModelForm` lại thần thánh?**
- Nó tự kế thừa luôn các quy tắc validation đã khai báo trong `models.py` (ví dụ: `max_length=200` của field `title`).
- Bạn chỉ cần gọi `form.save()`, nó tự biết phải lưu vào bảng nào trong Database.

---

## 2. Giải phẫu dòng `if form.is_valid()`

Đây là dòng code thần bí nhất, nhưng thực ra Django đang làm 3 bước rất logic:

**Bước 1: Kiểm tra trường có bị rỗng không?**
Vì `title` trong `models.py` là `CharField` (không có `blank=True`), Django mặc định bắt buộc phải nhập. Nếu người dùng gửi form rỗng, `is_valid()` sẽ trả về `False` ngay lập tức.

**Bước 2: Kiểm tra kiểu dữ liệu đúng chưa?**
Nếu có một field kiểu `IntegerField` (số nguyên) mà người dùng gõ chữ "abc" vào, `is_valid()` cũng trả về `False`.

**Bước 3: Kiểm tra độ dài có vượt quá giới hạn không?**
`max_length=200` trong `models.py` sẽ được áp dụng ở đây.

Nếu TẤT CẢ 3 bước đều qua, `is_valid()` mới trả về `True`.

---

## 3. Tự viết luật kiểm tra riêng (Custom Validation)

Để kiểm tra dữ liệu cho một trường cụ thể, Django sử dụng cơ chế **Quy ước đặt tên (Naming Convention)**.

#### A. Quy tắc đặt tên
Khi hàm `is_valid()` chạy, Django sẽ tự động tìm kiếm và thực thi các phương thức trong class Form có tên theo cấu trúc:
👉 **`clean_<fieldname>`**

*Ví dụ:* Để validate trường `title`, bạn phải đặt tên hàm chính xác là `clean_title`. Nếu đặt tên khác, Django sẽ không nhận diện được đây là hàm dùng để kiểm tra dữ liệu.

#### B. Nguồn gốc của `cleaned_data`
Biến `cleaned_data` là một Dictionary được kế thừa từ lớp cha `BaseForm`. 
1.  Khi gọi `is_valid()`, Django lọc dữ liệu thô từ `request.POST`.
2.  Dữ liệu hợp lệ ban đầu (đúng kiểu dữ liệu, không để trống) sẽ được lưu vào `self.cleaned_data`.
3.  Sau đó, các hàm `clean_<fieldname>` mới được gọi để thực hiện các kiểm tra chuyên sâu hơn.

#### C. Ví dụ:
```python
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']

    def clean_title(self):
        # 1. Lấy dữ liệu đã được lọc sơ bộ
        title = self.cleaned_data.get('title')

        # 2. Áp dụng luật riêng (VD: chặn từ cấm)
        if title.lower() in ['abc', 'test']:
            raise forms.ValidationError("Tên công việc không hợp lệ!")

        # 3. Trả về giá trị cuối cùng để lưu vào Database
        return title
```

Khi người dùng nhập "abc" vào, `is_valid()` sẽ tự động gọi hàm `clean_title()`, hàm đó `raise` lỗi, và `is_valid()` trả về `False`. Lỗi đó sẽ được gắn thẳng vào field `title` để hiển thị lên màn hình.

---

## 4. Tại sao PHẢI có `{% csrf_token %}` trong mọi Form?

Đây là cơ chế bảo mật chống lại cuộc tấn công **CSRF (Cross-Site Request Forgery - Mạo danh yêu cầu)**.

#### A. Kịch bản tấn công (Nếu không có Token)
1.  **Dấu vân tay (Cookie):** Khi bạn đăng nhập vào Facebook, trình duyệt lưu một cái Cookie (như dấu vân tay của bạn). Mỗi khi bạn làm gì trên Facebook, trình duyệt tự động đính kèm "dấu vân tay" này để Facebook biết đó là bạn.
2.  **Kẻ mạo danh:** Bạn lỡ tay bấm vào một trang web độc hại của Hacker. Trang đó chạy ngầm một cái Form yêu cầu Facebook: *"Xóa tài khoản của người này cho tôi"*.
3.  **Lỗ hổng:** Trình duyệt thấy yêu cầu gửi tới Facebook, nó **tự động** đính kèm dấu vân tay của bạn vào. Facebook thấy dấu vân tay đúng, thế là xóa tài khoản của bạn mà bạn không hề hay biết.

#### B. Giải pháp: Mã bí mật (`{% csrf_token %}`)
Django không chỉ tin vào mỗi "Dấu vân tay" (Cookie). Khi bạn mở một cái Form, Django nhét thêm một cái **Mã bí mật** ngẫu nhiên vào Form đó.

1.  **Xác thực kép:** Để thực hiện một yêu cầu (như Thêm/Xóa Task), Django bắt buộc bạn phải nộp đủ: **Dấu vân tay (Cookie)** + **Mã bí mật (Token)**.
2.  **Tính bảo mật:** Trang web của Hacker có thể lừa trình duyệt gửi "Dấu vân tay", nhưng nó **không cách nào lấy trộm được "Mã bí mật"** nằm bên trong trang web của bạn (do luật bảo mật của trình duyệt).
3.  **Kết quả:** Khi request từ trang Hacker gửi tới mà thiếu Mã bí mật, Django sẽ chặn đứng và báo lỗi `403 Forbidden`.

👉 **Tóm lại:** `{% csrf_token %}` là lá chắn đảm bảo rằng yêu cầu này được gửi đi từ **chính trang web của bạn**, chứ không phải bị một trang web khác mạo danh gửi hộ.
