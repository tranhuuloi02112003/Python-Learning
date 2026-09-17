# Custom Response / Base Class Cơ Bản Trong Project

Bài này giúp bạn đọc được pattern response helper trong project thực tế.

Trong DRF chuẩn, bạn thường thấy:

```python
return Response(data, status=status.HTTP_200_OK)
```

Nhưng trong project, bạn có thể gặp:

```python
return self._response_status_200(data)
```

Đây không phải method có sẵn của DRF. Đây là helper do project tự viết.

---

## 1. Vấn đề cần hiểu

Trong DRF chuẩn, khi muốn trả response, ta thường viết:

```python
from rest_framework.response import Response
from rest_framework import status

return Response(
    {
        "message": "Success",
        "data": data
    },
    status=status.HTTP_200_OK
)
```

Hoặc khi lỗi:

```python
return Response(
    {
        "message": "Bad request",
        "errors": errors
    },
    status=status.HTTP_400_BAD_REQUEST
)
```

Nhưng trong dự án thực tế, team thường không muốn mỗi API tự viết response lung tung như vậy.

Vì vậy họ tạo helper chung.

Ví dụ:

```python
return self._response_status_200(data)
```

hoặc:

```python
return self._response_status_400_bad_request(errors)
```

---

## 2. Vì sao project cần custom response?

Vì nếu mỗi API tự return response, format có thể bị lệch.

Ví dụ API A trả:

```json
{
  "data": {},
  "message": "Success"
}
```

API B trả:

```json
{
  "result": {},
  "msg": "OK"
}
```

API C trả:

```json
{
  "success": true,
  "payload": {}
}
```

Như vậy frontend rất khó xử lý.

Nên project thường thống nhất response format.

Ví dụ format chung:

```json
{
  "status": 200,
  "message": "Success",
  "data": {}
}
```

Hoặc:

```json
{
  "success": true,
  "code": 200,
  "data": {},
  "errors": null
}
```

---

## 3. Custom response helper là gì?

Custom response helper là các method được project viết sẵn để return response theo format chung.

Ví dụ:

```python
class BaseHandleAPI:
    def _response_status_200(self, data=None, message="Success"):
        return Response(
            {
                "status": 200,
                "message": message,
                "data": data
            },
            status=status.HTTP_200_OK
        )

    def _response_status_400_bad_request(self, errors=None, message="Bad request"):
        return Response(
            {
                "status": 400,
                "message": message,
                "errors": errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def _response_status_403_forbidden(self, message="Forbidden"):
        return Response(
            {
                "status": 403,
                "message": message
            },
            status=status.HTTP_403_FORBIDDEN
        )
```

Sau đó view kế thừa class này:

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    def get_tasks(self, request):
        data = []

        return self._response_status_200(data)
```

Khi đó thay vì viết `Response(...)` trực tiếp, API dùng helper chung.

---

## 4. Base class là gì trong case này?

Base class là class cha chứa logic dùng chung.

Ví dụ:

```python
class BaseHandleAPI:
    def _response_status_200(self, data=None):
        pass

    def _response_status_400_bad_request(self, errors=None):
        pass
```

Sau đó nhiều API kế thừa:

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    pass

class ProjectViewSet(BaseHandleAPI, ViewSet):
    pass

class DailyReportViewSet(BaseHandleAPI, ViewSet):
    pass
```

Như vậy các view đều có thể dùng:

```python
self._response_status_200()
self._response_status_400_bad_request()
self._response_status_403_forbidden()
```

---

## 5. So sánh DRF chuẩn và project style

### DRF chuẩn

```python
return Response(data, status=status.HTTP_200_OK)
```

Ưu điểm:

- Ngắn.
- Đúng chuẩn DRF.
- Dễ hiểu với người học DRF.

Nhược điểm trong project lớn:

- Mỗi API có thể trả format khác nhau.
- Dễ thiếu message/code/errors.
- Frontend khó thống nhất xử lý.

### Project style

```python
return self._response_status_200(data)
```

Ưu điểm:

- Response thống nhất.
- Giảm lặp code.
- Frontend dễ xử lý.
- Dễ thay đổi format toàn project.

Nhược điểm:

- Người mới vào dự án phải đọc base class trước.
- Không giống docs DRF 100%.
- Cần biết helper đang return gì bên trong.

---

## 6. Ví dụ thực tế khi đọc code

Giả sử trong `urls.py` có:

```python
path(
    "tasks/",
    TaskViewSet.as_view({
        "get": "get_tasks",
    })
)
```

Trong `views.py`:

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    def get_tasks(self, request):
        tasks = Task.objects.all()

        data = [
            {
                "id": task.id,
                "title": task.title,
            }
            for task in tasks
        ]

        return self._response_status_200(data)
```

Bạn đọc flow như sau:

```text
GET /tasks/
-> TaskViewSet.get_tasks()
-> query Task.objects.all()
-> build data
-> return self._response_status_200(data)
```

Đến đây cần biết `_response_status_200` nằm ở đâu.

Thường nó nằm trong file kiểu:

- `base.py`
- `common.py`
- `utils.py`
- `responses.py`
- `base_api.py`
- `base_view.py`

---

## 7. Cách trace custom response trong project

Khi gặp:

```python
return self._response_status_200(data)
```

Bạn làm như sau:

1. Xem class hiện tại kế thừa class nào.
2. Tìm `BaseHandleAPI` / `BaseAPIView` / `BaseViewSet`.
3. Search method `_response_status_200`.
4. Xem bên trong nó return Response format gì.
5. Ghi lại format response chung của project.

Ví dụ:

```python
class DailyReportViewSet(BaseHandleAPI, ViewSet):
    ...
```

Bạn cần mở `BaseHandleAPI` và tìm:

```python
def _response_status_200(...):
    ...
```

---

## 8. Các helper thường gặp

Project có thể có nhiều helper như:

```python
_response_status_200()
_response_status_201_created()
_response_status_400_bad_request()
_response_status_401_unauthorized()
_response_status_403_forbidden()
_response_status_404_not_found()
_response_status_500_internal_server_error()
```

Ý nghĩa cơ bản:

| Helper | Ý nghĩa |
|:---|:---|
| `200` | Request thành công |
| `201` | Tạo mới thành công |
| `400` | Request sai dữ liệu |
| `401` | Chưa đăng nhập / token sai |
| `403` | Không có quyền |
| `404` | Không tìm thấy dữ liệu |
| `500` | Lỗi server |

Khi mới join dự án, chưa cần nhớ hết. Chỉ cần nhớ hay gặp nhất:

- `200`
- `400`
- `403`
- `404`

---

## 9. Ví dụ lỗi validate serializer

DRF chuẩn có thể viết:

```python
serializer = TaskSerializer(data=request.data)

if not serializer.is_valid():
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Project style thường viết:

```python
serializer = TaskSerializer(data=request.data)

if not serializer.is_valid():
    return self._response_status_400_bad_request(serializer.errors)
```

Ý nghĩa:

```text
request data không hợp lệ
serializer.errors chứa lỗi
trả về response 400 theo format chung của project
```

---

## 10. Ví dụ check permission thủ công

Có project sẽ check quyền trong method:

```python
def approve_task(self, request, task_id=None):
    task = Task.objects.get(id=task_id)

    if task.owner != request.user:
        return self._response_status_403_forbidden(
            "You do not have permission to approve this task"
        )

    task.status = "approved"
    task.save()

    return self._response_status_200({
        "id": task.id,
        "status": task.status,
    })
```

Flow:

```text
Lấy task
Check quyền
Nếu không có quyền -> 403
Nếu có quyền -> xử lý business
Trả 200
```

---

## 11. Custom decorator như `CheckDecorator`

Ngoài base class/helper, project thực tế còn hay dùng **decorator** để bọc thêm logic trước khi chạy method chính.

Ví dụ Python decorator đơn giản:

```python
def my_decorator(func):
    def wrapper():
        print("Before")
        return func()

    return wrapper


@my_decorator
def say_hello():
    print("Hello")
```

Khi gọi:

```python
say_hello()
```

Thực tế chạy:

```text
Before
Hello
```

Dòng này:

```python
@my_decorator
```

tương đương với:

```python
say_hello = my_decorator(say_hello)
```

Nghĩa là function gốc bị bọc bởi một function khác, thường gọi là `wrapper`.

Trong project, bạn có thể gặp:

```python
@CheckDecorator.check_entity_exists(ProjectIssueInfo, "issue")
def delete_issue(self, request, *args, **kwargs):
    ...
```

Về bản chất, nó tương đương:

```python
delete_issue = CheckDecorator.check_entity_exists(
    ProjectIssueInfo,
    "issue",
)(delete_issue)
```

Decorator này bọc `delete_issue` bằng một `wrapper`. Wrapper chạy trước method chính.

Flow thường gặp:

```text
Client gọi API delete issue
-> wrapper của CheckDecorator chạy trước
-> lấy issue_id từ kwargs
-> query ProjectIssueInfo
-> nếu không có object: return 404
-> nếu có object: gắn kwargs["issue_obj"] = entity
-> gọi delete_issue(self, request, *args, **kwargs)
```

Ví dụ logic bên trong có thể giống:

```python
entity_id = kwargs.get("issue_id")
entity_qs = ProjectIssueInfo.objects.active(
    id=entity_id,
    is_deleted=False,
)

if not entity_qs.exists():
    return self._response_status_404_not_found()

kwargs["issue_obj"] = entity_qs.first()
return func(self, request, *args, **kwargs)
```

Ý nghĩa của `CheckDecorator` trong case này:

```text
Load object + trả 404 nếu object không tồn tại
trước khi vào API method thật
```

Các logic hay được tách bằng decorator:

- check object tồn tại
- check permission
- logging
- transaction
- validate request
- chuẩn bị object rồi nhét vào `kwargs`

Trong Django/DRF, bạn cũng sẽ gặp nhiều decorator quen thuộc:

```python
@login_required
@permission_required(...)
@transaction.atomic
@api_view(["GET"])
@action(...)
```

Khi đọc một custom decorator, hỏi 4 câu:

| Câu hỏi | Ý nghĩa |
|:---|:---|
| Decorator bọc function nào? | Method thật là gì? |
| Wrapper chạy trước làm gì? | Check object, quyền, log, transaction...? |
| Nếu fail thì return gì? | 400, 403, 404...? |
| Nếu pass thì truyền thêm gì? | Có thêm `kwargs["issue_obj"]` không? |

---

## 12. Chỗ dễ nhầm

### Nhầm 1: Tưởng `_response_status_200` là của DRF

Sai.

DRF không có sẵn method này.

DRF có:

```python
Response(...)
```

Còn:

```python
_response_status_200(...)
```

là project tự viết.

### Nhầm 2: Tưởng helper chỉ đổi status code

Không chỉ vậy.

Helper có thể xử lý thêm:

- format response chung
- message mặc định
- error code
- logging
- translate message
- custom exception
- pagination format

Nên khi đọc project, phải mở helper ra xem.

### Nhầm 3: Không biết method này từ đâu ra

Ví dụ thấy:

```python
self._response_status_200(data)
```

mà trong class hiện tại không có method đó.

Lý do là nó được kế thừa từ class cha:

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    ...
```

Nên method nằm trong `BaseHandleAPI`.

---

## 13. Công thức đọc nhanh

Khi gặp:

```python
return self._response_status_200(data)
```

Hiểu là:

```text
Trả response thành công theo format chung của project
```

Khi gặp:

```python
return self._response_status_400_bad_request(errors)
```

Hiểu là:

```text
Request sai dữ liệu / validate fail
```

Khi gặp:

```python
return self._response_status_403_forbidden()
```

Hiểu là:

```text
User không có quyền thực hiện action
```

Khi gặp:

```python
@CheckDecorator.check_entity_exists(ProjectIssueInfo, "issue")
```

Hiểu là:

```text
Trước khi chạy method chính, project sẽ tự check issue có tồn tại không.
Nếu có, thường object sẽ được truyền tiếp qua kwargs.
Nếu không, API trả 404 sớm.
```

---

## 14. Kết luận

Trong DRF chuẩn:

```python
return Response(data, status=200)
```

Trong project thực tế:

```python
return self._response_status_200(data)
```

Ý nghĩa không đổi nhiều:

```text
đều là trả response về client
```

Nhưng project style có thêm một lớp wrapper để:

- Thống nhất format response.
- Giảm lặp code.
- Dễ maintain toàn bộ API.

Khi join dự án, bạn chỉ cần nhớ:

- `_response_status_xxx` không phải DRF gốc.
- Nó là helper của project.
- Muốn hiểu chính xác response trả gì thì mở base class ra đọc.
- Custom decorator như `CheckDecorator` cũng không phải DRF gốc.
- Muốn hiểu method bị bọc thế nào thì mở decorator ra đọc wrapper.
