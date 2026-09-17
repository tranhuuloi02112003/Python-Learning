# Logger vs Print Khi Debug Django Backend

Bài này giúp phân biệt khi nào dùng `print()` / `CustomPrint`, khi nào nên dùng `logger` trong Django backend.

Mục tiêu:

```text
Không chỉ nhìn lỗi ở terminal,
mà log sao cho sau này đọc lại được,
lọc được,
biết lỗi từ đâu ra,
và có đủ stack trace để điều tra.
```

---

## 1. Debug Không Chỉ Là Nhìn Lỗi

Trong Django backend, debug thường có 2 kiểu chính.

---

## 2. Kiểu 1: Debug Local Bằng `print()` / `CustomPrint`

Ví dụ:

```python
print("data =", data)
```

Hoặc:

```python
CustomPrint().danger("Có lỗi")
```

Cách này nhanh và dễ nhìn khi chạy local.

Nhưng nó có nhiều vấn đề:

- Không biết log đến từ module/file nào.
- Không có level thật như `DEBUG`, `INFO`, `WARNING`, `ERROR`.
- Không có stack trace tự động.
- Khó filter trong Docker logs.
- Khó đẩy lên file, cloud logging, Sentry.
- Dễ bị quên trong code production.

Nên hiểu:

```text
print / CustomPrint phù hợp để debug nhanh tạm thời.
logger phù hợp hơn cho code thật.
```

---

## 3. Kiểu 2: Debug Bằng `logger`

Ví dụ:

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Start sync task_id=%s", task_id)
logger.warning("User mapping not found user_id=%s", user_id)
logger.exception("Error while syncing task_id=%s", task_id)
```

Cách này phù hợp hơn với code thật vì logging của Python/Django có hệ thống:

- logger
- handler
- formatter
- filter
- level

Django cấu hình logging qua biến:

```python
LOGGING
```

trong `settings.py`.

Cấu hình này quyết định:

- log nào được in ra console
- log nào được ghi file
- log nào gửi email/cloud/Sentry
- format log ra sao

---

## 4. Logging Hoạt Động Theo Luồng Nào?

Khi viết:

```python
logger = logging.getLogger(__name__)
logger.warning("Something wrong")
```

nó không đơn giản là `print`.

Flow thực tế:

```text
Code gọi logger
-> Logger kiểm tra level có được phép log không
-> Tạo LogRecord
-> Gửi LogRecord cho Handler
-> Handler quyết định ghi ra đâu: console / file / email / cloud
-> Formatter quyết định format dòng log
```

Ví dụ format log:

```text
[WARNING] 2026-06-01 15:30:10 BPO_Task.views: User mapping not found user_id=123
```

Dòng này có giá trị hơn:

```text
User mapping not found
```

Vì nó cho biết:

- Mức độ: `WARNING`
- Thời gian: `2026-06-01 15:30:10`
- Module: `BPO_Task.views`
- Nội dung lỗi: `User mapping not found user_id=123`

---

## 5. Vì Sao Hay Dùng `logging.getLogger(__name__)`?

Ví dụ trong file:

```python
# BPO_Task/views.py

import logging

logger = logging.getLogger(__name__)
```

Thì `__name__` thường là:

```text
BPO_Task.views
```

Trong file khác:

```python
# __Common/utils/excel.py

import logging

logger = logging.getLogger(__name__)
```

Thì logger name là:

```text
__Common.utils.excel
```

Điểm hay là khi log hiện ra, bạn biết lỗi từ module nào.

Ví dụ:

```text
ERROR BPO_Task.views Error while creating BPO task
ERROR __Common.utils.excel Error while exporting report
ERROR F39_Report_Management.crontab Error while running daily report cron
```

Nếu dùng `print()` hoặc `CustomPrint()`, bạn chỉ thấy text.

Khi Docker logs dài hàng ngàn dòng, rất khó biết dòng đó đến từ đâu.

---

## 6. Hiểu Đúng Các Level Logging

Các level hay dùng:

```text
debug
info
warning
error
exception
```

---

## 6.1. `logger.debug(...)`

Dùng cho thông tin rất chi tiết, chủ yếu để dev xem khi điều tra.

Ví dụ:

```python
logger.debug("request.data=%s", request.data)
logger.debug("query_params=%s", request.query_params)
logger.debug("calculated_score=%s", calculated_score)
```

Dùng khi:

- Muốn xem biến trung gian.
- Muốn xem payload.
- Muốn trace flow xử lý.
- Chỉ nên bật ở local/dev.

Không nên log debug quá nhiều ở production vì:

- dễ ồn log
- có thể lộ data nhạy cảm

---

## 6.2. `logger.info(...)`

Dùng cho sự kiện bình thường nhưng có ý nghĩa nghiệp vụ.

Ví dụ:

```python
logger.info("User created task task_id=%s user_id=%s", task.id, user.id)
logger.info("Start exporting daily report date=%s", report_date)
logger.info("Finish syncing BPO task task_id=%s", task_id)
```

Dùng khi:

- Một job bắt đầu/kết thúc.
- Một action quan trọng xảy ra.
- Muốn trace flow nghiệp vụ ở mức tổng quan.

---

## 6.3. `logger.warning(...)`

Dùng khi có vấn đề bất thường, nhưng hệ thống vẫn chạy tiếp được.

Ví dụ:

```python
logger.warning("User mapping not found user_id=%s", user_id)
logger.warning("Skip invalid task task_id=%s reason=%s", task_id, reason)
```

Dùng khi:

- Data thiếu nhưng không crash.
- Mapping không tồn tại.
- Một case bị skip.
- Có dấu hiệu lỗi nhưng chưa làm fail API/job.

---

## 6.4. `logger.error(...)`

Dùng khi có lỗi thật sự, nhưng bạn đã xử lý được hoặc không cần stack trace.

Ví dụ:

```python
logger.error("Failed to send notification task_id=%s error=%s", task_id, exc)
```

Lưu ý:

```text
logger.error() không tự in stack trace.
```

Muốn có stack trace thì truyền:

```python
logger.error(
    "Failed to send notification task_id=%s",
    task_id,
    exc_info=True,
)
```

---

## 6.5. `logger.exception(...)`

Dùng bên trong `except`.

Đây là cái nên nhớ kỹ nhất.

Ví dụ:

```python
try:
    create_task()
except Exception:
    logger.exception("Error while creating task")
```

`logger.exception()` sẽ:

```text
log ở level ERROR
và tự kèm exception info / stack trace
```

Nói đơn giản:

```python
logger.exception("Something failed")
```

gần tương đương với:

```python
logger.error("Something failed", exc_info=True)
```

Ví dụ log có stack trace:

```text
ERROR BPO_Task.views Error while creating task
Traceback (most recent call last):
  File ".../views.py", line 120, in create
    create_task()
  File ".../services.py", line 45, in create_task
    ...
ValueError: invalid task status
```

Đây là thứ:

```python
CustomPrint().danger(f"Error: {exc}")
```

không cho bạn đầy đủ.

---

## 7. Case Thực Tế: `_base_viewset.py`

Code hiện tại:

```python
try:
    obj_queryset = obj_queryset.annotate(
        **{
            concat_field_name: Concat(*field_names)
        }
    )
    query.add(Q(**{f"{concat_field_name}__{ICONTAINS}": text_search}), Q.OR)
except Exception as exc:
    CustomPrint().danger(f"Lỗi annotation concat: {exc}")
```

Ý nghĩa nghiệp vụ:

```text
Nếu field search là "first_name last_name",
code muốn tạo field concat tạm thời để search full name.
```

Ví dụ:

```text
first_name = "Nguyen"
last_name = "Van A"
```

Code dùng:

```python
Concat(first_name, last_name)
```

để search:

```text
Nguyen Van A
```

Nếu `Concat(*field_names)` lỗi, API không crash. Nó chỉ bỏ qua field search đó.

Nhưng vấn đề debug là dòng này:

```python
CustomPrint().danger(f"Lỗi annotation concat: {exc}")
```

Chỉ cho biết:

```text
Lỗi annotation concat: ...
```

Bạn không biết rõ:

- Field nào bị lỗi?
- Người dùng search text gì?
- Model/queryset nào đang chạy?
- Lỗi từ dòng nào?
- Stack trace đi qua đâu?

---

## 8. Version Tốt Hơn Cho `_base_viewset.py`

Có thể sửa theo hướng:

```python
import logging

logger = logging.getLogger(__name__)

if " " in _field:
    field_names = _field.split(" ")
    concat_field_name = "_".join(field_names) + "_concat"

    try:
        obj_queryset = obj_queryset.annotate(
            **{
                concat_field_name: Concat(*field_names)
            }
        )
        query.add(
            Q(**{f"{concat_field_name}__{ICONTAINS}": text_search}),
            Q.OR,
        )
    except Exception:
        logger.exception(
            "Lỗi annotation concat field=%s concat_field=%s search=%s",
            _field,
            concat_field_name,
            text_search,
        )
```

Khi lỗi, log có thể như:

```text
ERROR Common.base_viewset Lỗi annotation concat field=first_name last_name concat_field=first_name_last_name_concat search=loi
Traceback (most recent call last):
  ...
```

Như vậy khi debug bạn biết ngay field search nào gây lỗi.

Nếu sợ `text_search` chứa dữ liệu nhạy cảm, có thể log ngắn hơn:

```python
logger.exception(
    "Lỗi annotation concat field=%s concat_field=%s",
    _field,
    concat_field_name,
)
```

---

## 9. Vì Sao Không Nên Viết `logger.exception(f"...{exc}")`?

Có thể viết:

```python
logger.exception(f"Lỗi annotation concat: {exc}")
```

Nhưng tốt hơn là:

```python
logger.exception(
    "Lỗi annotation concat field=%s search=%s",
    _field,
    text_search,
)
```

Lý do:

```text
logger.exception() đã tự log exception rồi.
Không cần nhét {exc} vào message nữa.
```

Ví dụ exception là:

```text
FieldError: Cannot resolve keyword 'abc'
```

`logger.exception()` sẽ tự in phần đó trong traceback.

Message nên dùng để bổ sung context nghiệp vụ:

- field nào
- task_id nào
- user_id nào
- report_date nào
- payload nào

Không nên chỉ lặp lại message lỗi.

---

## 10. Vì Sao Dùng `%s` Thay Vì f-string?

Nên viết:

```python
logger.info("user_id=%s task_id=%s", user_id, task_id)
```

Thay vì:

```python
logger.info(f"user_id={user_id} task_id={task_id}")
```

Lý do:

```text
logging hỗ trợ lazy formatting.
```

Nếu level đó đang bị tắt, logging có thể bỏ qua việc format message.

Ví dụ production đang tắt `DEBUG`:

```python
logger.debug("payload=%s", request.data)
```

thì debug log không được format/in ra.

Nhưng với f-string:

```python
logger.debug(f"payload={request.data}")
```

Python vẫn dựng chuỗi trước rồi mới gọi logger.

Lưu ý thêm:

```text
Argument như request.data vẫn có thể được evaluate trước khi gọi logger.
```

Nếu dữ liệu cực nặng hoặc phải tính toán phức tạp:

```python
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("payload=%s", heavy_function())
```

---

## 11. Nên Log Gì Khi Debug Django?

Đừng log chung chung:

```python
logger.exception("Error")
```

Nên log có context:

```python
logger.exception(
    "Error while allocating exp point deliverable_id=%s user_id=%s",
    deliverable_id,
    user_id,
)
```

Một log tốt thường trả lời được:

- Lỗi xảy ra ở flow nào?
- Dữ liệu chính là gì?
- User/task/report/deliverable nào?
- Case đó bị skip hay làm fail API?
- Có stack trace không?

Ví dụ trong view:

```python
logger.info("Create task request user_id=%s", request.user.id)

try:
    task = service.create_task(request.data)
except ValidationError:
    logger.warning(
        "Invalid task payload user_id=%s payload=%s",
        request.user.id,
        request.data,
    )
    raise
except Exception:
    logger.exception(
        "Unexpected error while creating task user_id=%s",
        request.user.id,
    )
    raise
```

Ở đây có 3 tầng:

```text
info      -> user bắt đầu tạo task
warning   -> payload sai, lỗi dự đoán được
exception -> lỗi bất ngờ, cần stack trace
```

---

## 12. Khi Nào Nên `raise`, Khi Nào Chỉ Log Rồi Bỏ Qua?

Đây là điểm quan trọng.

Code hiện tại:

```python
except Exception as exc:
    CustomPrint().danger(...)
```

tức là đang nuốt exception. API vẫn chạy tiếp.

Điều này chỉ nên làm khi lỗi đó không nghiêm trọng.

Ví dụ hợp lý:

```text
Search theo field concat lỗi
-> bỏ qua field đó
-> search các field khác vẫn chạy
```

Nhưng nếu là lỗi nghiệp vụ quan trọng thì không nên nuốt lỗi.

Ví dụ không nên:

```python
try:
    allocate_exp_point()
except Exception:
    logger.exception("Allocate failed")
```

Nếu không `raise`, API có thể trả success trong khi thực tế chưa allocate xong.

Nên viết:

```python
try:
    allocate_exp_point()
except Exception:
    logger.exception(
        "Allocate failed deliverable_id=%s",
        deliverable_id,
    )
    raise
```

Quy tắc dễ nhớ:

| Loại lỗi                       | Cách xử lý                                                       |
| :----------------------------- | :--------------------------------------------------------------- |
| Lỗi phụ, có thể bỏ qua an toàn | log `warning` / `exception` rồi `continue`                       |
| Lỗi chính của nghiệp vụ        | log `exception` rồi `raise`                                      |
| Lỗi validation / user input    | raise `ValidationError` hoặc return `400`, log `warning` nếu cần |

---

## 13. Áp Dụng Trong Project Thực Tế

`CustomPrint` trong project giống công cụ hỗ trợ nhìn terminal đẹp hơn.

Nó hợp cho:

- Test local.
- Script nhỏ.
- In màu để dev dễ nhìn.
- Debug nhanh tạm thời.

Nhưng với code thật như:

- View
- ViewSet
- Service
- Crontab
- Job sync
- Export report
- API xử lý nghiệp vụ

nên dùng:

```python
import logging

logger = logging.getLogger(__name__)
```

Và tùy case dùng:

```python
logger.debug(...)
logger.info(...)
logger.warning(...)
logger.error(...)
logger.exception(...)
```

Riêng trong `except Exception`, mặc định nên nghĩ tới:

```python
logger.exception("Mô tả lỗi + context")
```

---

## 14. Tư Duy Debug Thực Tế Nên Học

Khi gặp bug Django, nên nghĩ theo flow:

1. Bug xảy ra ở request/job nào?
2. Log điểm bắt đầu flow bằng `info`.
3. Log dữ liệu đầu vào quan trọng bằng `debug`.
4. Log các case bất thường nhưng không crash bằng `warning`.
5. Trong `except` dùng `exception` để có stack trace.
6. Nếu lỗi ảnh hưởng nghiệp vụ chính, log xong phải `raise`.
7. Khi đọc log, tìm theo module name, `task_id`, `user_id`, `request_id` nếu có.

Ví dụ flow sync task:

```python
logger.info("Start sync BPO task task_id=%s", task_id)

logger.debug("Sync payload=%s", payload)

if not user_mapping:
    logger.warning(
        "Skip sync because user mapping not found user_id=%s",
        user_id,
    )
    return

try:
    response = client.sync_task(payload)
except Exception:
    logger.exception(
        "Error while syncing BPO task task_id=%s user_id=%s",
        task_id,
        user_id,
    )
    raise

logger.info("Finish sync BPO task task_id=%s", task_id)
```

Nhìn log là hiểu flow chạy tới đâu, fail ở đâu.

---

## 15. Tóm Tắt

`CustomPrint().danger()` giúp nhìn lỗi nhanh khi chạy local.

`logger.exception()` giúp debug backend thật sự vì có:

- level
- module name
- cấu hình output
- stack trace

Với Django project thực tế:

```text
View / ViewSet / Service / Crontab / Job
-> dùng logging
```

Chỉ dùng:

```text
print / CustomPrint
```

cho debug tạm thời hoặc script nhỏ.
