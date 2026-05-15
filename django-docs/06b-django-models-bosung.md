# 📘 Django Model – Bổ Sung Từ Docs Chính Thức

> Nguồn: https://docs.djangoproject.com/en/6.0/topics/db/models/
> File này bổ sung những phần còn sót so với `06-django-models.md` và `10-django-phase4-orm.md`.

---

## 1. Field Options Chi Tiết

Mỗi field đều có thể nhận các tham số chung sau (tất cả đều optional):

### `null` vs `blank` – Phân biệt rõ ràng

```python
# null = Database level (có cho lưu NULL trong DB không?)
# blank = Validation level (form có cho để trống không?)

name = models.CharField(max_length=100)                    # NOT NULL, bắt buộc nhập
bio = models.TextField(null=True, blank=True)              # Cho phép NULL trong DB + để trống trên form
code = models.CharField(max_length=10, blank=True)         # Không NULL, nhưng cho phép gửi chuỗi rỗng ""
```

> **Quy tắc vàng:** Với `CharField`/`TextField`, dùng `blank=True` (chuỗi rỗng `""`). Chỉ dùng `null=True` cho các field không phải chuỗi (`DateField`, `IntegerField`, `ForeignKey`...).

### `choices` – Giới hạn giá trị hợp lệ

```python
class Task(models.Model):
    # Cách 1: Dùng list of tuples
    PRIORITY_CHOICES = [
        ("low", "Thấp"),
        ("medium", "Trung bình"),
        ("high", "Cao"),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")

    # Cách 2: Dùng dict (Django 5+)
    STATUS = {
        "todo": "Chưa làm",
        "doing": "Đang làm",
        "done": "Hoàn thành",
    }
    status = models.CharField(max_length=10, choices=STATUS)

    # Cách 3: Dùng TextChoices (Chuyên nghiệp nhất)
    class Priority(models.TextChoices):
        LOW = "low", "Thấp"
        MEDIUM = "medium", "Trung bình"
        HIGH = "high", "Cao"

    priority_v2 = models.CharField(max_length=10, choices=Priority, default=Priority.MEDIUM)
```

**Lấy giá trị hiển thị:**

```python
task = Task.objects.get(id=1)
task.priority                      # "high" (giá trị lưu trong DB)
task.get_priority_display()        # "Cao" (giá trị hiển thị)
```

> ⚠️ Mỗi lần thay đổi thứ tự `choices`, Django sẽ tạo migration mới.

### `default` vs `db_default`

```python
# default: Giá trị mặc định xử lý ở Python (khi tạo object trong code)
score = models.IntegerField(default=0)

# db_default: Giá trị mặc định xử lý ở Database (khi INSERT không có field này)
# Hữu ích khi insert dữ liệu ngoài ORM (raw SQL, migration...)
created_at = models.DateTimeField(db_default=Now())
```

### Các option phổ biến khác

```python
# help_text: Text hướng dẫn hiển thị trên form
email = models.EmailField(help_text="Nhập email công ty, VD: user@company.com")

# unique: Giá trị không được trùng trong toàn bộ bảng
code = models.CharField(max_length=10, unique=True)

# primary_key: Tự định nghĩa khóa chính (Django sẽ không tạo id tự động)
sku = models.CharField(max_length=20, primary_key=True)

# db_column: Đặt tên cột DB khác tên field Python
full_name = models.CharField(max_length=100, db_column="ho_ten")
```

---

## 2. Verbose Field Names (Tên hiển thị của Field)

Django cho phép đặt tên hiển thị dễ đọc cho field (dùng trong Admin, Form):

```python
# Cách 1: Argument vị trí đầu tiên (cho field thường)
first_name = models.CharField("tên", max_length=30)           # verbose_name = "tên"
last_name = models.CharField(max_length=30)                    # verbose_name tự động = "last name"

# Cách 2: Keyword argument (BẮT BUỘC cho ForeignKey, M2M, O2O)
project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    verbose_name="dự án liên quan",      # Phải dùng keyword vì arg đầu tiên là Model class
)

tags = models.ManyToManyField(Tag, verbose_name="danh sách tag")
```

> **Convention:** Không viết hoa chữ cái đầu của `verbose_name`. Django sẽ tự capitalize khi cần.

---

## 3. Automatic Primary Key Fields

```python
# Mặc định Django tự thêm field này vào mọi model:
id = models.BigAutoField(primary_key=True)

# Nếu bạn tự khai báo primary_key, Django sẽ KHÔNG thêm id nữa:
class Product(models.Model):
    sku = models.CharField(max_length=20, primary_key=True)  # id sẽ không tồn tại

# Cấu hình kiểu PK mặc định trong settings.py:
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Mặc định Django 3.2+
```

> ⚠️ Primary key là **read-only**. Nếu đổi giá trị PK rồi save → Django tạo record MỚI thay vì update record cũ.

---

## 4. Extra Fields on Many-to-Many (Bảng trung gian `through`)

Khi M2M cần lưu thêm thông tin (ngày tham gia, vai trò...), dùng bảng trung gian:

```python
class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, through="Enrollment")  # Chỉ định bảng trung gian

class Enrollment(models.Model):
    """Bảng trung gian – lưu thêm thông tin quan hệ"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateField()          # Thông tin bổ sung
    grade = models.CharField(max_length=2, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_enrollment")
        ]
```

**Cách thao tác:**

```python
# Tạo quan hệ qua bảng trung gian
s1 = Student.objects.create(name="An")
c1 = Course.objects.create(name="Python")

# Cách 1: Tạo trực tiếp instance Enrollment
Enrollment.objects.create(student=s1, course=c1, enrolled_date=date.today())

# Cách 2: Dùng add() với through_defaults
c1.students.add(s1, through_defaults={"enrolled_date": date.today()})

# Query bình thường
c1.students.all()                    # Tất cả sinh viên trong khóa học
s1.course_set.all()                  # Tất cả khóa học của sinh viên

# Query thông tin bảng trung gian
Enrollment.objects.filter(course=c1, grade="A")

# Xóa và clear
c1.students.remove(s1)              # Xóa enrollment
c1.students.clear()                 # Xóa toàn bộ enrollment của course
```

---

## 5. Models Across Files (Liên kết Model xuyên App)

```python
# Cách 1: Import trực tiếp
from projects.models import Project

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

# Cách 2: Lazy Reference (dùng chuỗi "app_label.ModelName")
# Không cần import, tránh circular import
class Task(models.Model):
    project = models.ForeignKey(
        "projects.Project",           # "tên_app.TênModel"
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
```

> **Khi nào dùng Lazy Reference?** Khi 2 app phụ thuộc vòng (A import B, B import A) → dùng chuỗi `"app.Model"` để tránh `ImportError`.

---

## 6. Field Name Restrictions (Hạn chế đặt tên Field)

```python
# ❌ SAI: Không dùng Python reserved word
class Bad(models.Model):
    pass = models.IntegerField()       # SyntaxError!
    class = models.CharField(...)      # SyntaxError!

# ❌ SAI: Không dùng double underscore (trùng cú pháp lookup __)
class Bad(models.Model):
    foo__bar = models.IntegerField()   # ValidationError!

# ❌ SAI: Không kết thúc bằng underscore
class Bad(models.Model):
    name_ = models.CharField(...)      # Lỗi!

# ❌ SAI: Không đặt tên "check" (trùng với Model.check())
class Bad(models.Model):
    check = models.BooleanField()      # Conflict!

# ✅ ĐÚNG: SQL reserved words (join, where, select) thì OK – Django tự escape
class OK(models.Model):
    join = models.CharField(max_length=50)    # Hợp lệ
    select = models.BooleanField()            # Hợp lệ
```

> **Workaround:** Dùng `db_column` để đặt tên cột DB khác tên field Python:
> ```python
> class_name = models.CharField(max_length=50, db_column="class")
> ```

---

## 7. Meta Options Chi Tiết

```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Tên bảng trong DB (mặc định: app_model, VD: tasks_task)
        db_table = "task"

        # Sắp xếp mặc định khi query (- = giảm dần)
        ordering = ["-created_at"]

        # Tên hiển thị trong Admin
        verbose_name = "công việc"
        verbose_name_plural = "danh sách công việc"

        # Ràng buộc dữ liệu
        constraints = [
            models.UniqueConstraint(
                fields=["title", "project"],
                name="unique_task_per_project"
            ),
            models.CheckConstraint(
                check=models.Q(priority__in=["low", "medium", "high"]),
                name="valid_priority"
            ),
        ]

        # Index để tăng tốc truy vấn
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["title"], name="idx_task_title"),
        ]

        # Quyền tùy chỉnh
        permissions = [
            ("can_assign_task", "Có thể phân công task"),
        ]

        # Lấy bản ghi mới nhất theo field nào
        get_latest_by = "created_at"
```

---

## 8. Model Methods – Hai Method Nên Luôn Có

### `__str__()` – Biểu diễn chuỗi

```python
class Task(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    # Không có __str__: hiển thị "Task object (1)" – vô nghĩa
    # Có __str__: hiển thị "Học Django" – rõ ràng trong Admin, shell, debug
```

### `get_absolute_url()` – URL chuẩn của object

```python
from django.urls import reverse

class Task(models.Model):
    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})

# Sử dụng:
# - Trong template: <a href="{{ task.get_absolute_url }}">
# - Admin tự động thêm nút "View on site"
# - redirect(task) sẽ tự gọi get_absolute_url()
```

### Custom methods & `@property`

```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True)

    def is_overdue(self):
        """Method thường – gọi bằng task.is_overdue()"""
        if self.due_date:
            return self.due_date < date.today()
        return False

    @property
    def status_label(self):
        """Property – gọi bằng task.status_label (không có ngoặc)"""
        return f"[{self.get_status_display()}] {self.title}"
```

---

## 9. Override save() và delete() – Nâng Cao

```python
class Blog(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def save(self, **kwargs):
        # Tự động tạo slug từ name
        self.slug = slugify(self.name)

        # Nếu dùng update_fields, phải thêm slug vào danh sách
        if (update_fields := kwargs.get("update_fields")) is not None:
            if "name" in update_fields:
                kwargs["update_fields"] = {"slug"}.union(update_fields)

        super().save(**kwargs)  # BẮT BUỘC gọi super()
```

> ⚠️ **Cảnh báo quan trọng:**
> - `Model.objects.update(...)` và `bulk_create()` **KHÔNG** gọi `save()`.
> - `QuerySet.delete()` và cascading delete **KHÔNG** gọi `delete()`.
> - Muốn chạy logic khi bulk → dùng **Signals**: `pre_save`, `post_save`, `pre_delete`, `post_delete`.

---

## 10. Model Inheritance (Kế thừa Model) ⭐

Django hỗ trợ 3 kiểu kế thừa:

### A. Abstract Base Class – Chia sẻ fields, KHÔNG tạo bảng

Dùng khi nhiều model cần chung một nhóm field (VD: `created_at`, `updated_at`):

```python
class TimeStampedModel(models.Model):
    """Không tạo bảng DB – chỉ là "khuôn mẫu" cho model con"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True       # ← Dòng này khiến Django KHÔNG tạo bảng

class Task(TimeStampedModel):
    title = models.CharField(max_length=200)
    # Task sẽ có 3 field: title, created_at, updated_at
    # Chỉ tạo 1 bảng: tasks_task

class Project(TimeStampedModel):
    name = models.CharField(max_length=100)
    # Project sẽ có 3 field: name, created_at, updated_at
    # Chỉ tạo 1 bảng: tasks_project
```

**Meta inheritance:**

```python
class Base(models.Model):
    class Meta:
        abstract = True
        ordering = ["name"]

class Child(Base):
    name = models.CharField(max_length=100)
    class Meta(Base.Meta):         # Kế thừa Meta của Base
        db_table = "child_table"   # Thêm tùy chỉnh riêng
    # Child kế thừa ordering = ["name"] từ Base
```

**`related_name` trong Abstract class** – phải dùng `%(class)s` và `%(app_label)s`:

```python
class Base(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_set",   # Tránh trùng tên
    )
    class Meta:
        abstract = True

# tasks.Task  → related_name = "tasks_task_set"
# projects.Project → related_name = "projects_project_set"
```

### B. Multi-table Inheritance – Mỗi model một bảng riêng

Dùng khi model con "là một loại" (is-a) model cha, và cần bảng riêng:

```python
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_pizza = models.BooleanField(default=False)
    # Django tự tạo OneToOneField liên kết Restaurant → Place
    # Tạo 2 bảng: place + restaurant
```

**Query:**

```python
Place.objects.filter(name="Pizza Hut")           # Tìm trong bảng Place
Restaurant.objects.filter(name="Pizza Hut")      # Tìm qua JOIN 2 bảng

# Từ Place → Restaurant (đi xuống model con)
p = Place.objects.get(id=1)
p.restaurant          # Trả về Restaurant object (hoặc raise DoesNotExist)

# Từ Restaurant → Place (đi lên model cha)
r = Restaurant.objects.get(id=1)
r.name                # Truy cập thẳng field của Place
```

> ⚠️ Multi-table inheritance tạo JOIN mỗi khi query → nặng hơn Abstract. Chỉ dùng khi thật sự cần bảng cha tồn tại độc lập.

### C. Proxy Model – Thay đổi hành vi Python, KHÔNG đổi bảng

Dùng khi muốn thêm method hoặc đổi Manager/ordering mà không tạo bảng mới:

```python
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class OrderedPerson(Person):
    """Dùng cùng bảng person, nhưng mặc định sắp xếp theo last_name"""
    class Meta:
        proxy = True                    # ← Không tạo bảng mới
        ordering = ["last_name"]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# Cả 2 class dùng chung 1 bảng DB
Person.objects.create(first_name="An", last_name="Nguyen")
OrderedPerson.objects.all()    # Trả về Person data, sorted by last_name
```

### So sánh 3 kiểu kế thừa

| Tiêu chí | Abstract | Multi-table | Proxy |
|:---|:---|:---|:---|
| Tạo bảng DB? | ❌ Không | ✅ Mỗi model 1 bảng | ❌ Dùng chung bảng cha |
| Thêm field? | ✅ Có | ✅ Có (bảng riêng) | ❌ Không |
| Thêm method? | ✅ Có | ✅ Có | ✅ Có |
| Đổi Meta? | ✅ Có | ⚠️ Hạn chế | ✅ Có |
| Query cha trực tiếp? | ❌ Không | ✅ Có | ✅ Có |
| Use case | Chia sẻ fields chung | Mở rộng model có sẵn | Đổi behavior/ordering |

---

## 11. Organizing Models in a Package

Khi `models.py` quá dài, tách thành package:

```
myapp/
├── models/
│   ├── __init__.py       # Import tất cả models ở đây
│   ├── task.py
│   └── project.py
```

```python
# myapp/models/__init__.py
from .task import Task
from .project import Project
# Luôn import rõ ràng, KHÔNG dùng: from .task import *
```

---

## 12. on_delete Options (Hành vi khi xóa record cha)

```python
class Task(models.Model):
    # CASCADE: Xóa Project → Xóa luôn tất cả Task của nó
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    # SET_NULL: Xóa Project → Task.project = NULL (phải có null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    # SET_DEFAULT: Xóa Project → Task.project = giá trị default
    project = models.ForeignKey(Project, on_delete=models.SET_DEFAULT, default=1)

    # PROTECT: Xóa Project → Django chặn, raise ProtectedError
    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    # RESTRICT: Giống PROTECT nhưng cho phép xóa nếu cùng CASCADE chain
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)

    # DO_NOTHING: Không làm gì (nguy hiểm – có thể gây lỗi DB integrity)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
```

---

## 13. Field Name "Hiding" – Không Được Ghi Đè Field

```python
class Base(models.Model):
    title = models.CharField(max_length=100)

# ❌ SAI: Không được override field từ non-abstract parent
class Child(Base):
    title = models.TextField()  # Django raise FieldError!

# ✅ ĐÚNG: Có thể override field từ abstract parent
class AbstractBase(models.Model):
    title = models.CharField(max_length=100)
    class Meta:
        abstract = True

class Child(AbstractBase):
    title = models.TextField()     # OK!

# ✅ Có thể xóa field kế thừa từ abstract parent
class Child2(AbstractBase):
    title = None                   # Xóa field title
```

---

## Tổng kết: Checklist Model Chuyên Nghiệp

```python
from django.db import models
from django.urls import reverse

class Task(models.Model):
    """Checklist đầy đủ cho một Model chuyên nghiệp"""

    # 1. Choices dùng TextChoices
    class Status(models.TextChoices):
        TODO = "todo", "Chưa làm"
        DOING = "doing", "Đang làm"
        DONE = "done", "Hoàn thành"

    # 2. Fields với đầy đủ options
    title = models.CharField("tiêu đề", max_length=200)
    description = models.TextField("mô tả", blank=True)
    status = models.CharField(max_length=10, choices=Status, default=Status.TODO)
    project = models.ForeignKey(
        "projects.Project",              # Lazy reference
        on_delete=models.CASCADE,
        related_name="tasks",            # Quan hệ ngược rõ ràng
        verbose_name="dự án",
    )

    # 3. Audit fields (nên dùng Abstract Base Class)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 4. Meta options
    class Meta:
        db_table = "task"
        ordering = ["-created_at"]
        verbose_name = "công việc"
        verbose_name_plural = "danh sách công việc"

    # 5. __str__ – LUÔN LUÔN định nghĩa
    def __str__(self):
        return self.title

    # 6. get_absolute_url – nếu object có trang riêng
    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})

    # 7. Custom methods / properties
    @property
    def is_completed(self):
        return self.status == self.Status.DONE
```
