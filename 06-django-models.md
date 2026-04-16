# 📘 Django Model – Hướng Dẫn Chi Tiết Cho Người Mới

## 1. Khái Niệm Cơ Bản Về Model
**Model = Cầu nối giữa Python và Database (ORM).**
Đại diện cho một bảng (table) trong database dưới dạng Python Class.

### So sánh cách dùng:
* **SQL (Cách cũ):** Viết raw queries (`CREATE TABLE`, `SELECT`, `UPDATE`). Cồng kềnh, dễ lỗi cú pháp, dễ dính SQL Injection, khó chuyển đổi giữa MySQL/PostgreSQL.
* **Django Model (Cách mới):** Viết class Python. Django tự dịch ra SQL, tự quản lý bảng, quản lý quan hệ và tự động bảo vệ khỏi SQL Injection. Đổi database dễ dàng không ảnh hưởng code.

## 2. Công Dụng Và Vị Trí Của Model
Model là nơi trực tiếp làm việc với Database (CRUD). Hầu như luôn dùng Model, trừ các báo cáo quá phức tạp và nhiều join thì mới kết hợp raw SQL.

| Vai trò | Giải thích |
| :--- | :--- |
| **Định nghĩa cấu trúc** | Khai báo các trường dữ liệu bằng Field Types. |
| **Tạo DB (Migration)** | Chạy `makemigrations` -> `migrate` để sinh/cập nhật bảng SQL. |
| **Truy vấn an toàn** | ORM tự động escape biến, chống Query Injection triệt để. |
| **Quản lý dữ liệu** | Xử lý Thêm, Đọc, Sửa, Xoá (CRUD) hoàn toàn trên code Python. |
| **Business Logic** | Implement Logic kiểm tra tự động tại Model (Ví dụ: `save()`, `@property`). |

---

## 3. Làm Việc Với File Model (`models.py`)

### Khai báo một Model cơ bản:

```python
from django.db import models

class Employee(models.Model):
    # Các trường dữ liệu cơ bản (Fields)
    email = models.EmailField(unique=True) 
    account_name = models.CharField(max_length=20)
    joined_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Audit fields
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employee"         # Định nghĩa trực tiếp tên bảng SQL
        ordering = ["-joined_date"]   # Thiết lập sắp xếp mặc định
```

### Các Field Types Thông Dụng:
| Trong Model | Dưới Database | Dữ liệu Python |
| :--- | :--- | :--- |
| `CharField` | VARCHAR | `str` |
| `TextField` | LONGTEXT | `str` tự do |
| `IntegerField` | INT | `int` |
| `FloatField` | FLOAT | `float` |
| `DateField` | DATE | `datetime.date` |
| `DateTimeField`| DATETIME | `datetime.datetime` |
| `BooleanField` | TINYINT/BOOLEAN | `bool` |
| `EmailField` | VARCHAR | `str` (tự parse được dạng Email) |

---

## 4. Các Quan Hệ Giữa Bảng (Relationships)

Django tự động map khóa và xử lý truy vấn chéo (bạn không cần lệnh `JOIN` thủ công).

* **1 - 1 (One-to-One):** `models.OneToOneField()` - *Mỗi Employee chỉ có đúng 1 UserAccount tương ứng.*
* **1 - N (One-to-Many):** `models.ForeignKey()` - *Một Employee có thể đứng tên nhiều Request.*
* **N - N (Many-to-Many):** `models.ManyToManyField()` - *Nhiều Nhân viên làm nhiều Dự án và ngược lại.*

**Ví dụ thiết lập và Query ForeignKey:**
```python
class Request(models.Model):
    # Liên kết với bảng Employee (N-1)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="requests")

# === Query ngược (Reverse Relation) ===
# Bạn có Employee, muốn tìm mọi Requests của Employe đó:
emp = Employee.objects.get(id=1)
user_requests = emp.requests.all() # dùng tên của related_name để gọi
```

---

## 5. Thao Tác Cơ Bản Với Datbase (QuerySet & CRUD)

Thay vì `SELECT/INSERT/UPDATE...`, Django dùng đối tượng **Manager (objects)**.

```python
# 1. READ: Lấy dữ liệu
all_emps = Employee.objects.all()                                 # Lấy hết
active = Employee.objects.filter(is_active=True)                  # Mệnh đề WHERE
emp = Employee.objects.get(id=1)                                  # Lấy duy nhất 1 bản (văng lỗi Exception nếu k có)
emp_safe = Employee.objects.filter(id=999).first()                # Trả None nếu không tồn tại, an toàn hơn get()
exists = Employee.objects.filter(email="a@b.com").exists()        # Hàm đếm tồn tại hay không True/False

# 2. CREATE: Tạo mới
new_emp = Employee.objects.create(email="user@dev.com", account_name="Dev")
# --- Hoặc ---
new_emp2 = Employee(email="test@dev.com")
new_emp2.save() # Dùng kiểu này khi cần logic custom trước khi Save hoàn thành

# 3. UPDATE: Sửa đổi
emp.is_active = False 
emp.save()                                                        # Save update dòng hiện tại 
Employee.objects.filter(is_active=True).update(is_active=False)   # Bulk Update: Update nhiều Record trong 1 query

# 4. DELETE: Xoá
emp.delete()
Employee.objects.filter(is_deleted=True).delete()                 # Bulk Delete
```

---

## 6. Kỹ Thuật Model Nâng Cao

### A. Override Hành Động `save()`
Cho phép gài **Logic Nghiệp vụ** chạy tự động mỗi khi object được lưu xuống Table.

```python
class Violation(models.Model):
    score = models.IntegerField()
    
    def save(self, *args, **kwargs):
        """Override save để tự động logic, ví dụ tính lại điểm hoặc Validate"""
        if not self.id: 
             print("Đây là Record vừa tạo mới!")
        super().save(*args, **kwargs) # <- Bắt buộc phải gọi Hàm lưu cha
```

### B. Custom Managers và Thuộc Tính Ảo (`@property`)
Viết Query đóng gói vào class hoặc làm property nhanh phục vụ logic hiển thị mà không ghi Database.

```python
class Request(models.Model):
    duration = models.DurationField()

    @property
    def is_half_day(self):
        """Thuộc tính ảo: Query ra như 1 Field thường: request.is_half_day"""
        return self.duration.total_seconds() <= 4 * 3600

class EmployeeManager(models.Manager):
    def get_active(self):
        return self.get_queryset().filter(is_active=True)

class Employee(models.Model):
    objects = EmployeeManager() 
    
# CÁCH GỌI: employees = Employee.objects.get_active()
```

---

## 7. Best Practices (Chuẩn Đã Chốt Khi Query Database)

✅ **LÀM MẠNH:**
1. **Tránh kẹt N+1 Queries:** Luôn sử dụng tối ưu hóa `select_related()` cho truy cập field 1 nhánh (Foreign Keys), và `prefetch_related()` cho quan hệ danh sách.
2. **Dùng triệt để DB thay vì Code:** Chạy các Filter lớn `Employee.objects.filter(...)` bằng hệ quản trị Database chạy SQL ngầm, chứ CẤM query ra Python Memory List (`.all()`) rồi chạy vòng For để if-else lọc. Tràn Memory liền.
3. Đặt `related_name` chỉn chu rõ ràng. Truy cập Reverse mượt mà.

❌ **KHÔNG NÊN LÀM:**
1. Ném thẳng Logic check quyền user hoặc view request chìm trong file hàm Models. Tách bạch Logic ra Service hoặc Controller/View.
2. Bulk update/create `Model.objects.update(...)` sẽ KHÔNG trigger hàm `save()`. Nên chú ý cẩn dặn.
