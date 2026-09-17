# So Sánh Các Tầng DRF: APIView, Generic Views, ViewSet

> Note: Đây là bài tổng hợp để nhìn bản đồ DRF. Không cần học sâu `GenericAPIView + Mixins` và `Generic Class-Based Views` ở đây, vì hai phần đó đã có file riêng trong `advanced/15` và `advanced/16`.

Đến hiện tại, bạn cần phân biệt các tầng chính:

```text
APIView
-> GenericAPIView + Mixins
-> Generic Class-Based Views
-> ViewSet
-> Router
```

Bài này trả lời:

- Tầng nào tự viết nhiều?
- Tầng nào DRF viết sẵn nhiều?
- Khi nào dùng APIView?
- Khi nào dùng Generic Views?
- Khi nào dùng ViewSet?
- Router khác ViewSet ở đâu?

---

## 1. Nhìn tổng quan

Tư duy đơn giản:

```text
Càng xuống dưới:
code càng ngắn
convention càng nhiều
mapping càng bị ẩn
```

```text
Càng lên trên:
code rõ hơn
tự kiểm soát nhiều hơn
nhưng viết nhiều boilerplate hơn
```

Các tầng:

| Tầng | Vai trò chính |
|:---|:---|
| `APIView` | Tự viết flow API bằng `get`, `post`, `put`, `delete` |
| `GenericAPIView + Mixins` | Có helper queryset/serializer/object và action CRUD, nhưng còn tự map method |
| Generic Class-Based Views | DRF map sẵn method cho các CRUD pattern phổ biến |
| `ViewSet` | Gom nhiều action của một resource vào một class |
| Router | Tự sinh URL và map HTTP method vào ViewSet action |

---

## 2. APIView là gì trong bản đồ này?

`APIView` là tầng rõ nhất.

Ví dụ:

```python
class TaskAPIView(APIView):
    def get(self, request):
        ...

    def post(self, request):
        ...
```

Tư duy:

```text
GET  -> get()
POST -> post()
```

Bạn tự xử lý:

- query database
- khởi tạo serializer
- validate
- save/delete
- return `Response`
- status code

Nên dùng APIView khi:

- API rất custom.
- API không map rõ với một model.
- Endpoint dạng report/dashboard/webhook/import/export.
- Bạn muốn flow cực kỳ explicit.

Ví dụ:

```text
/api/dashboard/summary/
/api/reports/monthly/
/api/webhook/payment/
```

---

## 3. GenericAPIView + Mixins là gì?

Phần này đã có bài riêng:

```text
advanced/15-genericapiview-and-mixins.md
```

Ở đây chỉ cần hiểu ngắn gọn:

```text
GenericAPIView = APIView + helper cho queryset/serializer/object lookup
Mixins = action CRUD có sẵn
```

`GenericAPIView` thêm các helper:

- `queryset`
- `serializer_class`
- `get_queryset()`
- `get_serializer()`
- `get_object()`

Mixins thêm các action:

- `list()`
- `create()`
- `retrieve()`
- `update()`
- `partial_update()`
- `destroy()`

Nhưng bạn vẫn phải tự map HTTP method:

```python
class TaskListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

Cần nhớ:

```text
GenericAPIView + Mixins = tự ghép nền + action + method mapping.
```

Giai đoạn join project hiện tại: chỉ cần biết khái niệm, chưa cần đào sâu.

---

## 4. Generic Class-Based Views là gì?

Phần này đã có bài riêng:

```text
advanced/16-generic-class-based-views.md
```

Ở đây chỉ cần hiểu:

```text
Generic Class-Based Views
= GenericAPIView + Mixins + DRF map sẵn HTTP method
```

Ví dụ:

```python
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

DRF đã map sẵn:

```text
GET  -> list()
POST -> create()
```

Ví dụ detail:

```python
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

DRF đã map sẵn:

```text
GET    -> retrieve()
PUT    -> update()
PATCH  -> partial_update()
DELETE -> destroy()
```

Nên dùng Generic Views khi:

- CRUD khá chuẩn.
- Muốn endpoint rõ.
- Không muốn viết lặp `get`, `post`, `put`, `delete`.

Nhưng project hiện tại của bạn không focus nhiều vào style này, nên để sau.

---

## 5. ViewSet là gì?

`ViewSet` gom các action liên quan tới cùng một resource vào một class.

Ví dụ:

```python
class TaskViewSet(ViewSet):
    def list(self, request):
        ...

    def create(self, request):
        ...

    def retrieve(self, request, pk=None):
        ...
```

Điểm khác với APIView:

```text
APIView dùng get/post/put/delete.
ViewSet dùng list/create/retrieve/update/partial_update/destroy.
```

Mapping tư duy:

| HTTP/API | ViewSet action |
|:---|:---|
| `GET /tasks/` | `list()` |
| `POST /tasks/` | `create()` |
| `GET /tasks/<pk>/` | `retrieve()` |
| `PUT /tasks/<pk>/` | `update()` |
| `PATCH /tasks/<pk>/` | `partial_update()` |
| `DELETE /tasks/<pk>/` | `destroy()` |

Nên dùng ViewSet khi:

- API xoay quanh một resource.
- Có nhiều action liên quan cùng một model/domain.
- Muốn gom logic vào một class.
- Project dùng style `ViewSet.as_view({...})`.

Với project hiện tại, đây là phần cần ưu tiên hơn Generic Views.

---

## 6. Router là gì?

Router không phải ViewSet.

Router là công cụ tự sinh URL cho ViewSet.

Ví dụ:

```python
router.register("tasks", TaskViewSet, basename="task")
```

Router tự sinh:

```text
GET    /tasks/       -> list()
POST   /tasks/       -> create()
GET    /tasks/<pk>/  -> retrieve()
PUT    /tasks/<pk>/  -> update()
PATCH  /tasks/<pk>/  -> partial_update()
DELETE /tasks/<pk>/  -> destroy()
```

Cần phân biệt:

```text
ViewSet = nơi viết action.
Router  = nơi tự sinh URL và tự map method vào action.
```

Project hiện tại của bạn không phụ thuộc Router nhiều, vì hay dùng manual mapping:

```python
SomeViewSet.as_view({
    "get": "some_business_method",
})
```

---

## 7. Manual Mapping Nằm Ở Đâu?

Manual mapping là cách dùng ViewSet nhưng không dùng Router.

Ví dụ:

```python
TaskViewSet.as_view({
    "get": "list",
    "post": "create",
})
```

Hoặc theo business method:

```python
DailyReportViewSet.as_view({
    "get": "get_task_logged",
})
```

Tức là:

```text
ViewSet vẫn là ViewSet.
Nhưng URL/action không do Router sinh tự động.
Bạn tự khai báo mapping trong urls.py.
```

Phần này đã có bài riêng:

```text
focus/09-viewset-as-view-manual-mapping.md
```

Đây là bài quan trọng với project hiện tại.

---

## 8. Bảng So Sánh Nhanh

| Tầng | Bạn viết gì? | URL/mapping | Khi nào dùng? |
|:---|:---|:---|:---|
| `APIView` | `get`, `post`, `put`, `delete` | Tự khai báo URL | API custom, flow đặc biệt |
| `GenericAPIView + Mixins` | `get -> list`, `post -> create` | Tự khai báo URL | Muốn tự compose DRF generic behavior |
| Generic Views | `queryset`, `serializer_class` | Tự khai báo URL | CRUD chuẩn, endpoint rõ |
| ViewSet manual mapping | action method | Tự map bằng `as_view({...})` | Project có nhiều business API custom |
| ViewSet + Router | action method | Router tự sinh URL | CRUD chuẩn, convention rõ |

---

## 9. Chọn Cái Nào Trong Project Hiện Tại?

Với project hiện tại, ưu tiên đọc theo thứ tự:

```text
APIView
-> ViewSet action
-> ViewSet.as_view({...}) manual mapping
-> Serializer / ORM / custom response
```

Chưa cần ưu tiên sâu:

```text
GenericAPIView + Mixins
Generic Class-Based Views
Router tự sinh URL
```

Vì project đang nghiêng về style:

```python
SomeViewSet.as_view({
    "get": "some_business_method",
    "post": "another_business_method",
})
```

---

## 10. Kết Luận

Cần chốt:

- `APIView`: viết trực tiếp `get/post/put/delete`.
- `GenericAPIView + Mixins`: DRF cho helper và action, nhưng bạn còn tự map method.
- Generic Class-Based Views: DRF map sẵn method cho CRUD pattern phổ biến.
- `ViewSet`: gom action của một resource vào một class.
- Router: tự sinh URL cho ViewSet.
- Manual mapping: tự map HTTP method vào ViewSet action bằng `as_view({...})`.

Với project hiện tại:

```text
Đọc kỹ APIView + ViewSet manual mapping.
GenericAPIView / Generic Views / Router để hiểu nền, đọc sau.
```
