# DRF GenericAPIView và Mixins Core

Bài này học phần `GenericAPIView + Mixins` trong DRF.

Đây là bước nằm giữa:

```text
APIView
-> GenericAPIView + Mixins
-> Generic class-based views
-> ViewSet / Router
```

Bạn đã biết APIView rồi. Với APIView, mình tự viết gần như toàn bộ logic:

```python
class TaskListAPIView(APIView):
    def get(self, request):
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
```

Vấn đề là khi làm CRUD, các đoạn này lặp lại rất nhiều:

- lấy queryset
- lấy object
- khởi tạo serializer
- validate
- save
- delete
- return Response

`GenericAPIView` sinh ra để gom các phần lặp đó thành base behavior.

Docs DRF nói `GenericAPIView` extends từ `APIView`, thêm các behavior thường cần cho list view và detail view. Các concrete generic views của DRF được build bằng cách kết hợp `GenericAPIView` với một hoặc nhiều mixin classes.

---

## 1. Hiểu ngắn gọn GenericAPIView là gì

Có thể hiểu:

```text
APIView = nền API class cơ bản
GenericAPIView = APIView + các helper cho model/queryset/serializer
```

APIView chỉ biết:

- request
- response
- method `get`/`post`/`put`/`patch`/`delete`
- exception handling
- content negotiation

Còn `GenericAPIView` thêm các thứ liên quan đến CRUD model:

- `queryset`
- `serializer_class`
- `get_queryset()`
- `get_serializer()`
- `get_object()`
- `get_serializer_class()`
- `lookup_field`

Tức là thay vì trong từng method bạn tự viết:

```python
tasks = Task.objects.all()
serializer = TaskSerializer(tasks, many=True)
```

DRF muốn bạn khai báo:

```python
queryset = Task.objects.all()
serializer_class = TaskSerializer
```

Rồi generic view/mixin sẽ dùng các khai báo đó.

---

## 2. Vì sao cần GenericAPIView?

Với APIView, bạn viết explicit, dễ hiểu nhưng dễ lặp.

Ví dụ list:

```python
queryset = Task.objects.all()
serializer = TaskSerializer(queryset, many=True)
return Response(serializer.data)
```

Create:

```python
serializer = TaskSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
return Response(serializer.data, status=201)
```

Detail:

```python
task = get_object_or_404(Task, pk=pk)
serializer = TaskSerializer(task)
return Response(serializer.data)
```

Update:

```python
task = get_object_or_404(Task, pk=pk)
serializer = TaskSerializer(task, data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
return Response(serializer.data)
```

Delete:

```python
task = get_object_or_404(Task, pk=pk)
task.delete()
return Response(status=204)
```

Bạn thấy các pattern này lặp lại quanh:

- queryset
- object lookup
- serializer
- save/delete
- response/status

`GenericAPIView` và mixins giúp chuẩn hóa các pattern đó.

---

## 3. Hai thuộc tính quan trọng nhất

Với `GenericAPIView`, thường có 2 thuộc tính core:

```python
queryset = Task.objects.all()
serializer_class = TaskSerializer
```

Docs nói `queryset` là queryset dùng để return object từ view, còn `serializer_class` là serializer dùng cho validate/deserialize input và serialize output. Thường bạn phải set 2 thuộc tính này hoặc override method tương ứng như `get_queryset()` hoặc `get_serializer_class()`.

Ví dụ:

```python
class TaskListBaseAPIView(GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Ý nghĩa:

```text
queryset:
Nguồn dữ liệu chính của view là Task.objects.all()
```

```text
serializer_class:
View này dùng TaskSerializer để xử lý input/output
```

Chỗ cần nhớ:

```text
APIView tự viết logic nhiều.
GenericAPIView khai báo queryset + serializer_class để DRF helper/mixin dùng lại.
```

---

## 4. `queryset` dùng để làm gì?

`queryset` là nguồn dữ liệu mặc định của view.

Ví dụ:

```python
queryset = Task.objects.all()
```

Nó được dùng cho:

- list nhiều object
- retrieve một object
- update một object
- delete một object

Nhưng docs có một lưu ý quan trọng: nếu override method trong view, nên gọi `self.get_queryset()` thay vì truy cập trực tiếp `self.queryset`, vì `self.queryset` có thể bị evaluate một lần và cache kết quả cho các request sau.

Tức là nên nghĩ:

```python
queryset = self.get_queryset()
```

hơn là:

```python
queryset = self.queryset
```

---

## 5. `get_queryset()` dùng để làm gì?

`get_queryset()` trả về queryset dùng cho view.

Mặc định, nó lấy từ:

```python
queryset = ...
```

Nhưng bạn có thể override để queryset động theo request.

Ví dụ tư duy:

```python
def get_queryset(self):
    return Task.objects.filter(owner=self.request.user)
```

Ý nghĩa:

```text
Mỗi user chỉ thấy task của chính họ.
```

Hoặc tối ưu query:

```python
def get_queryset(self):
    return Task.objects.select_related("project").all()
```

Ý nghĩa:

```text
Khi serializer cần project, dùng select_related để tránh N+1 query.
```

Docs cũng note nếu serializer access relation và gây N+1 query, bạn có thể tối ưu queryset trong `get_queryset()` bằng `select_related()` hoặc `prefetch_related()`.

Chốt phần này:

```text
queryset = dữ liệu mặc định
get_queryset() = cách lấy dữ liệu linh hoạt hơn
```

Giai đoạn basic chỉ cần biết:

- Nếu dữ liệu cố định: dùng `queryset`.
- Nếu dữ liệu phụ thuộc request/user/filter: override `get_queryset()`.

---

## 6. `serializer_class` dùng để làm gì?

`serializer_class` khai báo serializer view sẽ dùng.

Ví dụ:

```python
serializer_class = TaskSerializer
```

Nó được dùng cho:

- serialize output
- validate input
- create/update object

Thay vì tự gọi:

```python
serializer = TaskSerializer(...)
```

`GenericAPIView` có helper:

```python
serializer = self.get_serializer(...)
```

`self.get_serializer()` sẽ biết serializer class nào cần dùng thông qua `serializer_class`.

---

## 7. `get_serializer_class()` dùng để làm gì?

Mặc định, `get_serializer_class()` trả về:

```python
self.serializer_class
```

Nhưng có thể override khi muốn dùng serializer khác nhau theo case.

Ví dụ tư duy:

```python
def get_serializer_class(self):
    if self.request.method == "GET":
        return TaskDetailSerializer
    return TaskWriteSerializer
```

Ý nghĩa:

```text
GET dùng serializer nhiều field để hiển thị.
POST/PUT/PATCH dùng serializer dành cho input.
```

Docs cũng nói `get_serializer_class()` có thể override để có behavior động, ví dụ dùng serializer khác nhau cho read/write hoặc theo loại user.

Chốt phần này:

```text
serializer_class = serializer mặc định
get_serializer_class() = chọn serializer động
```

Phần `get_serializer_class()` nên biết, nhưng chưa cần đào sâu quá sớm.

---

## 8. `get_serializer()` là gì?

Đây là helper của `GenericAPIView`.

Thay vì viết:

```python
serializer = TaskSerializer(task)
```

hoặc:

```python
serializer = TaskSerializer(data=request.data)
```

Trong generic view bạn có thể dùng:

```python
serializer = self.get_serializer(task)
```

hoặc:

```python
serializer = self.get_serializer(data=request.data)
```

Điểm hay là `get_serializer()` sẽ tự lấy class từ `get_serializer_class()`.

Flow:

```text
self.get_serializer(...)
-> self.get_serializer_class()
-> TaskSerializer(...)
```

Vì vậy, khi bạn override `get_serializer_class()`, toàn bộ chỗ gọi `self.get_serializer()` sẽ tự dùng serializer đúng.

---

## 9. `get_object()` là gì?

`get_object()` dùng cho detail view.

Ví dụ detail/update/delete đều cần lấy một object:

```text
GET /tasks/1/
PUT /tasks/1/
PATCH /tasks/1/
DELETE /tasks/1/
```

Với APIView, bạn thường tự viết:

```python
task = get_object_or_404(Task, pk=pk)
```

Với `GenericAPIView`, có sẵn:

```python
task = self.get_object()
```

`get_object()` mặc định dùng `lookup_field` để tìm object từ queryset. Docs nói `get_object()` trả về object instance dùng cho detail views, mặc định dùng `lookup_field` để filter base queryset.

Mặc định:

```python
lookup_field = "pk"
```

Tức là URL có `pk`, nó lấy object theo `pk`.

Có thể hiểu:

```text
self.get_object()
-> lấy queryset từ self.get_queryset()
-> tìm object theo pk
-> nếu không có thì 404
-> check object permission nếu có
-> trả object
```

Chốt phần này:

```text
APIView: tự get_object_or_404
GenericAPIView: dùng self.get_object()
```

---

## 10. `lookup_field` là gì?

Mặc định detail view tìm object theo:

```python
lookup_field = "pk"
```

Nghĩa là:

```text
/tasks/1/ -> tìm Task pk=1
```

Nếu muốn tìm theo slug, có thể đổi:

```python
lookup_field = "slug"
```

Khi đó tư duy là:

```text
/tasks/my-task-slug/ -> tìm Task slug="my-task-slug"
```

Giai đoạn basic chỉ cần biết:

- Mặc định dùng `pk`.
- Khi cần dùng `slug`/`uuid` thì mới quan tâm `lookup_field`.

---

## 11. Mixins là gì?

`GenericAPIView` chỉ cung cấp nền:

- `queryset`
- `serializer_class`
- `get_queryset()`
- `get_serializer()`
- `get_object()`

Nhưng nó chưa tự biết list/create/update/delete.

CRUD action nằm trong mixins.

DRF có các mixin chính:

- `ListModelMixin`
- `CreateModelMixin`
- `RetrieveModelMixin`
- `UpdateModelMixin`
- `DestroyModelMixin`

Có thể hiểu:

```text
GenericAPIView = nền
Mixin = hành động
```

Ví dụ:

```text
GenericAPIView + ListModelMixin = có khả năng list
GenericAPIView + CreateModelMixin = có khả năng create
GenericAPIView + RetrieveModelMixin = có khả năng retrieve
GenericAPIView + UpdateModelMixin = có khả năng update
GenericAPIView + DestroyModelMixin = có khả năng delete
```

Docs liệt kê các mixins này trong phần Generic views và cho biết concrete generic views được build bằng cách combine `GenericAPIView` với một hoặc nhiều mixin classes.

---

## 12. Các mixins tương ứng CRUD

### ListModelMixin

Dùng cho list nhiều object.

Nó cung cấp method:

```python
list(request, *args, **kwargs)
```

Tư duy bên trong:

```python
queryset = self.get_queryset()
serializer = self.get_serializer(queryset, many=True)
return Response(serializer.data)
```

### CreateModelMixin

Dùng cho create object.

Nó cung cấp method:

```python
create(request, *args, **kwargs)
```

Tư duy bên trong:

```python
serializer = self.get_serializer(data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
return Response(serializer.data, status=201)
```

### RetrieveModelMixin

Dùng cho detail một object.

Nó cung cấp method:

```python
retrieve(request, *args, **kwargs)
```

Tư duy bên trong:

```python
object = self.get_object()
serializer = self.get_serializer(object)
return Response(serializer.data)
```

### UpdateModelMixin

Dùng cho update object.

Nó cung cấp method:

```python
update(request, *args, **kwargs)
partial_update(request, *args, **kwargs)
```

Tư duy bên trong:

```python
object = self.get_object()
serializer = self.get_serializer(object, data=request.data)
serializer.is_valid(raise_exception=True)
serializer.save()
return Response(serializer.data)
```

Với partial update thì thêm:

```python
partial=True
```

### DestroyModelMixin

Dùng cho delete object.

Nó cung cấp method:

```python
destroy(request, *args, **kwargs)
```

Tư duy bên trong:

```python
object = self.get_object()
object.delete()
return Response(status=204)
```

---

## 13. Nhưng mixin không tự map HTTP method

Đây là chỗ rất quan trọng.

Mixin cung cấp action như:

- `list()`
- `create()`
- `retrieve()`
- `update()`
- `partial_update()`
- `destroy()`

Nhưng với `GenericAPIView + mixins`, bạn vẫn phải tự map HTTP method vào action.

Ví dụ tư duy:

```python
class TaskListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

Chỗ cần nhớ:

```text
get() gọi self.list()
post() gọi self.create()
```

Tức là:

```text
HTTP method handler: get/post/put/patch/delete
CRUD action từ mixin: list/create/retrieve/update/partial_update/destroy
```

Cầu nối giữa hai bên là code bạn viết trong class.

---

## 14. Vì sao sau đó có Generic Class-Based Views?

Vì đoạn mapping này vẫn hơi lặp:

```python
def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)
```

Nên DRF tạo sẵn các concrete generic views.

Ví dụ:

```text
ListCreateAPIView
= GenericAPIView + ListModelMixin + CreateModelMixin
+ đã map GET -> list, POST -> create
```

Và:

```text
RetrieveUpdateDestroyAPIView
= GenericAPIView
+ RetrieveModelMixin
+ UpdateModelMixin
+ DestroyModelMixin
+ đã map GET -> retrieve, PUT/PATCH -> update, DELETE -> destroy
```

Docs cũng liệt kê concrete generic views như `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`; ví dụ `ListCreateAPIView` cung cấp `get` và `post` method handlers, còn `RetrieveUpdateDestroyAPIView` cung cấp `get`, `put`, `patch`, `delete` handlers.

Vậy bài sau sẽ dễ hiểu hơn:

```text
GenericAPIView + Mixins
-> concrete generic views
```

---

## 15. Hình dung tầng abstraction

```text
APIView
  |
  | thêm queryset, serializer_class, get_queryset(), get_object()
  v
GenericAPIView
  |
  | thêm hành động CRUD bằng mixins
  v
GenericAPIView + Mixins
  |
  | DRF ghép sẵn HTTP method -> action
  v
Concrete Generic Views
  |
  | gom action theo resource, router tự sinh URL
  v
ViewSet + Router
```

Đây là flow quan trọng nhất của bài.

---

## 16. GenericAPIView khác APIView ở đâu?

| APIView | GenericAPIView |
|:---|:---|
| Base class API cơ bản | Base class cho model-based API |
| Tự viết queryset | Có `queryset` / `get_queryset()` |
| Tự gọi serializer class | Có `serializer_class` / `get_serializer()` |
| Tự lấy object | Có `get_object()` |
| Tự xử lý list/create/update/delete | Kết hợp mixins để có action |
| Phù hợp logic custom | Phù hợp CRUD/model API |

Nói ngắn gọn:

```text
APIView cho bạn toàn quyền.
GenericAPIView cho bạn bộ khung CRUD chuẩn hơn.
```

---

## 17. Khi nào dùng APIView, khi nào dùng GenericAPIView?

Dùng APIView khi:

- API không map trực tiếp với model.
- Logic rất custom.
- Endpoint kiểu report, dashboard, export, webhook.
- Bạn muốn tự kiểm soát toàn bộ flow.

Dùng `GenericAPIView` hoặc generic views khi:

- API làm việc với model/queryset.
- Có serializer rõ ràng.
- CRUD gần chuẩn.
- Muốn giảm code lặp.
- Muốn tận dụng `get_queryset`/`get_object`/`get_serializer`.

Ví dụ:

```text
Task CRUD API -> GenericAPIView/generic views/ViewSet hợp lý.
API tính thống kê dashboard -> APIView có thể hợp lý hơn.
```

---

## 18. Kết luận bài 8

Sau bài này, bạn cần chốt:

- `GenericAPIView` = `APIView` + helper cho queryset/serializer/object lookup.
- `queryset` = nguồn dữ liệu mặc định.
- `serializer_class` = serializer mặc định.
- `get_queryset()` = lấy queryset linh hoạt, nên dùng thay vì `self.queryset` trong method.
- `get_serializer()` = tạo serializer dựa trên `serializer_class`/`get_serializer_class()`.
- `get_object()` = lấy một object cho detail/update/delete.
- Mixins = các action CRUD có sẵn: `list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`.
- `GenericAPIView + mixins` vẫn cần map `get`/`post`/`put`/`patch`/`delete` sang action.
- Concrete generic views là bước tiếp theo vì DRF đã map sẵn HTTP method sang action.

---

## Note

Các phần như `get_serializer_context()`, `filter_queryset()`, `paginate_queryset()`, `perform_create()`, `perform_update()`, `perform_destroy()` là nhóm kiến thức deep-dive của `GenericAPIView` / Generic Views.

Hiện tại chưa cần học sâu. Khi gặp case thực tế như cần truyền thêm `request` vào serializer, filter/pagination queryset, hoặc custom logic lúc create/update/delete, sẽ search docs chính thức DRF và update thêm vào file deep-dive riêng.
