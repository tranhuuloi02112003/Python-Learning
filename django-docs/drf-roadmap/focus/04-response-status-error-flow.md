# DRF Response, Status và Error Flow

Bài này không học lại HTTP method cơ bản, cũng không học lại validation trong serializer.

Bài này chỉ tập trung vào phần DRF trả response như thế nào cho chuẩn khi làm API.

Khi vào CRUD, bạn sẽ gặp các case:

- `GET` thành công thì trả gì?
- `POST` tạo mới thành công thì status bao nhiêu?
- Validation lỗi thì trả response như nào?
- Không tìm thấy object thì xử lý ra sao?
- `DELETE` thành công có cần trả data không?
- Có nên bọc response bằng `data`, `message`, `errors` không?

Đây là phần nên nắm trước khi thực hành CRUD.

---

## 1. `Response()` trong DRF dùng để làm gì?

Trong DRF, mình thường trả response bằng:

```python
from rest_framework.response import Response
```

Ví dụ:

```python
return Response(serializer.data)
```

Hiểu đơn giản:

```text
serializer.data
-> Python dict/list
-> Response()
-> DRF render thành JSON hoặc browsable API
```

Khi viết DRF API, mình không cần tự dùng `JsonResponse` cho các response thông thường.

---

## 2. Response thành công cơ bản

Với API đọc dữ liệu, thường trả:

```python
return Response(serializer.data)
```

Nếu không truyền `status`, DRF mặc định là:

```text
200 OK
```

Ví dụ:

```python
@api_view(["GET"])
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)
```

Ý nghĩa:

```text
Lấy task thành công
-> trả data của task
-> status mặc định 200 OK
```

---

## 3. Khi nào cần truyền `status=...`?

Với các response đặc biệt, nên truyền rõ status.

Tạo mới thành công:

```python
return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Validation lỗi:

```python
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Delete thành công:

```python
return Response(status=status.HTTP_204_NO_CONTENT)
```

Không tìm thấy:

```python
return Response(status=status.HTTP_404_NOT_FOUND)
```

Nên dùng:

```python
status.HTTP_201_CREATED
```

thay vì:

```python
201
```

Vì code đọc rõ ý nghĩa hơn.

---

## 4. Các status thường dùng trong CRUD

Khi làm CRUD basic, bạn chỉ cần nắm nhóm này trước.

| Case | Status |
|:---|:---|
| `GET` list/detail thành công | `200 OK` |
| `POST` create thành công | `201 Created` |
| `PUT`/`PATCH` update thành công | `200 OK` |
| `DELETE` thành công | `204 No Content` |
| Input invalid | `400 Bad Request` |
| Object không tồn tại | `404 Not Found` |
| Method không được phép | `405 Method Not Allowed` |

Trong DRF code:

```python
from rest_framework import status
```

Sau đó dùng:

```python
status.HTTP_200_OK
status.HTTP_201_CREATED
status.HTTP_204_NO_CONTENT
status.HTTP_400_BAD_REQUEST
status.HTTP_404_NOT_FOUND
status.HTTP_405_METHOD_NOT_ALLOWED
```

Thực tế với `GET` hoặc `PUT`/`PATCH` thành công, nếu không truyền status thì DRF mặc định là `200 OK`, nên có thể không cần ghi rõ.

---

## 5. Response khi GET thành công

### GET list

```python
tasks = Task.objects.all()
serializer = TaskSerializer(tasks, many=True)

return Response(serializer.data)
```

Response thường là list:

```json
[
  {
    "id": 1,
    "title": "Learn DRF",
    "status": "todo"
  },
  {
    "id": 2,
    "title": "Learn CRUD",
    "status": "doing"
  }
]
```

Status:

```text
200 OK
```

### GET detail

```python
task = get_object_or_404(Task, pk=pk)
serializer = TaskSerializer(task)

return Response(serializer.data)
```

Response thường là object:

```json
{
  "id": 1,
  "title": "Learn DRF",
  "status": "todo"
}
```

Status:

```text
200 OK
```

---

## 6. Response khi POST tạo mới thành công

Khi tạo mới thành công, nên trả:

```python
return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Ví dụ:

```python
serializer = TaskSerializer(data=request.data)

if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Response:

```json
{
  "id": 10,
  "title": "New Task",
  "status": "todo"
}
```

Status:

```text
201 Created
```

Vì đây là object vừa được tạo mới, nên `201 Created` đúng nghĩa hơn `200 OK`.

---

## 7. Response khi validation lỗi

Nếu client gửi data sai, serializer sẽ có lỗi.

Ví dụ:

```python
serializer = TaskSerializer(data=request.data)

if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Giả sử thiếu `title`, response có thể là:

```json
{
  "title": [
    "This field is required."
  ]
}
```

Status:

```text
400 Bad Request
```

Ý nghĩa:

```text
Request gửi lên không hợp lệ.
Server hiểu request, nhưng data không pass validation.
```

---

## 8. Dùng `is_valid(raise_exception=True)` thì response lỗi ở đâu?

Trong code thực tế, bạn sẽ hay thấy:

```python
serializer = TaskSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()

return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Ở đây không có đoạn:

```python
return Response(serializer.errors, status=400)
```

Vì:

```python
serializer.is_valid(raise_exception=True)
```

nếu validation fail, DRF sẽ tự raise exception và trả response lỗi `400 Bad Request`.

Tức là:

```python
serializer.is_valid(raise_exception=True)
```

tương đương tư duy với:

```python
if not serializer.is_valid():
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Nhưng code gọn hơn.

---

## 9. Response khi update thành công

Với `PUT` hoặc `PATCH`, nếu update thành công thường trả object sau khi update:

```python
serializer = TaskSerializer(task, data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()

return Response(serializer.data)
```

Status mặc định:

```text
200 OK
```

Response:

```json
{
  "id": 1,
  "title": "Updated Task",
  "status": "done"
}
```

Với `PATCH`, thường có thêm:

```python
serializer = TaskSerializer(task, data=request.data, partial=True)
```

Nhưng phần `partial=True` thuộc serializer update flow, chưa cần học lại sâu ở bài này.

---

## 10. Response khi delete thành công

Với `DELETE`, thường không cần trả data.

Code:

```python
task.delete()
return Response(status=status.HTTP_204_NO_CONTENT)
```

Status:

```text
204 No Content
```

Điểm cần nhớ:

```text
204 nghĩa là xử lý thành công nhưng không có body response.
```

Vì vậy response này thường không trả JSON.

Không nên viết:

```python
return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
```

Vì `204 No Content` đúng nghĩa là không có content.

Nếu bạn muốn trả message, dùng `200 OK`:

```python
return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)
```

Nhưng convention phổ biến của REST API là:

```python
return Response(status=status.HTTP_204_NO_CONTENT)
```

---

## 11. Response khi object không tồn tại

Có 2 cách thường gặp.

### Cách 1: Tự `try/except`

```python
try:
    task = Task.objects.get(pk=pk)
except Task.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
```

Hoặc trả message:

```python
return Response(
    {"detail": "Task not found."},
    status=status.HTTP_404_NOT_FOUND
)
```

### Cách 2: Dùng `get_object_or_404`

```python
from django.shortcuts import get_object_or_404

task = get_object_or_404(Task, pk=pk)
```

Nếu không tìm thấy, Django/DRF sẽ trả lỗi `404`.

Trong API basic, dùng `get_object_or_404` giúp code gọn hơn.

---

## 12. Error response mặc định của DRF

DRF thường dùng key:

```json
{
  "detail": "Not found."
}
```

Hoặc với validation error:

```json
{
  "title": [
    "This field is required."
  ],
  "status": [
    "\"invalid\" is not a valid choice."
  ]
}
```

Có 2 nhóm error phổ biến.

Field error:

```json
{
  "title": ["This field is required."]
}
```

General error:

```json
{
  "detail": "Not found."
}
```

Nên khi tự trả lỗi, bạn có thể dùng style gần với DRF:

```python
return Response(
    {"detail": "Task not found."},
    status=status.HTTP_404_NOT_FOUND
)
```

---

## 13. Có nên bọc response bằng `data`, `message`, `errors` không?

Đây là câu hỏi thực tế.

Có 2 style phổ biến.

### Style 1: Theo DRF default

Success response trả trực tiếp data:

```json
{
  "id": 1,
  "title": "Learn DRF"
}
```

Validation error trả trực tiếp field errors:

```json
{
  "title": [
    "This field is required."
  ]
}
```

Not found:

```json
{
  "detail": "Not found."
}
```

Ưu điểm:

- Đơn giản.
- Đúng style DRF mặc định.
- Ít code custom.
- Dễ học.

Nhược điểm:

- Format response không đồng nhất tuyệt đối giữa success và error.

### Style 2: Bọc response theo format riêng

Ví dụ success:

```json
{
  "success": true,
  "message": "Get task successfully",
  "data": {
    "id": 1,
    "title": "Learn DRF"
  }
}
```

Error:

```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "title": [
      "This field is required."
    ]
  }
}
```

Ưu điểm:

- Frontend dễ xử lý theo format thống nhất.
- Có message rõ ràng.
- Phù hợp team/project có convention riêng.

Nhược điểm:

- Phải custom nhiều hơn.
- Có thể lệch khỏi DRF default.
- Khi dùng generic view/viewset cần thêm custom response.

---

## 14. Giai đoạn học nên chọn style nào?

Ở giai đoạn đang học DRF basic, nên đi theo:

```text
Style 1: DRF default
```

Tức là:

```python
return Response(serializer.data)
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
return Response(status=status.HTTP_204_NO_CONTENT)
```

Lý do:

- Bạn đang học DRF core trước.
- Chưa nên tự custom format quá sớm.
- Cần hiểu default trước rồi mới custom sau.

Sau này khi làm project thực tế, nếu team yêu cầu format thống nhất thì mới bọc:

```json
{
  "success": true,
  "data": {}
}
```

---

## 15. Response flow cho CRUD

Tổng hợp lại, CRUD basic sẽ có flow response như sau.

GET list/detail success:

```text
Response(serializer.data)
-> 200 OK
```

POST create success:

```text
Response(serializer.data, status=201)
-> 201 Created
```

POST/PUT/PATCH validation error:

```text
Response(serializer.errors, status=400)
```

Hoặc:

```text
is_valid(raise_exception=True)
-> DRF tự trả 400
```

PUT/PATCH update success:

```text
Response(serializer.data)
-> 200 OK
```

DELETE success:

```text
Response(status=204)
-> 204 No Content
```

Object not found:

```text
{"detail": "Not found."}
-> 404 Not Found
```

---

## 16. Mẫu code response nên nhớ

Success read/update:

```python
return Response(serializer.data)
```

Success create:

```python
return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Validation error:

```python
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Hoặc:

```python
serializer.is_valid(raise_exception=True)
```

Not found:

```python
return Response(
    {"detail": "Task not found."},
    status=status.HTTP_404_NOT_FOUND
)
```

Delete success:

```python
return Response(status=status.HTTP_204_NO_CONTENT)
```

---

## 17. Kết luận

Sau bài này, bạn cần chốt được:

- `Response(serializer.data)` dùng cho success response.
- `Response(serializer.errors, status=400)` dùng cho validation error.
- `POST` create thành công nên trả `201 Created`.
- `DELETE` thành công thường trả `204 No Content` và không có body.
- DRF default error thường dùng key `detail` hoặc field errors.
- Giai đoạn học basic nên theo DRF default response trước.
- Chưa nên custom format `data`/`message`/`errors` quá sớm.
