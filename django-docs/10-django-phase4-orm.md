# Phase 4: Trái tim của hệ thống (Models & ORM)

Nếu Views là "Bộ não" chuyên tính toán, thì Models chính là "Trái tim" đập liên tục để bơm máu (Dữ liệu) đi nuôi toàn bộ hệ thống Web.

Linh hồn của Models trong Django chính là **ORM (Object-Relational Mapping)**.

---

## 1. ORM là cái phép thuật gì?

Trước khi có ORM, để lấy dữ liệu từ Database, lập trình viên bắt buộc phải viết mã SQL thô (Raw SQL) xen kẽ vào code Python:
```python
# Cách cổ đại (rất dễ bị Hacker tấn công SQL Injection)
cursor.execute("SELECT * FROM tasks WHERE completed = 1 AND title LIKE '%Học%'")
```

Với ORM, Django tạo ra một lớp "Phiên dịch viên". Bạn chỉ cần viết code Python Hướng đối tượng thuần túy, ORM sẽ tự động dịch đoạn Python đó thành câu lệnh SQL cực kỳ an toàn:
```python
# Cách của Django ORM (Thanh lịch và an toàn tuyệt đối)
Task.objects.filter(completed=True, title__contains="Học")
```

---

## 2. Giải phẫu file `models.py` (Bản thiết kế)

Khi bạn viết:
```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
```
1.  **Class `Task`:** ORM dịch nó thành lệnh tạo một cái bảng (Table) trong Database mang tên `tasks_task`.
2.  **Các thuộc tính (`title`, `completed`):** ORM dịch nó thành các Cột (Columns) trong bảng đó. 
3.  *Bí mật:* Mặc dù bạn không viết, nhưng ORM luôn tự động nhét thêm một cột số 0 có tên là `id = models.AutoField(primary_key=True)` để làm chứng minh thư (Primary Key) cho mỗi dòng dữ liệu.

---

## 3. Hệ thống "Chuyển nhà" (Migrations)

Khi bạn thay đổi bản thiết kế ở `models.py`, Database không hề biết sự thay đổi đó. Bạn phải nói chuyện với Database thông qua 2 câu lệnh huyền thoại:

1.  `python manage.py makemigrations`: 
    *   **Nghĩa là:** *"Này Django, tôi vừa sửa code Python đấy. Hãy đọc code và viết giùm tôi một tờ sớ (file migration) miêu tả những thay đổi đó ra ngôn ngữ mà DB hiểu được."*
2.  `python manage.py migrate`: 
    *   **Nghĩa là:** *"Này Django, hãy đem tờ sớ đó đưa cho Database thực thi đi (Tạo cột, xóa bảng, sửa kiểu dữ liệu...)."*

---

## 4. QuerySet API (Nghệ thuật truy vấn)

Khi bạn gọi `Task.objects...`, kết quả trả về không phải là một cái mảng (List) bình thường, mà nó là một **QuerySet** (Tập hợp truy vấn). Dưới đây là bộ bí kíp QuerySet cơ bản:

### A. Lấy dữ liệu (Đọc)
*   `Task.objects.all()`: Lấy hết toàn bộ.
*   `Task.objects.get(id=5)`: Chỉ lấy ĐÚNG 1 cái có ID là 5 (không có thì báo lỗi - nhớ bài học Phase 3 không?).
*   `Task.objects.filter(completed=True)`: Lấy ra "một bầy" các task đã hoàn thành.

### B. Mẹo tìm kiếm bá đạo (Dùng Double Underscore `__`)
Chỉ cần thêm 2 dấu gạch dưới, ORM của Django sẽ cho bạn sức mạnh vô hạn:
*   `Task.objects.filter(title__contains="Python")`: Tìm task có chứa chữ Python.
*   `Task.objects.filter(title__icontains="python")`: Giống ở trên nhưng không phân biệt chữ hoa chữ thường.
*   `Task.objects.filter(created_at__gte="2024-01-01")`: Lấy task tạo từ ngày mùng 1 trở đi (`gte` = Greater Than or Equal).

### C. Thêm, Sửa, Xóa (Write)
*   **Thêm:** `Task.objects.create(title="Quét nhà")`
*   **Sửa:** 
    ```python
    t = Task.objects.get(id=1)
    t.title = "Lau nhà"
    t.save() # Chạy lệnh này DB mới được update
    ```
*   **Xóa:** 
    ```python
    Task.objects.filter(completed=True).delete() # Xóa sạch các task đã làm xong trong 1 nốt nhạc!
    ```

---

## 5. Cấp độ Nâng cao: Sự liên kết (Relationships)

Sức mạnh khủng khiếp nhất của Database không nằm ở từng bảng rời rạc, mà ở cách chúng liên kết với nhau. Django ORM hỗ trợ 3 loại liên kết kinh điển nhất:

### A. One-to-Many (1-Nhiều) - `ForeignKey`
Đây là loại phổ biến nhất.
*   **Thực tế:** 1 Chuyên mục (Category) có thể có nhiều Bài viết (Posts). Nhưng 1 Bài viết chỉ nằm trong 1 Chuyên mục.
*   **Code:**
    ```python
    class Category(models.Model):
        name = models.CharField(max_length=100)

    class Post(models.Model):
        title = models.CharField(max_length=200)
        # Khóa ngoại trỏ về bảng Category
        category = models.ForeignKey(Category, on_delete=models.CASCADE) 
        # on_delete=models.CASCADE nghĩa là: Nếu lỡ tay xóa Chuyên mục, tất cả bài viết bên trong cũng bị xóa theo.
    ```
*   **Ma thuật Query:** 
    *   Từ bài viết suy ra chuyên mục: `post.category.name`
    *   Từ chuyên mục lấy ra TẤT CẢ bài viết: `category.post_set.all()` (Django tự động tạo ra hàm `_set` này).

### B. Many-to-Many (Nhiều-Nhiều) - `ManyToManyField`
*   **Thực tế:** 1 Bài viết có thể gắn nhiều Thẻ (Tags: #hot, #new). Ngược lại, 1 thẻ #hot có thể được gắn cho nhiều Bài viết khác nhau.
*   **Code:**
    ```python
    class Tag(models.Model):
        name = models.CharField(max_length=50)

    class Post(models.Model):
        title = models.CharField(max_length=200)
        tags = models.ManyToManyField(Tag) 
    ```
*   **Ma thuật Query:** Lấy tất cả tag của bài viết `post.tags.all()`. Lấy tất cả bài viết có chứa tag hot `hot_tag.post_set.all()`.

### C. One-to-One (1-1) - `OneToOneField`
*   **Thực tế:** 1 User (Người dùng) chỉ có đúng 1 Profile (Ảnh đại diện, Ngày sinh). Để bảng User bớt nặng, người ta tách các thông tin phụ ra bảng Profile.
*   **Code:**
    ```python
    class UserProfile(models.Model):
        # Trỏ 1-1 với bảng User mặc định của Django
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        avatar = models.ImageField(...)
        dob = models.DateField(...)
    ```
*   **Ma thuật Query:** Cực kỳ dễ: `user.userprofile.avatar` (Truy cập thẳng xuyên qua bảng bên kia như không có khoảng cách).

---
**Tóm tắt Phase 4:** Bạn không bao giờ phải động tay vào một dòng SQL nào cả. ORM của Django đã cung cấp cho bạn một cái điều khiển từ xa cực kỳ xịn để thao tác với Database và nối các bảng lại với nhau một cách diệu kỳ.
