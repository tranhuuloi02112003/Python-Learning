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

## 2. Hình dạng code của từng tầng

Mỗi tầng đã có bài riêng dạy sâu. Ở đây chỉ để cạnh nhau cho thấy code **ngắn dần** như thế nào.

**`APIView` — tự viết mọi thứ** → chi tiết: `../focus/07-drf-apiview.md`

```python
class TaskListAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        return Response(TaskSerializer(tasks, many=True).data)
```

**`GenericAPIView` + Mixins — có helper, còn tự map method** → `15-genericapiview-and-mixins.md`

```python
class TaskListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *a, **kw):  return self.list(request, *a, **kw)
    def post(self, request, *a, **kw): return self.create(request, *a, **kw)
```

**Generic Class-Based Views — DRF map sẵn method** → `16-generic-class-based-views.md`

```python
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

**`ViewSet` — gom mọi action của một resource vào một class** → `../focus/08-viewset-router-basic.md`

```python
class TaskViewSet(ViewSet):
    def list(self, request): ...
    def retrieve(self, request, pk=None): ...
    def create(self, request): ...
```

**Router — tự sinh URL cho ViewSet** → `../focus/08-viewset-router-basic.md`

```python
router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")
# GET /tasks/ -> list() ; GET /tasks/1/ -> retrieve() ; POST /tasks/ -> create()
```

**Manual mapping — dùng ViewSet nhưng tự chọn URL** → `../focus/09-viewset-as-view-manual-mapping.md`

```python
path("tasks/", TaskViewSet.as_view({"get": "list", "post": "create"})),
```

> Điểm mấu chốt: **Router không thay ViewSet, nó chỉ thay `urls.py`.**
> Bỏ Router đi thì ViewSet vẫn chạy — chỉ là bạn tự map bằng `as_view({...})`.

---

## 3. Bảng So Sánh Nhanh

| Tầng | Bạn viết gì? | URL/mapping | Khi nào dùng? |
|:---|:---|:---|:---|
| `APIView` | `get`, `post`, `put`, `delete` | Tự khai báo URL | API custom, flow đặc biệt |
| `GenericAPIView + Mixins` | `get -> list`, `post -> create` | Tự khai báo URL | Muốn tự compose DRF generic behavior |
| Generic Views | `queryset`, `serializer_class` | Tự khai báo URL | CRUD chuẩn, endpoint rõ |
| ViewSet manual mapping | action method | Tự map bằng `as_view({...})` | Project có nhiều business API custom |
| ViewSet + Router | action method | Router tự sinh URL | CRUD chuẩn, convention rõ |

---

## 4. Chọn Cái Nào Trong Project Hiện Tại?

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

## 5. Kết Luận

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

---

**Điều hướng:** ← `16-generic-class-based-views.md` · `../00-lo-trinh-doc.md` · `../test/18-testing-foundation.md` →
