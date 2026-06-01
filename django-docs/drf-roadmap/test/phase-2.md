# PHASE 2 — DJANGO MODEL TESTING (PHẦN KHÁC THẬT SỰ SO VỚI PHASE 1)

# File Gợi Ý

```text
tests/test_models.py
```

Hoặc tách rõ hơn:

```text
tests/test_product_model.py
tests/test_skill_area_model.py
tests/test_user_model.py
```

Project lớn thường tách theo model/domain.

---

# 1. Điểm Khác Thật Sự So Với Phase 1

Phase 1:

- học unittest foundation
- assert
- setUp
- Arrange/Act/Assert

---

Phase 2:

# bắt đầu test behavior của Django model thật

Bao gồm:

```text
- clean()
- full_clean()
- ValidationError
- relationship
- ForeignKey
- unique constraint
- query
- dependency giữa model
- refresh_from_db()
```

Đây mới là phần Django-specific.

---

# 2. clean() & full_clean()

## clean()

```python
def clean(self):
```

Nơi viết business validation.

Ví dụ:

```python
if self.price < 0:
    raise ValidationError(...)
```

---

## full_clean()

```python
product.full_clean()
```

Dùng để chạy validation.

Bao gồm:

```text
field validation
→ clean()
→ unique validation
```

---

# Cực Kỳ Quan Trọng

```python
save()
```

KHÔNG tự gọi validation.

---

# 3. Validation Test

Ví dụ:

```python
class Product(models.Model):
    price = models.IntegerField()

    def clean(self):
        if self.price < 0:
            raise ValidationError(
                "Price cannot be negative"
            )
```

Test:

```python
with self.assertRaises(ValidationError):
    product.full_clean()
```

---

# 4. ForeignKey Relationship Test

## Model

```python
class GroupSkill(models.Model):
    name = models.CharField(max_length=255)

class SkillArea(models.Model):
    group_skill = models.ForeignKey(
        GroupSkill,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
```

---

## Test

```python
class SkillAreaModelTestCase(TestCase):

    def test_skill_area_belongs_to_group_skill(self):

        # Arrange
        group = GroupSkill.objects.create(
            name="Backend"
        )

        skill = SkillArea.objects.create(
            group_skill=group,
            name="Django"
        )

        # Assert
        self.assertEqual(
            skill.group_skill.name,
            "Backend"
        )
```

---

# 5. Dependency Giữa Models

Nếu model có ForeignKey bắt buộc:

```python
group_skill = ForeignKey(...)
```

thì test phải tạo parent trước.

Ví dụ:

```python
group = GroupSkill.objects.create(...)
```

rồi mới:

```python
SkillArea.objects.create(
    group_skill=group
)
```

---

# 6. CASCADE Test

## on_delete=models.CASCADE

Nghĩa là:

- xóa parent
- child bị xóa theo

---

## Test

```python
def test_delete_group_skill_should_delete_skill_area(self):

    # Arrange
    group = GroupSkill.objects.create(
        name="Backend"
    )

    SkillArea.objects.create(
        group_skill=group,
        name="Django"
    )

    # Act
    group.delete()

    # Assert
    self.assertEqual(
        SkillArea.objects.count(),
        0
    )
```

---

# 7. Unique Validation Test

## Model

```python
class Product(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True
    )
```

---

## Test

```python
class ProductModelTestCase(TestCase):

    def test_code_must_be_unique(self):

        # Arrange
        Product.objects.create(code="P001")

        product = Product(code="P001")

        # Act + Assert
        with self.assertRaises(ValidationError):
            product.full_clean()
```

---

# 8. Query Test

Ví dụ custom query/business filter.

---

## Model

```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
```

---

## Test

```python
def test_filter_active_products(self):

    # Arrange
    Product.objects.create(
        name="A",
        is_active=True
    )

    Product.objects.create(
        name="B",
        is_active=False
    )

    # Act
    result = Product.objects.filter(
        is_active=True
    )

    # Assert
    self.assertEqual(result.count(), 1)
```

---

# 9. refresh_from_db()

## refresh_from_db() Là Gì?

```python
task.refresh_from_db()
```

Nghĩa là:

```text
Lấy lại dữ liệu mới nhất của object đó từ database
và cập nhật vào object Python đang cầm trên tay.
```

Nói dễ hiểu:

```text
Database là "sổ chính".
Object Python là "bản photo" mình đang cầm.

Nếu có hàm khác sửa sổ chính,
bản photo trên tay mình không tự đổi theo.

refresh_from_db()
= đi photo lại bản mới từ sổ chính.
```

---

## Vì Sao Cần refresh_from_db() Trong Test?

Trong test, mình hay làm kiểu:

```python
task = Task.objects.create(title="Ship")

mark_task_done(task)

self.assertEqual(task.status, "done")
```

Nhìn thì có vẻ đúng, nhưng có một vấn đề:

```text
task là object Python đã được tạo trước khi gọi mark_task_done().
```

Nếu `mark_task_done()` sửa dữ liệu bằng cách update trong database, ví dụ:

```python
Task.objects.filter(id=task.id).update(status="done")
```

thì database đã đổi, nhưng biến `task` trong RAM có thể vẫn đang giữ giá trị cũ.

Vì vậy test phải hỏi lại database:

```python
task.refresh_from_db()
```

rồi mới assert.

---

## Ví Dụ Dễ Hiểu

## Service

```python
def mark_task_done(task):
    Task.objects.filter(id=task.id).update(
        status="done"
    )
```

Hàm này update trực tiếp xuống database.

Nó không sửa object `task` đang nằm trong RAM.

---

## Test Sai / Dễ Gây Hiểu Nhầm

```python
def test_mark_task_done(self):
    task = Task.objects.create(
        title="Ship feature",
        status="todo"
    )

    mark_task_done(task)

    self.assertEqual(task.status, "done")
```

Vấn đề:

```text
Assertion đang kiểm tra object cũ trong RAM,
chưa chắc đang kiểm tra dữ liệu thật trong database.
```

Test này có thể fail dù database đã update đúng.

Hoặc nguy hiểm hơn: test có thể pass vì service vô tình sửa object trong RAM,
nhưng mình chưa chắc dữ liệu đã được save thật xuống database.

---

## Test Đúng

```python
def test_mark_task_done(self):
    task = Task.objects.create(
        title="Ship feature",
        status="todo"
    )

    mark_task_done(task)

    task.refresh_from_db()

    self.assertEqual(task.status, "done")
```

Ý nghĩa:

```text
1. Tạo task trong test database.
2. Gọi code cần test.
3. Reload task từ database.
4. Assert trên dữ liệu thật sau khi service chạy.
```

---

## Khi Nào Nên Dùng?

Nên dùng sau khi gọi code có thể sửa database:

```text
- service function
- signal
- API/view xử lý POST/PATCH/DELETE
- queryset.update()
- method có save()
- hàm archive / restore / mark done
```

Ví dụ:

```python
archive_project(project)
project.refresh_from_db()
self.assertEqual(project.status, "archived")
```

```python
restore_task(task)
task.refresh_from_db()
self.assertEqual(task.status, "todo")
```

---

## Công Thức Nhớ Nhanh

```text
Nếu code cần test có khả năng đổi database,
thì trước khi assert object cũ:

object.refresh_from_db()
```

Không phải lúc nào cũng cần.

Nếu mình vừa tự set field trên chính object đó rồi assert ngay:

```python
task.status = "done"
self.assertEqual(task.status, "done")
```

thì không cần `refresh_from_db()`, vì lúc này chỉ đang kiểm tra giá trị trong RAM.

Nhưng trong model/service/API test, thường mình muốn chắc chắn:

```text
Database thật sự đã đổi đúng.
```

Lúc đó `refresh_from_db()` rất quan trọng.

---

# 10. Things KHÔNG Cần Test

Không cần test Django framework.

Ví dụ:

❌ BAD

```python
self.assertEqual(product.name, "Iphone")
```

nếu không có business meaning.

---

Nên test:

- business rule
- validation
- relationship
- custom method
- custom query

---

# 11. Core Mindset Của Model Testing

Model test chủ yếu để verify:

```text
- business rule
- data integrity
- relationship integrity
- validation logic
- query logic
- database state sau khi service/API thay đổi dữ liệu
```

Không phải để:

- test Django ORM hoạt động
- test framework Django
- test CharField có tồn tại hay không

```

```
