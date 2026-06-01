# Django Transactions Trong API Basic

> Note: Bài này không đào sâu database isolation level hay lock. Mục tiêu là đọc được `transaction.atomic()` trong API write và tránh hiểu sai rollback.

## 1. Vì sao cần transaction trong API?

Một API write thường không chỉ có một lệnh DB.

Ví dụ sửa phòng ban có thể gồm:

```text
update DepartmentInfo
-> update HOD
-> delete DHOD cũ
-> create DHOD mới
```

Nếu mỗi bước lưu riêng và bước cuối lỗi, DB có thể bị trạng thái dở dang:

```text
Department đã đổi tên
HOD đã đổi
DHOD cũ đã bị xóa
DHOD mới chưa tạo
```

Transaction dùng để gom các thao tác DB liên quan thành một khối nhất quán:

```text
all success -> commit
có lỗi làm transaction fail -> rollback
```

---

## 2. Cần biết gì trước?

Trong Django, cần nắm 3 ý trước:

1. Django mặc định chạy ở `autocommit`.
2. `transaction.atomic()` tạo một vùng all-or-nothing cho DB operations.
3. Rollback tự động của `atomic` dựa vào exception thoát khỏi block, không dựa vào việc API trả response lỗi.

---

## 3. Autocommit mặc định

Django mặc định chạy kiểu:

```text
Nếu không có transaction đang active,
mỗi query DB thường được commit ngay khi query đó thành công.
```

Ví dụ:

```python
department.save()
DepartmentEmployees.objects.filter(...).delete()
DepartmentEmployees.objects.bulk_create(new_dhod)
```

Nếu không bọc transaction:

```text
department.save() thành công -> dữ liệu đã lưu
delete() thành công -> dữ liệu đã xóa
bulk_create() lỗi -> các bước trước không tự quay lại hết
```

Vì vậy những write operations phải đi cùng nhau thường cần `atomic`.

---

## 4. `with transaction.atomic()` dạng block

Đây là kiểu hay gặp khi chỉ muốn bọc một đoạn code:

```python
from django.db import transaction

def edit_department(request):
    param_data = request.data

    with transaction.atomic():
        department = DepartmentInfo.objects.get(id=param_data["department_id"])
        department.name = param_data["name"]
        department.save()

        DepartmentEmployees.objects.filter(
            department=department,
            position__code="dhod",
        ).delete()

        DepartmentEmployees.objects.bulk_create(...)
```

Đọc là:

```text
Các thao tác DB trong block atomic này phải hoàn thành cùng nhau.
```

Nếu block kết thúc bình thường:

```text
commit
```

Nếu exception thoát khỏi block:

```text
rollback
```

---

## 5. `@transaction.atomic` dạng decorator

Nếu cả function là một unit write chung, có thể viết:

```python
from django.db import transaction

@transaction.atomic
def edit_department(request):
    ...
```

So sánh:

| Kiểu | Phạm vi transaction |
|:---|:---|
| `with transaction.atomic():` | Chỉ block nằm trong `with` |
| `@transaction.atomic` | Cả function được decorate |

Khi đọc code, câu hỏi là:

```text
Tác giả muốn bọc đoạn DB nào thành một transaction?
```

---

## 6. Dễ nhầm: `return Response lỗi` không tự rollback

Đây là điểm rất quan trọng khi đọc API.

Ví dụ:

```python
with transaction.atomic():
    department.name = param_data.get("name")
    department.save()

    if has_duplicate_dhod:
        return Response({"detail": "DHOD duplicate"}, status=400)
```

Ở đây block `atomic` kết thúc bằng `return`, không có exception thoát ra.

Nên không được mặc định nghĩ:

```text
API trả 400 -> rollback
```

Trong kiểu flow này, các write đã chạy trước `return` có thể được commit.

### Cách an toàn hơn khi validation fail

Ưu tiên validate trước khi write:

```python
if has_duplicate_dhod:
    return Response({"detail": "DHOD duplicate"}, status=400)

with transaction.atomic():
    department.save()
    ...
```

Nếu lỗi phải làm fail transaction sau khi đã vào write flow, cần dùng pattern rõ ràng để transaction rollback, thường là raise exception phù hợp và xử lý ở ngoài vùng atomic.

---

## 7. Dễ nhầm: bắt exception bên trong `atomic`

Django quyết định commit hay rollback khi thoát khỏi `atomic` dựa vào việc block thoát bình thường hay có exception.

Vì vậy cần cẩn thận với kiểu:

```python
with transaction.atomic():
    try:
        do_db_write()
    except Exception:
        handle_error()
```

Nếu exception bị nuốt bên trong block, code đọc sau đó dễ hiểu sai transaction đang ở trạng thái nào.

Khi cần bắt lỗi DB, pattern dễ đọc hơn thường là:

```python
try:
    with transaction.atomic():
        do_db_write()
except Exception:
    handle_error()
```

Khi đọc project, kiểm tra:

```text
Exception có thoát khỏi atomic block không?
Validation có xảy ra trước write không?
```

---

## 8. `atomic` lồng nhau và savepoint

Bạn có thể gặp:

```python
with transaction.atomic():
    create_parent()

    with transaction.atomic():
        create_children()
```

Đọc mức basic:

- Outer `atomic` là transaction lớn.
- Inner `atomic` thường tạo savepoint.
- Inner block thành công vẫn có thể bị rollback nếu outer block về sau fail.

Chưa cần đào sâu savepoint cho đến khi project có code nested transaction thật.

---

## 9. `ATOMIC_REQUESTS`

Django còn có cấu hình:

```python
ATOMIC_REQUESTS = True
```

Ý tưởng:

```text
Mỗi request view được bọc trong transaction.
```

Nhưng nó là lựa chọn cấu hình cho database của project và có cost riêng.

Khi đang đọc API code, đừng mặc định project bật `ATOMIC_REQUESTS`. Nếu cần biết chính xác, kiểm tra settings.

---

## 10. `on_commit()` biết là có

Đôi khi code cần làm việc sau khi DB commit thành công, ví dụ:

- gửi task background
- gửi email
- cập nhật cache

Django có:

```python
transaction.on_commit(callback)
```

Ở mức basic, chỉ cần nhớ:

```text
Side effect phụ thuộc DB commit đôi khi nên chạy sau commit,
không nên luôn chạy ngay giữa atomic block.
```

---

## 11. Áp vào API edit department

Trong project đang đọc:

```python
with transaction.atomic():
    department_obj = self.model.objects.get(id=department_id)
    department_obj.name = param_data.get("name")
    department_obj.type = param_data.get("type")
    department_obj.description = param_data.get("description")
    department_obj.save()

    # update HOD
    # delete DHOD cũ
    # bulk create DHOD mới
```

Ý đồ transaction:

```text
Sửa DepartmentInfo và sửa DepartmentEmployees phải đi cùng nhau.
```

Điểm cần soi tiếp trong code:

```text
Check DHOD duplicate đang nằm trước hay sau write?
Nếu trả 400 bằng return trong atomic sau khi đã save, rollback có thật sự xảy ra không?
```

---

## 12. Checklist khi đọc transaction trong API

Gặp `transaction.atomic()`, tự hỏi:

1. API này đang write những model/bảng nào?
2. Những write nào phải thành công cùng nhau?
3. Validation xảy ra trước hay sau write?
4. Nếu lỗi xảy ra, exception có thoát khỏi atomic block không?
5. Có `return` lỗi sau khi đã write trong atomic không?
6. Có xóa dữ liệu cũ rồi tạo dữ liệu mới không?
7. Có side effect ngoài DB như cache/email/task không?

---

## 13. Câu chốt

```text
Transaction không phải "API trả lỗi thì DB tự quay lại".
Transaction bảo vệ DB write khi các thao tác nằm trong vùng quản lý transaction
và transaction thật sự đi vào nhánh rollback.
```

Với Django `atomic`, bước đầu tiên khi đọc là nhìn xem block kết thúc bình thường hay có exception thoát ra.

