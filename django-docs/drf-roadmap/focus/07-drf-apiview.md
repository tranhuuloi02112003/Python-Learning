# DRF APIView

Bài này không học lại Django Class-Based View.

Bạn đã biết CBV rồi, nên mình sẽ bỏ qua các phần như:

- Class-based view là gì.
- `get()`/`post()` method trong class là gì.
- `as_view()` là gì.
- `dispatch()` là gì.

Bài này chỉ tập trung vào câu hỏi:

```text
DRF APIView khác Django CBV thường ở điểm nào?
Vì sao APIView là bước trung gian trước ViewSet/Router?
```

---

## 1. APIView là gì?

Hiểu ngắn gọn:

```text
APIView = Class-Based View dành cho API trong Django REST Framework
```

Cú pháp nhìn giống Django CBV:

```python
class TaskListAPIView(APIView):
    def get(self, request):
        ...
```

Nhưng điểm quan trọng là:

```text
APIView thêm các behavior của DRF vào class view.
```

Theo docs DRF, APIView khác view thường ở chỗ:

- Request truyền vào handler là DRF Request.
- Handler có thể trả DRF Response.
- `APIException`, `Http404`, `PermissionDenied` được xử lý thành API response phù hợp.

---

## 2. So sánh nhanh Django CBV và DRF APIView

| Django CBV | DRF APIView |
|:---|:---|
| Dùng cho web page / HTML | Dùng cho API |
| Request là Django `HttpRequest` | Request là DRF `Request` |
| Thường trả `render`, `redirect`, `HttpResponse` | Thường trả `Response` |
| Form xử lý input | Serializer xử lý input/output |
| Lỗi thường tự xử lý hoặc dùng Django exception | DRF exception handling trả response API |
| Output thường là HTML | Output thường là JSON / Browsable API |

Tư duy chuyển đổi:

```text
Django CBV:
request -> form/queryset -> render template
```

```text
DRF APIView:
request -> serializer/queryset -> Response
```

---

## 3. Điểm khác biệt số 1: request là DRF Request

Trong Django CBV thường:

```python
def post(self, request):
    ...
```

`request` thường là Django `HttpRequest`.

Trong DRF APIView:

```python
def post(self, request):
    ...
```

`request` là DRF `Request`.

Điểm quan trọng nhất:

```python
request.data
```

Dùng để lấy data client gửi lên API.

Ví dụ:

```python
class TaskCreateAPIView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        ...
```

DRF docs nói APIView hoặc `@api_view` sẽ đảm bảo request truyền vào handler là instance của DRF Request, thay vì Django `HttpRequest` thường.

Chỗ cần nhớ:

```text
APIView giúp mình dùng request.data trong class-based API.
```

---

## 4. Điểm khác biệt số 2: trả về DRF Response

Trong Django CBV thường, bạn có thể trả:

```python
return render(request, "tasks/list.html", context)
```

hoặc:

```python
return redirect("task-list")
```

Trong DRF APIView, thường trả:

```python
return Response(serializer.data)
```

Ví dụ:

```python
class TaskDetailAPIView(APIView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
```

DRF Response nhận data dạng Python primitive, sau đó DRF dùng content negotiation để render ra content type phù hợp, ví dụ JSON hoặc browsable API.

Tư duy cần nhớ:

```text
Django CBV trả HTML response.
DRF APIView trả API response.
```

---

## 5. Điểm khác biệt số 3: APIView xử lý content negotiation

Đây là phần chỉ cần hiểu ở mức vừa đủ.

Khi dùng:

```python
return Response(serializer.data)
```

DRF chưa render JSON ngay tại dòng đó.

DRF sẽ dựa vào request/client để quyết định output cuối cùng.

Ví dụ:

```text
Client muốn JSON -> trả JSON
Browser mở API -> có thể trả browsable API
```

Docs gọi quá trình này là content negotiation: chọn representation phù hợp để trả về client dựa trên request và renderer hiện có.

Bạn không cần custom phần này lúc học basic.

Chỉ cần nhớ:

```text
APIView + Response giúp DRF tự render response đúng format.
```

---

## 6. Điểm khác biệt số 4: exception handling theo kiểu API

Trong Django CBV thường, nếu validation lỗi hoặc object không tồn tại, bạn thường tự xử lý để render template/error page.

Trong DRF APIView, exception có thể được DRF chuyển thành API response.

Ví dụ:

```python
serializer.is_valid(raise_exception=True)
```

Nếu validation fail, DRF tự trả lỗi dạng API với status `400 Bad Request`.

Hoặc:

```python
task = get_object_or_404(Task, pk=pk)
```

Nếu không tìm thấy, DRF có thể trả response lỗi `404`.

Docs nói exception từ handler method sẽ đi qua `handle_exception`; mặc định DRF xử lý các subclass của `APIException`, Django `Http404`, và `PermissionDenied`, rồi trả response lỗi phù hợp.

Tư duy cần nhớ:

```text
APIView giúp lỗi trong API được trả về theo dạng response API,
không phải HTML page thông thường.
```

---

## 7. APIView so với `@api_view`

Bạn đã học `@api_view` trước đó.

Có thể hiểu:

```text
@api_view = DRF wrapper cho function-based API
APIView   = DRF base class cho class-based API
```

So sánh nhanh:

| `@api_view` | `APIView` |
|:---|:---|
| Function-based | Class-based |
| Logic nhiều method thường dùng `if request.method == ...` | Tách thành `get`, `post`, `put`, `patch`, `delete` |
| Dễ hiểu khi mới bắt đầu | Gọn hơn khi endpoint có nhiều method |
| Phù hợp học Request/Response ban đầu | Phù hợp trước khi lên `GenericAPIView`/ViewSet |

Ví dụ function-based:

```python
@api_view(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        ...

    elif request.method == "POST":
        ...
```

Sang APIView:

```python
class TaskListAPIView(APIView):
    def get(self, request):
        ...

    def post(self, request):
        ...
```

Không phải học lại CBV, chỉ là chuyển cách tổ chức code API.

---

## 8. APIView giúp chuẩn bị cho CRUD như thế nào?

Khi làm CRUD bằng APIView, flow sẽ rất rõ:

```python
class TaskListAPIView(APIView):
    def get(self, request):
        # list

    def post(self, request):
        # create
```

Và:

```python
class TaskDetailAPIView(APIView):
    def get(self, request, pk):
        # detail

    def put(self, request, pk):
        # full update

    def patch(self, request, pk):
        # partial update

    def delete(self, request, pk):
        # delete
```

Điểm hay của APIView:

- Mỗi HTTP method có một method riêng trong class.
- Không cần `if request.method` quá nhiều.
- Flow CRUD dễ nhìn hơn function-based API.

Nhưng APIView vẫn chưa ẩn quá nhiều logic.

Bạn vẫn nhìn rõ:

- queryset/object
- serializer
- `is_valid()`
- `save()`
- `Response()`
- `status`

Đây là lý do nên học APIView trước ViewSet.

---

## 9. Ví dụ APIView list/create

Ví dụ này chỉ để nhìn flow, chưa cần học CRUD sâu.

```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskListSerializer, TaskCreateSerializer


class TaskListAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.select_related("project").all()
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

DRF-specific flow:

```text
GET request
-> APIView tạo DRF Request
-> get()
-> queryset
-> serializer
-> Response
```

```text
POST request
-> APIView tạo DRF Request
-> post()
-> request.data
-> serializer.is_valid()
-> serializer.save()
-> Response(status=201)
```

---

## 10. Vì sao chưa học ViewSet ngay?

ViewSet/Router tiện hơn, nhưng ẩn nhiều thứ hơn.

Trong ViewSet, bạn không viết:

```python
def get(self, request):
    ...
```

mà viết các action:

```python
def list(self, request):
    ...

def retrieve(self, request, pk=None):
    ...

def create(self, request):
    ...

def update(self, request, pk=None):
    ...

def partial_update(self, request, pk=None):
    ...

def destroy(self, request, pk=None):
    ...
```

Docs Tutorial 6 nói ViewSet gần giống View, nhưng thay vì các method handler như `get()` hoặc `put()`, nó dùng các action như `retrieve()` hoặc `update()`. Router có thể tự động sinh URLConf cho ViewSet.

Vì vậy nếu học ViewSet quá sớm, bạn có thể bị mơ hồ:

- `GET` map vào `list` ở đâu?
- `POST` map vào `create` như thế nào?
- URL được sinh ra từ đâu?
- Router làm gì?

APIView là bước trung gian tốt vì nó vẫn explicit.

---

## 11. APIView có phải lựa chọn cuối cùng không?

Không hẳn.

Trong DRF có nhiều level abstraction:

```text
@api_view
-> APIView
-> GenericAPIView + mixins
-> concrete generic views
-> ViewSet
-> ModelViewSet + Router
```

APIView phù hợp khi:

- Bạn muốn tự kiểm soát flow rõ ràng.
- Endpoint có logic custom.
- Bạn đang học nền tảng DRF.
- Bạn chưa muốn dùng abstraction quá cao.

ViewSet/ModelViewSet phù hợp khi:

- CRUD theo pattern chuẩn.
- Muốn giảm code lặp.
- Muốn router tự sinh URL.
- Muốn project nhanh gọn hơn.

Giai đoạn hiện tại bạn nên hiểu APIView trước để không bị ViewSet che mất flow.

---

## 12. Skeleton APIView cần nhớ

Bạn chưa cần thực hành ngay, nhưng nên nhớ khung này:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TaskListAPIView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class TaskDetailAPIView(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
```

Khi vào CRUD thực hành, mình sẽ fill logic vào từng method.

---

## 13. Flow APIView cần nhớ

Flow đầy đủ:

```text
Client gọi API
-> Django URL gọi TaskListAPIView.as_view()
-> APIView initialize DRF Request
-> gọi method tương ứng: get/post/put/patch/delete
-> bên trong method dùng serializer/queryset
-> return Response(...)
-> APIView finalize response
-> DRF render JSON/browsable API
```

Bạn đã biết phần URL/CBV rồi, nên chỗ cần nhớ chỉ là:

```text
APIView initialize request thành DRF Request
và finalize Response theo DRF.
```

Docs cũng mô tả `initialize_request()` đảm bảo request truyền vào handler là DRF Request; `finalize_response()` đảm bảo Response được render đúng content type theo content negotiation.

---

## 14. Kết luận

Sau bài này, bạn cần chốt được:

- APIView không phải học lại CBV.
- APIView là DRF version của CBV dành cho API.
- Trong APIView, `request` là DRF Request nên dùng được `request.data`.
- APIView thường trả DRF `Response`, không trả `render`/`redirect`.
- APIView có content negotiation và exception handling của DRF.
- APIView giúp tổ chức CRUD rõ hơn `@api_view`.
- APIView nên học trước ViewSet vì ViewSet ẩn nhiều mapping hơn.
