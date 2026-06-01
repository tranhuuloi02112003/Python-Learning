# Function-Based API với `@api_view`

> Note: Bài này chỉ là ghi chú ngắn về function-based API trong DRF. Project thực tế của bạn focus nhiều hơn vào `APIView`, `ViewSet`, và `ViewSet.as_view({...})`, nên bài này chỉ cần đọc lướt.

---

## 1. `@api_view` là gì?

Trong Django function view thường:

```python
def task_list(request):
    ...
```

Trong DRF function-based API, ta bọc function bằng:

```python
from rest_framework.decorators import api_view


@api_view(["GET"])
def task_list(request):
    ...
```

`@api_view` giúp function view hoạt động theo kiểu DRF:

- Request truyền vào là DRF Request.
- Dùng được `request.data`.
- Có thể trả DRF `Response`.
- Giới hạn HTTP method được phép.
- Hỗ trợ parser/renderer và browsable API.

---

## 2. Giới hạn method

Ví dụ:

```python
@api_view(["GET"])
def task_list(request):
    ...
```

API này chỉ cho phép `GET`.

Nếu client gọi `POST`, DRF sẽ trả:

```text
405 Method Not Allowed
```

Nếu muốn cho phép cả `GET` và `POST`:

```python
@api_view(["GET", "POST"])
def task_list(request):
    ...
```

---

## 3. Ví dụ GET đơn giản

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


@api_view(["GET"])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    return Response(serializer.data)
```

Flow:

```text
GET /tasks/
-> @api_view nhận request
-> query Task
-> serializer many=True
-> Response(serializer.data)
```

---

## 4. Ví dụ GET/POST đơn giản

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Điểm cần nhìn:

```text
GET  -> serialize queryset để trả response
POST -> đọc request.data để validate/create
```

---

## 5. Khác gì với APIView?

`@api_view` dùng cho function-based API:

```python
@api_view(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        ...

    if request.method == "POST":
        ...
```

`APIView` dùng cho class-based API:

```python
class TaskListAPIView(APIView):
    def get(self, request):
        ...

    def post(self, request):
        ...
```

Tư duy:

```text
@api_view = DRF wrapper cho function view
APIView   = DRF base class cho class view
```

---

## 6. Khi nào cần học kỹ?

Học kỹ `@api_view` khi:

- Project dùng nhiều function-based API.
- Bạn muốn viết API nhỏ, đơn giản.
- Bạn đang học DRF từ docs/tutorial cơ bản.

Với project hiện tại, chỉ cần biết khái niệm vì trọng tâm là:

```text
ViewSet.as_view({
    "get": "some_business_method",
})
```

---

## 7. Kết luận

Cần nhớ:

- `@api_view` biến function view thành DRF API view.
- `@api_view(["GET"])` giới hạn API chỉ nhận `GET`.
- Gọi sai method sẽ được DRF trả `405 Method Not Allowed`.
- Function-based API dùng `if request.method == ...`.
- APIView tách method thành `get()`, `post()`.
- Project hiện tại không focus sâu vào `@api_view`, nên đọc lướt là đủ.
