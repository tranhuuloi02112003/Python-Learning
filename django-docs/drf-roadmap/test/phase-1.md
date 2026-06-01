# PHASE 1 — DJANGO TESTING FOUNDATION

# 1. Test Là Gì?

Test là code dùng để kiểm tra code khác có chạy đúng không.

Ví dụ:

```python
def add(a, b):
    return a + b
```

Thay vì tự kiểm tra bằng tay:

```python
add(1, 2)
```

Ta viết test:

```python
from django.test import TestCase

class MathTestCase(TestCase):

    def test_add_two_numbers(self):
        result = add(1, 2)

        self.assertEqual(result, 3)
```

Ý nghĩa:

```python
self.assertEqual(result, 3)
```

=> Mong kết quả phải bằng `3`.

---

# 2. Cấu Trúc Một Django Test

```python
from django.test import TestCase

class MyTestCase(TestCase):

    def setUp(self):
        pass

    def test_something(self):
        self.assertEqual(1 + 1, 2)
```

## Giải thích

### class ...TestCase(TestCase)

Là nhóm test.

---

### setUp()

Chạy trước MỖI test.

---

### test\_\*

Django chỉ nhận diện các function bắt đầu bằng:

```python
test_
```

---

# 3. Arrange - Act - Assert Pattern

Hầu hết test đều nên theo format này.

Ví dụ:

```python
def test_add_two_numbers(self):

    # Arrange
    a = 1
    b = 2

    # Act
    result = add(a, b)

    # Assert
    self.assertEqual(result, 3)
```

---

## Arrange

Chuẩn bị data.

Ví dụ:

```python
a = 1
b = 2
```

---

## Act

Gọi code cần test.

Ví dụ:

```python
result = add(a, b)
```

---

## Assert

Kiểm tra kết quả.

Ví dụ:

```python
self.assertEqual(result, 3)
```

---

# 4. Các Assert Quan Trọng

## assertEqual

```python
self.assertEqual(a, b)
```

Kiểm tra:

```python
a == b
```

---

## assertTrue

```python
self.assertTrue(result)
```

Kiểm tra result là True.

---

## assertFalse

```python
self.assertFalse(result)
```

Kiểm tra result là False.

---

## assertIsNone

```python
self.assertIsNone(value)
```

Kiểm tra value là None.

---

## assertIsNotNone

```python
self.assertIsNotNone(value)
```

Kiểm tra value khác None.

---

# 5. Django TestCase

Import:

```python
from django.test import TestCase
```

Django sẽ:

- tạo test database riêng
- chạy test trên DB đó
- xóa DB sau khi test xong

=> Không làm bẩn database thật.

---

# 6. Ví Dụ Model Test

## Model

```python
class SkillArea(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
```

---

## Test

```python
from django.test import TestCase
from app.models import SkillArea

class SkillAreaTestCase(TestCase):

    def test_str_returns_name(self):

        # Arrange
        skill = SkillArea.objects.create(
            name="Backend"
        )

        # Act
        result = str(skill)

        # Assert
        self.assertEqual(result, "Backend")
```

---

# 7. setUp()

Dùng để tránh lặp code tạo data.

Ví dụ:

```python
class ProductTestCase(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Iphone 15"
        )

    def test_product_name(self):
        self.assertEqual(
            self.product.name,
            "Iphone 15"
        )

    def test_is_phone(self):
        result = self.product.is_phone()

        self.assertTrue(result)
```

---

# 8. Flow Hoạt Động Của setUp()

Nếu có 2 test:

```python
test_a()
test_b()
```

Thì flow:

```text
setUp()
→ test_a()

setUp()
→ test_b()
```

=> Mỗi test độc lập nhau.

---

# 9. self Trong Test

## Sai phạm vi

```python
product = Product.objects.create(...)
```

Chỉ dùng được trong 1 function.

---

## Dùng self

```python
self.product = Product.objects.create(...)
```

Dùng được trong toàn bộ class.

---

# 10. Test Phải Predictable

Test tốt phải:

- hôm nay pass
- mai pass
- CI/CD pass
- máy khác vẫn pass

Không nên phụ thuộc:

- DB thật
- internet
- external API
- data có sẵn

---

# 11. assertRaises()

Dùng để kiểm tra code có raise exception không.

Ví dụ:

```python
with self.assertRaises(ValueError):
    int("abc")
```

Vì:

```python
int("abc")
```

sẽ raise:

```python
ValueError
```

---

# 12. full_clean()

```python
model.full_clean()
```

Dùng để chạy validation của model.

Ví dụ:

```python
class Product(models.Model):
    name = models.CharField(max_length=10)
```

Test:

```python
from django.core.exceptions import ValidationError

product = Product(
    name="aaaaaaaaaaaaaaaaaaaa"
)

with self.assertRaises(ValidationError):
    product.full_clean()
```

Vì name vượt max_length.

---

# 13. Happy Path & Fail Path

Không chỉ test case đúng.

Cần test cả:

- input đúng
- input sai
- empty
- duplicate
- unauthorized
- permission denied
- invalid data

Ví dụ:

```python
class ProductTestCase(TestCase):

    def test_is_phone_returns_true(self):

        # Arrange
        product = Product(name="Iphone 15")

        # Act
        result = product.is_phone()

        # Assert
        self.assertTrue(result)

    def test_is_phone_returns_false(self):

        # Arrange
        product = Product(name="Macbook")

        # Act
        result = product.is_phone()

        # Assert
        self.assertFalse(result)
```

---

# 14. Cách Chạy Test

## Chạy toàn bộ

```bash
python manage.py test
```

---

## Chạy 1 file

```bash
python manage.py test app.tests.test_models
```

---

## Chạy 1 class

```bash
python manage.py test app.tests.test_models.SkillAreaTestCase
```

---

## Chạy 1 method

```bash
python manage.py test app.tests.test_models.SkillAreaTestCase.test_str_returns_name
```

---

# 15. Mindset Quan Trọng

Test không phải để:

- code cho có
- tăng coverage

Test là để:

- chống bug
- verify business logic
- đảm bảo refactor không phá code cũ

---

# PHASE 1 — EXTRA NOTE (NHỮNG ĐIỂM DỄ NHẦM)

# 1. TABLE ≠ DATA

Đây là chỗ dễ nhầm nhất.

---

## TABLE (Schema)

Là cấu trúc database:

```text
auth_user
auth_group
skill_area
group_skill
```

Django tạo từ migration.

Khi chạy test:

```bash
python manage.py test
```

Django thường sẽ tạo gần như full schema cho test DB.

=> Không phải chỉ tạo mỗi table liên quan file test.

---

## DATA (Row/Object)

Là dữ liệu bên trong table:

```text
admin
backend
manager role
```

Data chỉ xuất hiện khi:

- test create object
- migration seed data
- fixture
- signal
- setUpTestData()
- code startup

Ví dụ:

```python
User.objects.create(...)
```

---

# 2. Test DB KHÔNG copy data từ DB thật

Django KHÔNG copy data production/dev DB sang test DB.

Nó chỉ:

```text
- tạo DB test
- chạy migration
- tạo schema/table
```

=> Data phải tự tạo trong test.

Đó là lý do test thường có:

```python
User.objects.create(...)
```

---

# 3. Vì sao thấy data sẵn trong test DB?

Nếu thấy data trong:

```text
test_xxx_db
```

thì thường do:

---

## Migration seed data

Ví dụ:

```python
migrations.RunPython(create_roles)
```

Khi test DB tạo:

- migration chạy
- data seed được insert

---

## Fixture

Ví dụ:

```python
fixtures = ["users.json"]
```

Django tự load data mẫu.

---

## setUpTestData()

Ví dụ:

```python
@classmethod
def setUpTestData(cls):
    User.objects.create(...)
```

---

## Test đang create data

Ví dụ:

```python
User.objects.create(...)
```

---

## Dùng --keepdb

```bash
python manage.py test --keepdb
```

Django giữ lại test DB sau khi test xong.

---

# 4. Rollback ≠ Không Có Data

Nhiều newbie nghĩ:

```text
rollback
```

nghĩa là data chưa từng tồn tại.

Sai.

---

Trong lúc test đang chạy:

```text
- data vẫn tồn tại
- vẫn query được
- vẫn thấy trong MySQL Workbench
```

Sau khi test xong:

- Django flush/rollback
- hoặc destroy test DB

---

# 5. Unit Test vs Integration/API Test

## Unit Test

Ví dụ:

```python
result = service.calculate()
```

Đặc điểm:

```text
- không request HTTP
- không auth
- không permission
- test logic nhỏ
```

Thường dùng cho:

- model method
- utility function
- service logic

---

## API / Integration Test

Ví dụ:

```python
response = self.client.get("/api/users/")
```

Đặc điểm:

```text
- có request giả lập
- đi qua URL
- auth
- permission
- serializer
- view
```

Dùng để test:

- token
- role
- permission
- API response
- authentication
- authorization

---

# 6. Test 1 File KHÔNG có nghĩa chỉ tạo table file đó

Ví dụ chạy:

```bash
python manage.py test app.tests.test_models
```

Django vẫn có thể:

- tạo full schema
- auth tables
- permission tables
- các app tables

Chỉ khác:

- chỉ chạy test trong file đó

---

# 7. Django Tìm Test Như Nào?

Khi chạy:

```bash
python manage.py test
```

Django sẽ tìm:

## File

```text
test*.py
```

Ví dụ:

```text
test_models.py
test_services.py
tests/test_api.py
```

---

## Method

```python
def test_xxx(self):
```

Chỉ method bắt đầu bằng:

```text
test_
```

mới được chạy.

---

# 8. Test Độc Lập

Mỗi test:

- chạy riêng
- setUp chạy lại
- data không nên phụ thuộc test khác

Ví dụ:

```python
def test_a(self):
    ...

def test_b(self):
    ...
```

KHÔNG nên:

- test_b phụ thuộc test_a tạo data trước.

---

# 9. SQLite In-Memory vs MySQL Test DB

## SQLite Memory

```python
NAME = ":memory:"
```

DB chỉ nằm trong RAM.

Test xong:

- DB biến mất hoàn toàn.

---

## MySQL test_xxx_db

Ví dụ:

```text
test_wky_api_db
```

DB tồn tại thật trong MySQL trong lúc test chạy.

Có thể nhìn thấy bằng Workbench.

Nếu dùng:

```bash
python manage.py test --keepdb
```

DB còn tồn tại sau test.

---

# 10. Mindset Quan Trọng

Test không phải:

- chỉ để pass
- chỉ để coverage đẹp

Mà là để:

```text
- chống bug
- verify business logic
- refactor an toàn
- đảm bảo system hoạt động đúng
```

---

# Phase 1 Bạn Đã Học

✅ Test là gì
✅ Django TestCase
✅ Arrange - Act - Assert
✅ assertEqual
✅ assertTrue / assertFalse
✅ assertRaises
✅ full_clean()
✅ setUp()
✅ self trong test
✅ test database
✅ test độc lập nhau
✅ happy path & fail path
✅ cách chạy test
✅ table ≠ data
✅ test DB không copy data từ DB thật
✅ migration seed data / fixture / setUpTestData
✅ rollback trong test
✅ unit test vs API/integration test
✅ SQLite memory vs MySQL test DB

---

# Phase Tiếp Theo

PHASE 2 — MODEL TESTING

Sẽ học:

- test **str**
- test field
- test validation
- test custom method
- test relationship
- test business rule
- test model clean()
- test full_clean()
