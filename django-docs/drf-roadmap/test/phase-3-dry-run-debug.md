# PHASE 3 — DRY-RUN DEBUG TRONG DJANGO

# 1. Dry-run Là Gì?

Dry-run là cách chạy thử flow thật của hệ thống:

```text
API / code thật vẫn chạy
logic thật vẫn chạy
model.save() vẫn chạy
service thật có thể được gọi
```

nhưng:

```text
không làm bẩn database thật
không gọi service ngoài thật nếu đã mock
```

Nói ngắn gọn:

```text
Chạy thật để quan sát,
nhưng rollback DB và fake external service.
```

---

# 2. Khi Nào Dùng Dry-run?

Dùng khi cần kiểm tra flow thực tế nhưng chưa muốn ảnh hưởng data thật.

Ví dụ:

```text
Assign task
→ serializer
→ service
→ model.save()
→ detect assignee changed
→ call Slack service
```

Mình muốn biết:

- code có chạy tới Slack service không
- message truyền vào Slack là gì
- task có bị update đúng logic không
- flow có lỗi ở serializer/service/model không

nhưng không muốn:

- đổi assignee thật trong DB
- gửi Slack thật
- tạo log/task/comment thật

---

# 3. Kiến Thức Cần Có

## 3.1. Đọc Được Flow Code

Đây là phần quan trọng nhất.

Cần đọc được luồng:

```text
URL
→ View / ViewSet / APIView
→ Serializer
→ Service
→ Model save()
→ Signal nếu có
→ External service như Slack / Email / Webhook
```

Nếu không biết flow chạy qua đâu, sẽ không biết cần mock cái gì.

---

## 3.2. Django Transaction

Import:

```python
from django.db import transaction
```

Dùng:

```python
with transaction.atomic():
    task.save()
```

Ý nghĩa:

```text
Các thay đổi DB bên trong block sẽ được commit cùng lúc.
```

Nếu muốn chạy xong rồi hủy kết quả DB:

```python
from django.db import transaction

with transaction.atomic():
    task.save()

    transaction.set_rollback(True)
```

Kết quả:

```text
task.save() vẫn chạy
logic trong save/service vẫn chạy
nhưng DB quay lại như trước
```

---

## 3.3. Python mock.patch

Import:

```python
from unittest.mock import patch
```

Ý nghĩa:

```text
Thay function thật bằng function giả.
```

Ví dụ function thật:

```python
send_slack_message()
```

Ta thay bằng:

```python
def fake_send_slack_message(*args, **kwargs):
    print("SLACK CALLED")
    print(args)
    print(kwargs)
```

Dùng patch:

```python
with patch(
    "path.to.send_slack_message",
    fake_send_slack_message
):
    run_code()
```

Code bên trong `with patch(...)` sẽ gọi function giả.

---

## 3.4. Import Path Trong Python

Đây là lỗi rất hay gặp.

Ví dụ trong code có:

```python
from services.slack import send_message
```

Và trong file service đang dùng:

```python
send_message(...)
```

Thường phải patch tại nơi function được import vào để dùng.

Ví dụ:

```python
with patch(
    "tasks.services.send_message",
    fake_send_message
):
    run_code()
```

Không phải lúc nào cũng patch vào file gốc:

```python
services.slack.send_message
```

Quy tắc dễ nhớ:

```text
Patch nơi code đang gọi tên function,
không chỉ patch nơi function được định nghĩa.
```

---

## 3.5. override_settings

Import:

```python
from django.test import override_settings
```

Dùng để fake settings tạm thời.

Ví dụ:

```python
with override_settings(CONFIG_ENV_TYPE="live"):
    run_code()
```

Ý nghĩa:

```text
Trong block này, settings.CONFIG_ENV_TYPE tạm thời là "live".
```

Dùng khi muốn test flow phụ thuộc env/config.

---

## 3.6. Django Shell

Thường chạy:

```bash
python manage.py shell
```

Hoặc nếu project có `django-extensions`:

```bash
python manage.py shell_plus
```

Sau đó chạy thủ công:

```python
task = Task.objects.get(id=1)
task.assignee = user
task.save()
```

Dry-run thường được dùng trong shell để debug nhanh flow thật.

---

# 4. Mẫu Dry-run Cơ Bản

Ví dụ muốn đổi assignee của task để xem Slack có được gọi không.

```python
from django.db import transaction
from unittest.mock import patch

from tasks.models import Task
from users.models import User


def fake_send_slack_message(*args, **kwargs):
    print("SLACK WOULD BE SENT")
    print("args:", args)
    print("kwargs:", kwargs)


task = Task.objects.get(id=1)
user = User.objects.get(id=2)

with transaction.atomic():
    with patch(
        "tasks.services.send_slack_message",
        fake_send_slack_message
    ):
        task.assignee = user
        task.save()

    transaction.set_rollback(True)
```

Kết quả:

```text
task.save() chạy thật
logic detect assignee changed chạy thật
Slack bị thay bằng fake function
DB rollback sau khi chạy xong
```

---

# 5. Mẫu Dry-run Có override_settings

Ví dụ code chỉ gửi Slack khi env là `live`.

```python
from django.db import transaction
from django.test import override_settings
from unittest.mock import patch


def fake_send_slack_message(*args, **kwargs):
    print("SLACK WOULD BE SENT")
    print(args)
    print(kwargs)


with transaction.atomic():
    with override_settings(CONFIG_ENV_TYPE="live"):
        with patch(
            "tasks.services.send_slack_message",
            fake_send_slack_message
        ):
            task.assignee = user
            task.save()

    transaction.set_rollback(True)
```

---

# 6. Debug Trong Dry-run

Dùng `print()` để biết flow chạy tới đâu:

```python
print("STEP 1: before save")
task.save()
print("STEP 2: after save")
```

Hoặc dùng:

```python
breakpoint()
```

Khi code dừng lại ở `breakpoint()`, có thể inspect:

```python
task.assignee
task.status
user.id
```

---

# 7. Checklist Khi Dry-run Không Chạy Như Mong Đợi

## 7.1. Patch Có Đúng Path Không?

Nếu fake function không được gọi, 80% là patch sai path.

Cần kiểm tra file đang gọi function:

```python
from services.slack import send_message
```

Nếu file gọi là:

```text
tasks/services.py
```

thì thường patch:

```python
"tasks.services.send_message"
```

---

## 7.2. Code Có Thật Sự Chạy Vào Nhánh Đó Không?

Ví dụ code chỉ gửi Slack khi:

```python
if old_assignee != new_assignee:
    send_slack_message()
```

Nếu assignee không đổi, Slack sẽ không được gọi.

Debug bằng:

```python
print(old_assignee)
print(new_assignee)
```

---

## 7.3. Có Đang Bị Điều Kiện Env Chặn Không?

Ví dụ:

```python
if settings.CONFIG_ENV_TYPE != "live":
    return
```

Lúc này cần:

```python
with override_settings(CONFIG_ENV_TYPE="live"):
    ...
```

---

## 7.4. Có Nằm Trong transaction.atomic() Không?

Nếu quên:

```python
with transaction.atomic():
```

thì:

```python
transaction.set_rollback(True)
```

sẽ không rollback đúng như mong muốn.

---

# 8. Những Gì Chưa Cần Học Sâu Ban Đầu

Ban đầu chưa cần:

- pytest nâng cao
- fixture phức tạp
- CI/CD
- factory boy
- advanced mocking
- integration test architecture

Chỉ cần nắm:

| Kiến thức | Mức cần |
|:----------|:--------|
| Đọc flow Django | Quan trọng nhất |
| `transaction.atomic()` | Cơ bản |
| `transaction.set_rollback(True)` | Cơ bản |
| `unittest.mock.patch` | Rất quan trọng |
| Import path Python | Quan trọng |
| `override_settings` | Dễ |
| `manage.py shell` | Dễ |
| `print()` / `breakpoint()` | Quan trọng |

---

# 9. Tóm Tắt

Dry-run là kỹ thuật debug backend:

```text
Chạy flow thật
nhưng rollback DB
và mock service ngoài.
```

Nó đặc biệt hữu ích khi debug:

- API update/create phức tạp
- signal
- model.save()
- service layer
- Slack / Email / Webhook
- logic phụ thuộc settings/env

Đây là kỹ năng rất thực tế khi làm Django backend.
