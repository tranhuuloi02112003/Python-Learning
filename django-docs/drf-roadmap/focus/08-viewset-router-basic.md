# DRF ViewSet và Router Basic

Bài này là cầu nối từ `APIView` sang `ViewSet`.

Mục tiêu chính:

```text
Hiểu ViewSet dùng action thay vì get/post trực tiếp.
```

Router chỉ cần hiểu ở mức cơ bản:

```text
Router có thể tự sinh URL và tự map HTTP method vào action.
```

Trong project thực tế của bạn, phần quan trọng hơn Router là manual mapping:

```python
SomeViewSet.as_view({
    "get": "some_business_method",
})
```

Phần đó sẽ học kỹ ở bài tiếp theo.

---

## 1. Nhắc lại APIView

Với `APIView`, method trong class thường trùng với HTTP method.

```python
class TaskAPIView(APIView):
    def get(self, request):
        ...

    def post(self, request):
        ...
```

Mapping:

```text
GET  /tasks/ -> get()
POST /tasks/ -> post()
```

Tư duy:

```text
APIView nghĩ theo HTTP method.
```

---

## 2. ViewSet khác APIView ở đâu?

Với `ViewSet`, ta thường không viết:

```python
def get(self, request):
    ...

def post(self, request):
    ...
```

Mà viết theo action:

```python
class TaskViewSet(ViewSet):
    def list(self, request):
        ...

    def create(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...
```

Tư duy:

```text
ViewSet nghĩ theo action của resource.
```

Ví dụ resource là `Task`, thì action thường là:

- `list`: lấy danh sách task
- `create`: tạo task
- `retrieve`: lấy chi tiết một task
- `update`: cập nhật toàn bộ task
- `partial_update`: cập nhật một phần task
- `destroy`: xóa task

---

## 3. Mapping quan trọng nhất

Đây là bảng cần nhớ:

| HTTP/API | ViewSet action | Ý nghĩa |
|:---|:---|:---|
| `GET /tasks/` | `list()` | Lấy danh sách |
| `POST /tasks/` | `create()` | Tạo mới |
| `GET /tasks/<pk>/` | `retrieve()` | Lấy chi tiết |
| `PUT /tasks/<pk>/` | `update()` | Update toàn bộ |
| `PATCH /tasks/<pk>/` | `partial_update()` | Update một phần |
| `DELETE /tasks/<pk>/` | `destroy()` | Xóa |

Điểm cần chốt:

```text
APIView: GET -> get()
ViewSet: GET /tasks/ -> list()
ViewSet: GET /tasks/<pk>/ -> retrieve()
```

---

## 4. Vấn đề: ai nối GET vào list?

Với `APIView`, DRF tự hiểu:

```text
GET  -> get()
POST -> post()
```

Với `ViewSet`, phải có một bước mapping:

```text
GET  -> list()
POST -> create()
GET  -> retrieve()
```

Có 2 cách mapping thường gặp:

```text
Cách 1: Router tự map.
Cách 2: Manual mapping bằng as_view({...}).
```

Project của bạn quan trọng hơn ở cách 2.

---

## 5. Router là gì?

Router là công cụ của DRF giúp tự sinh URL cho ViewSet.

Ví dụ:

```python
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = router.urls
```

Router sẽ tự sinh route kiểu:

```text
GET    /tasks/       -> list()
POST   /tasks/       -> create()
GET    /tasks/<pk>/  -> retrieve()
PUT    /tasks/<pk>/  -> update()
PATCH  /tasks/<pk>/  -> partial_update()
DELETE /tasks/<pk>/  -> destroy()
```

Bạn không cần tự viết:

```python
path("tasks/", ...)
path("tasks/<int:pk>/", ...)
```

Vì Router sinh dựa trên convention.

Ở giai đoạn này, chỉ cần nhớ:

```text
Router = tự sinh URL + tự map HTTP method vào action chuẩn.
```

---

## 6. Manual mapping là gì?

Manual mapping là tự khai báo HTTP method nào gọi action nào.

Ví dụ:

```python
TaskViewSet.as_view({
    "get": "list",
    "post": "create",
})
```

Nghĩa là:

```text
GET  -> list()
POST -> create()
```

Ví dụ detail:

```python
TaskViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})
```

Nghĩa là:

```text
GET    -> retrieve()
PUT    -> update()
PATCH  -> partial_update()
DELETE -> destroy()
```

Project thực tế của bạn hay dùng manual mapping với tên method theo business:

```python
SomeViewSet.as_view({
    "get": "get_task_logged",
    "post": "approve_task",
})
```

Phần này sẽ học kỹ ở bài 09.

---

## 7. ModelViewSet là gì?

`ModelViewSet` là ViewSet có sẵn full CRUD action chuẩn.

```python
from rest_framework import viewsets


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Với đoạn này, DRF cung cấp sẵn:

- `list`
- `create`
- `retrieve`
- `update`
- `partial_update`
- `destroy`

Hiểu đơn giản:

```text
ModelViewSet = ViewSet có sẵn CRUD chuẩn quanh một model.
```

Nó phù hợp khi API là CRUD chuẩn.

---

## 8. ReadOnlyModelViewSet là gì?

Nếu API chỉ cho đọc dữ liệu, dùng:

```python
class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Nó chỉ có:

- `list`
- `retrieve`

Mapping:

```text
GET /tasks/      -> list()
GET /tasks/<pk>/ -> retrieve()
```

Phù hợp với API chỉ đọc như:

- danh sách category
- danh sách status
- public data
- user list/detail chỉ đọc

---

## 9. ViewSet có làm code dễ hiểu hơn không?

Có và không.

`APIView`:

```text
Rõ nhất, nhưng viết nhiều code.
```

`ViewSet + Router`:

```text
Gọn hơn cho CRUD chuẩn, nhưng mapping bị ẩn hơn.
```

`ViewSet + manual mapping`:

```text
Vẫn dùng action của ViewSet,
nhưng URL/action được khai báo rõ trong urls.py.
```

Vì project của bạn dùng nhiều API business custom, manual mapping thường dễ đọc hơn Router.

---

## 10. Chỗ dễ nhầm

### Nhầm 1: ViewSet tự gọi `get()`

Không đúng.

ViewSet thường dùng action:

```python
def list(self, request):
    ...
```

không phải:

```python
def get(self, request):
    ...
```

### Nhầm 2: Router là bắt buộc

Không đúng.

Bạn có thể dùng Router:

```python
router.register("tasks", TaskViewSet)
```

hoặc manual mapping:

```python
TaskViewSet.as_view({
    "get": "list",
})
```

Cả hai đều được.

### Nhầm 3: Method name bắt buộc phải là `list`, `create`

Không hẳn.

Nếu dùng CRUD chuẩn thì thường là:

```text
list, create, retrieve, update, partial_update, destroy
```

Nhưng nếu manual mapping, có thể dùng tên business:

```python
TaskViewSet.as_view({
    "get": "get_task_summary",
    "post": "approve_task",
})
```

Miễn là trong ViewSet có method tương ứng.

---

## 11. Cần nhớ gì sau bài này?

Chỉ cần chốt các ý này:

- `APIView` dùng `get`/`post`/`put`/`delete`.
- `ViewSet` dùng action như `list`/`create`/`retrieve`/`update`/`partial_update`/`destroy`.
- `Router` có thể tự sinh URL và tự map method vào action chuẩn.
- `ModelViewSet` có full CRUD action chuẩn.
- `ReadOnlyModelViewSet` chỉ có `list` và `retrieve`.
- Project của bạn quan trọng hơn ở manual mapping bằng `as_view({...})`.

---

## 12. Đọc tiếp bài nào?

Sau bài này, đọc kỹ:

```text
09-viewset-as-view-manual-mapping.md
```

Vì project thực tế của bạn hay dùng:

```python
SomeViewSet.as_view({
    "get": "some_business_method",
})
```

Flow cần đọc được:

```text
URL -> HTTP method -> as_view mapping -> ViewSet method
```
