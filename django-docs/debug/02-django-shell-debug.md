# Django Shell Khi Debug Backend

Django shell là cách mở Python console nhưng đã load sẵn:

- Django settings
- database connection
- models
- app config
- môi trường backend của project

## 0. Nắm Nhanh

Dùng Django shell khi muốn chủ động hỏi backend/DB:

```text
Thay vì chạy code qua API/UI,
mình vào thẳng môi trường backend để hỏi hệ thống.
```

Hỏi nhanh các câu như:

- DB đang có data gì?
- Query này trả ra gì?
- Service/function này chạy ra kết quả gì?
- Serializer validate như nào?
- Data thật có đúng như mình nghĩ không?

Với project `lift_wky_api`, lệnh hay dùng:

```bash
cd /Users/user/Downloads/wky/lift_wky_api
docker exec -it wky_api_web python manage.py shell_plus
```

Nếu muốn chắc chắn, import rõ ràng hoặc chạy command một dòng:

```bash
docker exec -w /wky_api wky_api_web python manage.py shell -c "from F21_Employee_Management.models import Employee; print(Employee.objects.count())"
```

Khác biệt quan trọng:

| Lệnh | Nguồn gốc | Điểm cần nhớ |
|:-----|:----------|:-------------|
| `shell` | Django built-in | Phải tự import model, rõ ràng, hợp cho `shell -c` |
| `shell_plus` | `django-extensions` | Tự import model, tiện soi data nhanh |

Muốn dùng `shell_plus`, project phải:

1. Cài package `django-extensions`.
2. Thêm vào `INSTALLED_APPS`:

```python
"django_extensions"
```

Nếu thiếu, chạy `python manage.py shell_plus` sẽ báo:

```text
Unknown command: 'shell_plus'
```

Nhớ 4 điểm chính:

1. `shell_plus` tiện vì thường tự import model như `Employee`, `BPOProjectTaskInfo`.
2. Nếu project có 2 class trùng tên, nên tự import rõ ràng để tránh nhầm.
3. QuerySet là lazy, chỉ query DB khi `.count()`, `.first()`, `list(qs)`, loop...
4. Lệnh `save()`, `create()`, `update()`, `delete()` trong shell ghi DB thật.

Tóm tắt:

```text
Logger = theo dõi app khi nó đang chạy.
Django shell = chủ động hỏi backend/DB ngay tại chỗ.
```

---

<details>
<summary>Đọc thêm: ví dụ soi data, QuerySet, SQL, serializer và rollback</summary>

## 1. Chạy Django Shell Trong Project Docker

Với dự án `lift_wky_api`, nên chạy trong Docker container.

Đi tới project:

```bash
cd /Users/user/Downloads/wky/lift_wky_api
```

Mở Django shell:

```bash
docker exec -it wky_api_web python manage.py shell
```

Nếu project có `django_extensions`, có thể dùng bản tiện hơn:

```bash
docker exec -it wky_api_web python manage.py shell_plus
```

`shell_plus` không phải lệnh mặc định của Django.

Nó đến từ package:

```text
django-extensions
```

Muốn dùng được `shell_plus`, project cần:

1. Đã cài package `django-extensions`.
2. Đã thêm vào `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "django_extensions",
]
```

Trong project này đã có:

```text
django_extensions==3.2.3
```

và đã đăng ký:

```python
"django_extensions"
```

trong `INSTALLED_APPS`.

Nếu thiếu package hoặc chưa thêm vào `INSTALLED_APPS`, chạy:

```bash
python manage.py shell_plus
```

sẽ báo kiểu:

```text
Unknown command: 'shell_plus'
```

Khác biệt quan trọng nhất:

| Lệnh | Nguồn gốc | Điểm chính |
|:-----|:----------|:-----------|
| `shell` | Django built-in | Phải tự import model |
| `shell_plus` | `django-extensions` | Thường tự import model |

Ví dụ với `shell`, cần import rõ:

```python
from F21_Employee_Management.models import Employee

Employee.objects.count()
```

Với `shell_plus`, thường có thể gọi thẳng:

```python
Employee.objects.count()
```

Nhưng nếu project có nhiều class trùng tên, `shell_plus` có thể import không đúng class mình nghĩ, hoặc đặt alias.

Khi cần chắc chắn, cứ import rõ ràng:

```python
from F21_Employee_Management.models import Employee
```

Tóm lại:

```text
shell      = chắc chắn, rõ ràng, import tay.
shell_plus = tiện để soi data nhanh, auto import model.
```

---

## 2. Vì Sao Dùng Shell?

Ví dụ đang debug API list task.

Nếu dùng `print`, thường phải:

```text
sửa code
-> restart/reload
-> gọi API lại
-> xem log
```

Còn shell cho phép kiểm tra thẳng:

```python
from BPO_Task.models import BPOProjectTaskInfo

BPOProjectTaskInfo.objects.count()
```

Hoặc soi vài record:

```python
qs = BPOProjectTaskInfo.objects.all()
qs.first()
```

Muốn xem rõ hơn thì dùng `.values()`:

```python
BPOProjectTaskInfo.objects.values(
    "id",
    "bpo_status",
    "original_task_url",
)[:10]
```

Cách này rất hợp khi cần biết:

```text
Data thật trong DB đang như nào?
```

---

## 3. Ví Dụ Soi Employee

Import model:

```python
from F21_Employee_Management.models import Employee
```

Đếm số lượng:

```python
Employee.objects.count()
```

Tìm employee theo account name:

```python
Employee.objects.filter(
    account_name__icontains="hoang"
).values(
    "id",
    "account_name",
    "slack_user_id",
)[:10]
```

Nếu query trả rỗng, lỗi có thể không nằm ở API mà là data không có.

Đây là lý do shell rất mạnh:

```text
Nó giúp tách vấn đề data ra khỏi frontend/API.
```

---

## 4. Ví Dụ Soi BPO Task

Import model:

```python
from BPO_Task.models import BPOProjectTaskInfo
```

Filter task theo URL:

```python
qs = BPOProjectTaskInfo.objects.filter(
    original_task_url__contains="RT-540"
)
```

Đếm kết quả:

```python
qs.count()
```

In vài record:

```python
for item in qs[:10]:
    print(item.id, item.bpo_status, item.original_task_url)
```

---

## 5. Soi Data Quan Hệ Bằng `select_related`

Nếu cần lấy thông tin quan hệ:

```python
qs = BPOProjectTaskInfo.objects.select_related(
    "task",
    "task__assignee_user",
    "task__project_sprint__project",
).filter(
    original_task_url__contains="RT-540"
)
```

In thông tin liên quan:

```python
for item in qs[:10]:
    print(
        item.id,
        item.task.status,
        item.task.assignee_user.account_name if item.task.assignee_user else None,
        item.task.project_sprint.project.code,
    )
```

Đây là kiểu debug data cực thực tế:

```text
Xem object BPO nối qua task, assignee, project có đúng không.
```

---

## 6. Hiểu QuerySet Lazy

Điểm rất quan trọng:

```text
Django QuerySet thường chưa query DB ngay.
```

Ví dụ:

```python
qs = Employee.objects.filter(account_name__icontains="a")
```

Dòng trên mới tạo query.

DB thường chỉ bị gọi khi làm:

```python
qs.count()
list(qs)
qs.first()
```

Hoặc:

```python
for item in qs:
    ...
```

Vì vậy khi debug performance, phải để ý:

```text
Lúc nào query thật sự chạy?
```

---

## 7. Xem SQL Thật

Muốn biết ORM sinh ra SQL gì:

```python
qs = Employee.objects.filter(account_name__icontains="hoang")
print(qs.query)
```

Nếu dùng `shell_plus`, có thể bật in SQL:

```bash
docker exec -it wky_api_web python manage.py shell_plus --print-sql
```

Khi chạy query trong shell, SQL có thể được in ra luôn.

Cách này rất hữu ích khi debug:

- filter
- annotation
- `select_related`
- `prefetch_related`
- query chậm
- query không ra data như mong đợi

---

## 8. Chạy Thử Logic Trong Shell

Shell không chỉ để xem data.

Nó còn dùng để gọi thử function/service.

Ví dụ giả sử có một hàm xử lý nghiệp vụ:

```python
from some_app.services.some_service import some_function

result = some_function(...)
result
```

Lúc này mình test logic trực tiếp, không cần đi qua API.

Nếu hàm lỗi, traceback hiện ngay trong shell.

---

## 9. Debug Serializer Trong Shell

Ví dụ API trả `400` nhưng chưa biết field nào sai.

Có thể test serializer trực tiếp:

```python
from F31_Project_Management.serializers import ProjectTaskInfoSerializer

data = {
    "title": "Test task",
}

serializer = ProjectTaskInfoSerializer(data=data)
serializer.is_valid()
serializer.errors
serializer.validated_data
```

Cách này cực hữu ích để biết:

- field nào thiếu
- field nào sai type
- validation nào đang fail
- serializer có parse data đúng không

---

## 10. Cẩn Thận Khi Ghi DB Trong Shell

Trong shell, các lệnh này ghi DB thật:

```python
obj.save()
Model.objects.create(...)
qs.update(...)
obj.delete()
```

Nên nhớ:

```text
Django shell đang dùng DB thật của môi trường container đó.
```

Nếu chạy trên dev/staging/prod, phải rất cẩn thận.

---

## 11. Test Ghi DB Rồi Rollback

Nếu chỉ muốn test thử rồi rollback:

```python
from django.db import transaction

with transaction.atomic():
    emp = Employee.objects.first()
    emp.account_name = "TEST"
    emp.save()

    raise Exception("rollback")
```

Exception sẽ làm transaction rollback.

Cách này hợp để thử logic ghi DB mà không muốn giữ dữ liệu test.

Một cách khác là dùng `transaction.set_rollback(True)`:

```python
from django.db import transaction

with transaction.atomic():
    emp = Employee.objects.first()
    emp.account_name = "TEST"
    emp.save()

    transaction.set_rollback(True)
```

Ý nghĩa:

```text
Code trong block vẫn chạy,
nhưng DB quay lại trạng thái trước đó.
```

---

## 12. Một Lệnh Nhanh Không Vào Interactive Shell

Khi chỉ muốn check nhanh một câu:

```bash
docker exec -w /wky_api wky_api_web python manage.py shell -c "from F21_Employee_Management.models import Employee; print(Employee.objects.count())"
```

Cách này tiện khi muốn hỏi DB một câu ngắn, ví dụ:

- count record
- check một query
- in vài field quan trọng
- xác nhận data có tồn tại không

---

## 13. Shell vs Logging

`logging` dùng để theo dõi khi app đang chạy.

Ví dụ:

```text
API đang được gọi
job đang chạy
crontab đang sync
service đang xử lý
```

Django shell dùng để chủ động hỏi hệ thống.

Ví dụ:

```text
DB hiện có gì?
Query này ra sao?
Service này chạy thế nào?
Serializer này validate ra sao?
```

Tư duy thực tế khi debug:

```text
Dùng shell trước để xác nhận data/query/logic.
Sau đó mới quyết định có cần breakpoint hoặc log thêm không.
```

---

## 14. Checklist Khi Debug Bằng Django Shell

Khi gặp bug, có thể hỏi theo thứ tự:

1. Model/table có data không?
2. Query filter có trả data không?
3. Quan hệ `ForeignKey`/`select_related` có đúng không?
4. Serializer validate ra sao?
5. Service/function chạy trực tiếp có lỗi không?
6. ORM sinh SQL đúng không?
7. Có đang vô tình ghi DB thật không?

---

## 15. Tóm Tắt

Django shell là môi trường Python đã load sẵn Django.

Nó giúp debug nhanh:

- data thật trong DB
- QuerySet / ORM
- relation giữa models
- SQL sinh ra từ ORM
- service/function
- serializer validation

Nhớ ngắn gọn:

```text
Logger = theo dõi app khi nó đang chạy.
Django shell = chủ động hỏi backend/DB ngay tại chỗ.
```

</details>
