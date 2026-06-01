# DRF Request/Response: Nền tảng trước khi học CRUD

> Note: Bài này chỉ đặt nền cho `request.data`, `Response`, và `status`. Các phần serializer, response error flow, APIView/ViewSet sẽ được học kỹ hơn ở các bài sau, nên ở đây chỉ cần nắm ý chính.

Sau khi đã biết serializer, bước tiếp theo là hiểu cách một API request đi qua DRF.

Flow tổng quát:

```text
Client gửi request
-> Django/DRF nhận request
-> View xử lý request
-> Serializer chuyển object thành data
-> Response trả data ra client
```

Trong phase này, mình chưa học CRUD đầy đủ. Mình chỉ tập trung vào các khối nền tảng:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
```

Và object quan trọng nhất:

```python
request.data
```

DRF mở rộng từ `HttpRequest` thường của Django. Điểm quan trọng khi làm API là DRF cung cấp `request.data`, giúp mình đọc dữ liệu client gửi lên một cách linh hoạt hơn.

---

## 1. Phase này học gì?

Mục tiêu của phase này là hiểu API khác view render template ở đâu.

Bạn cần nắm:

- `request.data`
- `Response`
- `status`
- `@api_view`
- URL mapping tới API view
- GET API đơn giản
- POST API đơn giản

Tạm thời chưa học:

- `PUT`
- `PATCH`
- `DELETE`
- `APIView`
- Generic views
- ViewSet
- Router

Các phần đó sẽ dễ hơn nhiều sau khi bạn hiểu rõ request và response.

---

## 2. Vì sao cần học Request/Response trước CRUD?

CRUD thật ra chỉ là nhiều API nhỏ ghép lại:

| Method | Ý nghĩa |
|:---|:---|
| `GET` | Đọc dữ liệu |
| `POST` | Tạo dữ liệu |
| `PUT` | Cập nhật toàn bộ |
| `PATCH` | Cập nhật một phần |
| `DELETE` | Xóa dữ liệu |

Nếu chưa hiểu request và response, khi học CRUD bạn dễ bị rối ở các câu hỏi:

- Dữ liệu client gửi lên nằm ở đâu?
- Vì sao dùng `request.data`?
- Vì sao POST cần `serializer.is_valid()`?
- Vì sao trả về `Response(serializer.data)`?
- Vì sao lỗi validation trả status `400`?
- Vì sao tạo thành công trả status `201`?

Nên phase này là nền móng trước khi đi vào CRUD.

---

## 3. Request trong DRF là gì?

Trong Django, bạn đã quen với các thuộc tính như:

```python
request.GET
request.POST
request.user
request.method
```

Trong DRF, bạn vẫn có thể gặp các thuộc tính đó, nhưng khi làm API cần nhớ nhất:

```python
request.data
```

`request.data` là nơi chứa dữ liệu client gửi lên trong request body.

Ví dụ client gửi JSON:

```json
{
  "title": "Learn DRF",
  "description": "Understand Request and Response",
  "status": "todo"
}
```

Trong DRF view, mình đọc dữ liệu bằng:

```python
request.data
```

Không nên dùng `request.POST` làm cách chính khi xử lý API JSON.

---

## 4. `request.POST` và `request.data` khác gì?

`request.POST` thường phù hợp với form data của HTML form.

`request.data` phù hợp hơn khi làm API vì nó có thể xử lý nhiều kiểu dữ liệu client gửi lên, ví dụ:

- JSON
- form data
- multipart data

Và `request.data` dùng tốt cho các method:

- `POST`
- `PUT`
- `PATCH`

Ví dụ khi tạo task:

```python
@api_view(["POST"])
def task_create(request):
    serializer = TaskSerializer(data=request.data)
```

Ở đây:

```python
request.data
```

là dữ liệu thô client gửi lên.

Còn:

```python
serializer.validated_data
```

là dữ liệu sau khi serializer validate thành công.

Flow cần nhớ:

```text
request.data
-> Serializer(data=request.data)
-> serializer.is_valid()
-> serializer.validated_data
-> serializer.save()
```

---

## 5. Response trong DRF là gì?

Trong DRF, mình thường trả dữ liệu bằng:

```python
Response(data)
```

Ví dụ:

```python
return Response(serializer.data)
```

`Response` nhận dữ liệu Python như dict hoặc list, sau đó DRF render thành format phù hợp để trả về client, thường là JSON.

Điểm rất dễ nhầm:

```text
Response không bắt buộc toàn bộ data phải đi qua Serializer.
Response cần data đã ở dạng Python render được như dict/list/str/int/bool/None.
```

Serializer thường cần khi data còn là object phức tạp như Django model instance hoặc queryset.

Ví dụ đúng:

```python
tasks = Task.objects.all()
serializer = TaskSerializer(tasks, many=True)

return Response({
    "total_records": tasks.count(),
    "data": serializer.data,
})
```

Ở ví dụ này:

- `tasks` là queryset phức tạp nên cần `TaskSerializer(..., many=True)`.
- Dict bọc ngoài gồm `total_records` và `data` đã là Python data có thể đưa vào `Response`.
- Không cần tạo serializer riêng chỉ vì response có một dict bọc ngoài.

Ví dụ:

```python
tasks = Task.objects.all()
serializer = TaskSerializer(tasks, many=True)
return Response(serializer.data)
```

Flow:

```text
Task object trong database
-> TaskSerializer convert thành Python data
-> Response trả data ra client
```

Điểm quan trọng:

```python
serializer.data
```

là dữ liệu Python đã sẵn sàng để trả ra API.

```python
Response(serializer.data)
```

là response DRF gửi về client.

---

## 6. `status` trong DRF là gì?

Khi trả response, mình thường cần HTTP status code.

Ví dụ tạo thành công:

```python
return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Ví dụ dữ liệu gửi lên không hợp lệ:

```python
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

DRF cung cấp các tên status code dễ đọc:

```python
status.HTTP_200_OK
status.HTTP_201_CREATED
status.HTTP_400_BAD_REQUEST
status.HTTP_404_NOT_FOUND
status.HTTP_405_METHOD_NOT_ALLOWED
```

Nên ưu tiên:

```python
status.HTTP_201_CREATED
```

thay vì viết số cứng:

```python
201
```

Vì code dễ đọc hơn và tránh nhầm ý nghĩa của status code.

---

## 7. `@api_view` là gì?

Để function-based view hoạt động đúng kiểu DRF, mình dùng:

```python
@api_view(["GET"])
def task_list(request):
    ...
```

`@api_view` giúp view nhận request theo kiểu DRF, dùng được `Response`, hỗ trợ xử lý dữ liệu API, và tự xử lý trường hợp client gọi sai method.

Ví dụ:

```python
@api_view(["GET"])
def task_list(request):
    ...
```

Nghĩa là API này chỉ cho phép method `GET`.

Nếu client gọi `POST` vào API này, DRF sẽ trả:

```text
405 Method Not Allowed
```

Nếu muốn cho phép cả `GET` và `POST`, viết:

```python
@api_view(["GET", "POST"])
def task_list(request):
    ...
```

---

## 8. GET API đơn giản

API đầu tiên nên viết là list task.

Mục tiêu:

```text
GET /api/tasks/
```

Code mẫu:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskListSerializer


@api_view(["GET"])
def task_list(request):
    tasks = Task.objects.select_related("project").all()
    serializer = TaskListSerializer(tasks, many=True)

    return Response(serializer.data)
```

Điểm cần hiểu:

```python
tasks = Task.objects.select_related("project").all()
```

Query nhiều task từ database.

```python
serializer = TaskListSerializer(tasks, many=True)
```

Dùng `many=True` vì đang serialize nhiều object.

```python
return Response(serializer.data)
```

Trả dữ liệu ra client.

Flow:

```text
GET /api/tasks/
-> urls.py match URL
-> gọi task_list(request)
-> query Task
-> TaskListSerializer(tasks, many=True)
-> Response(serializer.data)
```

---

## 9. Detail API đơn giản

Sau list API, viết detail API.

Mục tiêu:

```text
GET /api/tasks/1/
```

Code mẫu:

```python
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskDetailSerializer


@api_view(["GET"])
def task_detail(request, pk):
    task = get_object_or_404(
        Task.objects.select_related("project"),
        pk=pk
    )
    serializer = TaskDetailSerializer(task)

    return Response(serializer.data)
```

Điểm cần hiểu:

```python
task = get_object_or_404(..., pk=pk)
```

Lấy một task theo id. Nếu không có, trả lỗi `404`.

```python
serializer = TaskDetailSerializer(task)
```

Không dùng `many=True` vì chỉ serialize một object.

Flow:

```text
GET /api/tasks/1/
-> urls.py lấy pk = 1
-> gọi task_detail(request, pk=1)
-> tìm Task id=1
-> TaskDetailSerializer(task)
-> Response(serializer.data)
```

---

## 10. POST API đơn giản

Sau khi GET list/detail ổn, mới học POST.

Mục tiêu:

```text
POST /api/tasks/
```

Client gửi JSON:

```json
{
  "project": 1,
  "title": "Learn API request",
  "description": "Practice request.data and Response",
  "status": "todo"
}
```

View xử lý:

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskListSerializer, TaskCreateSerializer, TaskDetailSerializer


@api_view(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.select_related("project").all()
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = TaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save()
            output_serializer = TaskDetailSerializer(task)
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
```

Điểm cần hiểu:

```python
TaskCreateSerializer(data=request.data)
```

Dùng khi client gửi input lên.

```python
serializer.is_valid()
```

Kiểm tra dữ liệu có hợp lệ không.

```python
serializer.save()
```

Tạo object trong database.

```python
TaskDetailSerializer(task)
```

Serialize object vừa tạo để trả về client.

```python
status=status.HTTP_201_CREATED
```

Báo rằng tạo dữ liệu thành công.

Nếu validation lỗi:

```python
return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

Flow:

```text
Client gửi JSON
-> DRF đọc vào request.data
-> TaskCreateSerializer(data=request.data)
-> serializer.is_valid()
-> serializer.save()
-> TaskDetailSerializer(task)
-> Response(data, status=201)
```

---

## 11. Object -> data và input -> object

Đây là điểm rất quan trọng.

Khi muốn chuyển object thành data để trả ra API:

```python
serializer = TaskDetailSerializer(task)
return Response(serializer.data)
```

Flow:

```text
Task object -> Serializer -> serializer.data -> Response
```

Khi muốn nhận input từ client để tạo object:

```python
serializer = TaskCreateSerializer(data=request.data)
serializer.is_valid()
task = serializer.save()
```

Flow:

```text
request.data -> Serializer -> is_valid() -> save() -> Task object
```

Nhìn giống nhau nhưng ý nghĩa khác nhau:

| Cách dùng | Ý nghĩa |
|:---|:---|
| `TaskSerializer(task)` | Object -> data |
| `TaskSerializer(tasks, many=True)` | Nhiều object -> list data |
| `TaskSerializer(data=request.data)` | Input data -> validate -> object |

---

## 12. URL mapping cho API

Ví dụ trong `tasks/urls.py`:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("tasks/", views.task_list, name="task-list"),
    path("tasks/<int:pk>/", views.task_detail, name="task-detail"),
]
```

Nếu root URL include như sau:

```python
path("api/", include("tasks.urls"))
```

Thì endpoint đầy đủ là:

```text
GET /api/tasks/
GET /api/tasks/1/
POST /api/tasks/
```

Flow list:

```text
Client gọi /api/tasks/
-> Django urls.py match path
-> gọi task_list(request)
-> view query Task
-> serializer convert object thành data
-> Response trả về client
```

Flow detail:

```text
Client gọi /api/tasks/1/
-> Django urls.py lấy pk = 1
-> gọi task_detail(request, pk=1)
-> view tìm Task id=1
-> serializer convert object thành data
-> Response trả về client
```

---

## 13. Bài thực hành nên làm

Làm theo thứ tự này:

1. Viết `GET /api/tasks/` bằng `@api_view(["GET"])`.
2. Test bằng browser hoặc Postman.
3. Gọi thử `POST /api/tasks/` khi view chỉ cho phép GET để thấy lỗi `405 Method Not Allowed`.
4. Viết `GET /api/tasks/<id>/`.
5. Test id tồn tại.
6. Test id không tồn tại để thấy lỗi `404`.
7. Sau khi GET ổn, thêm `POST /api/tasks/`.
8. Test request data hợp lệ để thấy status `201`.
9. Test request data sai để thấy status `400`.

Chỉ sau khi các bước này rõ ràng, mới chuyển sang `APIView` class và CRUD đầy đủ.

---

## 14. Tóm tắt cần nhớ

`request.data`:

```text
Dữ liệu client gửi lên API
```

`Response(data)`:

```text
Trả dữ liệu từ API về client
```

`status.HTTP_201_CREATED`:

```text
Tạo dữ liệu thành công
```

`status.HTTP_400_BAD_REQUEST`:

```text
Client gửi dữ liệu không hợp lệ
```

`@api_view(["GET"])`:

```text
Function-based API chỉ cho phép GET
```

`serializer = TaskSerializer(task)`:

```text
Object -> data
```

`serializer = TaskSerializer(data=request.data)`:

```text
Input -> validate -> save object
```

Thứ tự học tiếp theo:

```text
Request/Response
-> @api_view
-> URL mapping
-> GET list
-> GET detail
-> POST create
-> APIView
-> CRUD
```
