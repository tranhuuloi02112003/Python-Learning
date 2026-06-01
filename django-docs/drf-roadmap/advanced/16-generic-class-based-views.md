# DRF Generic Class-Based Views Core

Bài trước bạn đã học:

```text
GenericAPIView + Mixins
```

Nghĩa là `GenericAPIView` cung cấp nền:

- `queryset`
- `serializer_class`
- `get_queryset()`
- `get_serializer()`
- `get_object()`

Mixins cung cấp action:

- `list()`
- `create()`
- `retrieve()`
- `update()`
- `partial_update()`
- `destroy()`

Nhưng khi dùng trực tiếp `GenericAPIView + Mixins`, mình vẫn phải tự map HTTP method:

```python
def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)
```

DRF thấy pattern này lặp lại nhiều, nên cung cấp sẵn Generic Class-Based Views.

Hiểu ngắn gọn:

```text
Generic Class-Based Views
= GenericAPIView + Mixins + DRF đã map sẵn HTTP method
```

---

## 1. Generic Class-Based Views là gì?

Generic class-based views là các class DRF tạo sẵn để xử lý các pattern API phổ biến.

Import:

```python
from rest_framework import generics
```

Sau đó có thể dùng:

```python
generics.ListAPIView
generics.CreateAPIView
generics.ListCreateAPIView
generics.RetrieveAPIView
generics.UpdateAPIView
generics.DestroyAPIView
generics.RetrieveUpdateDestroyAPIView
```

Các class này giúp bạn không cần tự viết:

- `def get(...)`
- `def post(...)`
- `def put(...)`
- `def patch(...)`
- `def delete(...)`

nếu logic CRUD của bạn theo pattern chuẩn.

---

## 2. Vấn đề của GenericAPIView + Mixins

Ví dụ nếu tự dùng mixins:

```python
class TaskListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

Phần quan trọng thực ra chỉ là:

```python
queryset = Task.objects.all()
serializer_class = TaskSerializer
```

Còn đoạn này gần như lặp lại ở mọi list/create API:

```python
def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)
```

Vậy DRF tạo sẵn:

```python
generics.ListCreateAPIView
```

để mình viết gọn hơn.

---

## 3. ListCreateAPIView

`ListCreateAPIView` dùng cho endpoint dạng collection.

Ví dụ:

```text
/tasks/
```

Nó thường xử lý 2 hành động:

```text
GET  -> list
POST -> create
```

Với `GenericAPIView + Mixins`, tư duy là:

```text
GenericAPIView
+ ListModelMixin
+ CreateModelMixin
+ map GET -> list()
+ map POST -> create()
```

DRF đã đóng gói sẵn thành:

```python
generics.ListCreateAPIView
```

Code minh họa:

```python
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Ý nghĩa:

```text
GET /tasks/
-> tự gọi logic list
```

```text
POST /tasks/
-> tự gọi logic create
```

Bạn không thấy `get()` và `post()` trong class, vì `ListCreateAPIView` đã có sẵn.

---

## 4. RetrieveUpdateDestroyAPIView

`RetrieveUpdateDestroyAPIView` dùng cho endpoint dạng detail.

Ví dụ:

```text
/tasks/<pk>/
```

Nó thường xử lý:

```text
GET     -> retrieve
PUT     -> update
PATCH   -> partial_update
DELETE  -> destroy
```

Tư duy bên dưới:

```text
GenericAPIView
+ RetrieveModelMixin
+ UpdateModelMixin
+ DestroyModelMixin
+ map GET -> retrieve()
+ map PUT -> update()
+ map PATCH -> partial_update()
+ map DELETE -> destroy()
```

DRF đóng gói sẵn thành:

```python
generics.RetrieveUpdateDestroyAPIView
```

Code minh họa:

```python
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Ý nghĩa:

```text
GET /tasks/1/
-> lấy chi tiết task 1
```

```text
PUT /tasks/1/
-> update toàn bộ task 1
```

```text
PATCH /tasks/1/
-> update một phần task 1
```

```text
DELETE /tasks/1/
-> xóa task 1
```

Bạn không cần tự viết `get`, `put`, `patch`, `delete` nếu logic chuẩn.

---

## 5. Các generic views thường gặp

### ListAPIView

Dùng cho API chỉ list.

```text
GET /tasks/
```

Tư duy:

```text
ListAPIView
= GenericAPIView + ListModelMixin
```

Code:

```python
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

### CreateAPIView

Dùng cho API chỉ create.

```text
POST /tasks/
```

Tư duy:

```text
CreateAPIView
= GenericAPIView + CreateModelMixin
```

Code:

```python
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

### ListCreateAPIView

Dùng cho API vừa list vừa create.

```text
GET  /tasks/
POST /tasks/
```

Tư duy:

```text
ListCreateAPIView
= GenericAPIView + ListModelMixin + CreateModelMixin
```

Code:

```python
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Đây là class rất hay gặp.

### RetrieveAPIView

Dùng cho API chỉ lấy chi tiết một object.

```text
GET /tasks/1/
```

Tư duy:

```text
RetrieveAPIView
= GenericAPIView + RetrieveModelMixin
```

Code:

```python
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

### UpdateAPIView

Dùng cho API chỉ update object.

```text
PUT   /tasks/1/
PATCH /tasks/1/
```

Tư duy:

```text
UpdateAPIView
= GenericAPIView + UpdateModelMixin
```

Code:

```python
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

### DestroyAPIView

Dùng cho API chỉ delete object.

```text
DELETE /tasks/1/
```

Tư duy:

```text
DestroyAPIView
= GenericAPIView + DestroyModelMixin
```

Code:

```python
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

### RetrieveUpdateDestroyAPIView

Dùng cho API detail đầy đủ.

```text
GET     /tasks/1/
PUT     /tasks/1/
PATCH   /tasks/1/
DELETE  /tasks/1/
```

Tư duy:

```text
RetrieveUpdateDestroyAPIView
= GenericAPIView
+ RetrieveModelMixin
+ UpdateModelMixin
+ DestroyModelMixin
```

Code:

```python
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Đây cũng là class rất hay gặp.

---

## 6. Bảng tổng hợp

| Generic view | Method hỗ trợ | Mixin bên dưới | Dùng cho |
|:---|:---|:---|:---|
| `ListAPIView` | `GET` | `ListModelMixin` | List nhiều object |
| `CreateAPIView` | `POST` | `CreateModelMixin` | Create object |
| `ListCreateAPIView` | `GET`, `POST` | `ListModelMixin`, `CreateModelMixin` | List + Create |
| `RetrieveAPIView` | `GET` | `RetrieveModelMixin` | Detail một object |
| `UpdateAPIView` | `PUT`, `PATCH` | `UpdateModelMixin` | Update object |
| `DestroyAPIView` | `DELETE` | `DestroyModelMixin` | Delete object |
| `RetrieveUpdateDestroyAPIView` | `GET`, `PUT`, `PATCH`, `DELETE` | `RetrieveModelMixin`, `UpdateModelMixin`, `DestroyModelMixin` | Detail + Update + Delete |

---

## 7. Vì sao chỉ cần queryset và serializer_class?

Vì các generic views đã biết flow chuẩn.

Ví dụ `ListCreateAPIView` đã biết:

Nếu `GET`:

- lấy queryset
- serialize `many=True`
- return `Response(serializer.data)`

Nếu `POST`:

- lấy `request.data`
- validate serializer
- save
- return `Response(serializer.data, status=201)`

Nên bạn chỉ cần khai báo:

```python
queryset = Task.objects.all()
serializer_class = TaskSerializer
```

Tức là bạn nói với DRF:

```text
API này làm việc với data nào?
-> Task.objects.all()
```

```text
API này dùng serializer nào?
-> TaskSerializer
```

Còn flow chuẩn thì DRF đã có sẵn.

---

## 8. Generic views khác APIView ở đâu?

Với APIView, bạn tự viết rõ từng method:

```python
class TaskListAPIView(APIView):
    def get(self, request):
        ...

    def post(self, request):
        ...
```

Với generic view:

```python
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

So sánh:

| APIView | Generic Views |
|:---|:---|
| Tự viết method `get`/`post`/`put`/`delete` | DRF viết sẵn method theo pattern |
| Linh hoạt nhất | Gọn hơn cho CRUD chuẩn |
| Phù hợp logic custom | Phù hợp model CRUD |
| Dễ nhìn rõ flow | Ít code hơn |
| Lặp code nếu CRUD nhiều | Giảm lặp code nhiều |

Nói ngắn gọn:

```text
APIView = tự viết flow
Generic Views = dùng flow CRUD chuẩn DRF đã viết sẵn
```

---

## 9. Generic views khác GenericAPIView + Mixins ở đâu?

Với `GenericAPIView + Mixins`, bạn vẫn tự map method:

```python
class TaskListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

Với generic view:

```python
class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Khác biệt chính:

```text
GenericAPIView + Mixins:
Bạn tự ghép nền + action + method mapping.
```

```text
Generic Views:
DRF đã ghép sẵn nền + action + method mapping.
```

Vậy generic views là version tiện dụng hơn của `GenericAPIView + Mixins`.

---

## 10. Khi nào dùng Generic Views?

Nên dùng Generic Views khi:

- API map trực tiếp với model/queryset.
- CRUD theo pattern chuẩn.
- Không có quá nhiều logic đặc biệt.
- Bạn muốn code ngắn và rõ.

Ví dụ phù hợp:

- Task list/create
- Task detail/update/delete
- Project list/create
- Project detail/update/delete
- Category list
- User profile detail

Không nên ép dùng generic views khi:

- API không map với một model cụ thể.
- Logic xử lý quá custom.
- Response không theo flow CRUD chuẩn.
- Endpoint dạng dashboard/report/statistics/export/import/webhook.

Các case đó dùng APIView có thể hợp lý hơn.

---

## 11. Custom thì làm ở đâu?

Generic views không có nghĩa là không custom được.

Bạn vẫn có thể override:

- `get_queryset()`
- `get_serializer_class()`
- `perform_create()`
- `perform_update()`
- `perform_destroy()`

Ví dụ tư duy:

```python
def get_queryset(self):
    return Task.objects.filter(owner=self.request.user)
```

Hoặc:

```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

Nhưng các phần này thuộc nhóm deep-dive. Hiện tại chỉ cần biết:

```text
Generic views có sẵn flow chuẩn,
nhưng vẫn cho phép override khi cần custom.
```

---

## 12. Mối liên hệ với ViewSet/Router

Generic views vẫn cần bạn khai báo URL thủ công.

Ví dụ tư duy:

```text
/tasks/      -> TaskListCreateView
/tasks/<pk>/ -> TaskDetailView
```

Còn ViewSet/Router sẽ đi thêm một bước:

```text
TaskViewSet
-> router tự sinh:
   /tasks/
   /tasks/<pk>/
```

Nên flow abstraction là:

```text
APIView
-> GenericAPIView + Mixins
-> Generic Class-Based Views
-> ViewSet + Router
```

Bài này nằm ngay trước ViewSet/Router.

---

## 13. Điểm cần nhớ nhất

Nếu bạn chỉ nhớ một câu:

```text
Generic Class-Based Views là các class DRF ghép sẵn GenericAPIView + Mixins + HTTP method mapping.
```

Ví dụ quan trọng nhất:

```text
ListCreateAPIView
= list + create cho collection endpoint
```

```text
RetrieveUpdateDestroyAPIView
= retrieve + update + delete cho detail endpoint
```

---

## 14. Kết luận bài 9

Sau bài này, bạn cần chốt:

- Generic views giúp giảm code CRUD chuẩn.
- `GenericAPIView` cung cấp nền queryset/serializer/object lookup.
- Mixins cung cấp action CRUD.
- Generic views ghép sẵn `GenericAPIView + Mixins + HTTP method mapping`.
- `ListCreateAPIView` dùng cho list/create.
- `RetrieveUpdateDestroyAPIView` dùng cho detail/update/delete.
- Nếu logic quá custom thì dùng APIView.
- Nếu CRUD chuẩn thì dùng Generic Views hoặc sau này ViewSet/Router.
