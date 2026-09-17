# ViewSet Manual Mapping bằng `as_view({...})`

Bài này tập trung vào pattern rất quan trọng khi đọc project thực tế:

```python
SomeViewSet.as_view({
    "get": "some_method",
    "post": "create_something",
})
```

Đây là kiểu map URL thủ công từ HTTP method sang action trong ViewSet.

---

## 1. Vấn đề cần hiểu

Trước đó bạn đã học APIView.

Với APIView, ta thường viết:

```python
class TaskAPIView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass
```

URL sẽ map như này:

```python
path("tasks/", TaskAPIView.as_view())
```

Khi request vào:

```text
GET  /tasks/ -> gọi get()
POST /tasks/ -> gọi post()
```

Tức là với APIView, method trong class trùng với HTTP method:

```text
GET    -> get()
POST   -> post()
PUT    -> put()
DELETE -> delete()
```

---

## 2. Nhưng ViewSet thì khác

Với ViewSet, ta không viết `get()` / `post()` trực tiếp.

Thường sẽ viết các action như:

```python
class TaskViewSet(ViewSet):
    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass
```

Lúc này câu hỏi là:

```text
GET thì gọi method nào?
POST thì gọi method nào?
```

Vì trong class không có `get()` hay `post()`.

Đó là lý do ViewSet cần mapping.

---

## 3. Manual mapping là gì?

Manual mapping là tự khai báo:

```python
TaskViewSet.as_view({
    "get": "list",
    "post": "create",
})
```

Nghĩa là:

```text
Nếu request là GET  -> gọi method list()
Nếu request là POST -> gọi method create()
```

Ví dụ đầy đủ:

```python
# urls.py

from django.urls import path
from .views import TaskViewSet

urlpatterns = [
    path(
        "tasks/",
        TaskViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="task-list-create"
    ),
]
```

ViewSet:

```python
# views.py

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status


class TaskViewSet(ViewSet):
    def list(self, request):
        return Response({
            "message": "Get task list"
        })

    def create(self, request):
        return Response(
            {
                "message": "Create task"
            },
            status=status.HTTP_201_CREATED
        )
```

Kết quả:

```text
GET /tasks/
-> gọi TaskViewSet.list()

POST /tasks/
-> gọi TaskViewSet.create()
```

---

## 4. Điểm quan trọng nhất

Với APIView:

```python
TaskAPIView.as_view()
```

DRF tự hiểu:

```text
GET  -> get()
POST -> post()
```

Nhưng với ViewSet:

```python
TaskViewSet.as_view({
    "get": "list",
    "post": "create",
})
```

Bạn phải nói rõ:

```text
GET gọi action nào
POST gọi action nào
```

Vì ViewSet làm việc bằng action, không làm việc trực tiếp bằng `get()` / `post()`.

---

## 5. Ví dụ với detail API

Ví dụ API lấy chi tiết, cập nhật, xóa task:

```python
# urls.py

urlpatterns = [
    path(
        "tasks/<int:pk>/",
        TaskViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }),
        name="task-detail"
    ),
]
```

ViewSet:

```python
class TaskViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        return Response({
            "message": f"Get task detail {pk}"
        })

    def update(self, request, pk=None):
        return Response({
            "message": f"Update task {pk}"
        })

    def destroy(self, request, pk=None):
        return Response({
            "message": f"Delete task {pk}"
        })
```

Mapping:

```text
GET    /tasks/1/ -> retrieve(request, pk=1)
PUT    /tasks/1/ -> update(request, pk=1)
DELETE /tasks/1/ -> destroy(request, pk=1)
```

---

## 6. Vì sao project thực tế hay dùng kiểu này?

Trong docs/tutorial, bạn thường thấy router:

```python
router.register("tasks", TaskViewSet)
```

Router sẽ tự sinh URL và tự map:

```text
GET    /tasks/      -> list()
POST   /tasks/      -> create()
GET    /tasks/{id}/ -> retrieve()
PUT    /tasks/{id}/ -> update()
DELETE /tasks/{id}/ -> destroy()
```

Nhưng trong dự án thực tế, nhiều team muốn tự kiểm soát URL rõ hơn.

Ví dụ:

```python
path(
    "projects/<int:project_id>/tasks/",
    ProjectTaskViewSet.as_view({
        "get": "get_tasks_by_project",
        "post": "create_task_for_project",
    })
)
```

Ở đây method không còn là `list()` hay `create()` chuẩn nữa.

Mà là method theo business:

```text
get_tasks_by_project()
create_task_for_project()
```

Manual mapping giúp project:

- Tự đặt tên method theo business.
- Tự kiểm soát URL.
- Không phụ thuộc hoàn toàn vào router.
- Dễ đọc flow từ `urls.py` vào view method.
- Dễ gắn các API đặc biệt không đúng CRUD chuẩn.

---

## 7. So sánh Router và Manual Mapping

### Router

Dùng router:

```python
router.register("tasks", TaskViewSet)
```

Phù hợp khi API đi theo CRUD chuẩn:

- `list`
- `create`
- `retrieve`
- `update`
- `destroy`

Ưu điểm:

- Ít code `urls.py`.
- DRF tự sinh URL.
- Phù hợp API chuẩn REST.

Nhược điểm:

- Khó nhìn trực tiếp URL đang gọi action nào.
- Không linh hoạt bằng manual mapping với các API business đặc biệt.

### Manual mapping

Dùng manual mapping:

```python
TaskViewSet.as_view({
    "get": "get_tasks_by_project",
    "post": "create_task_for_project",
})
```

Ưu điểm:

- Nhìn `urls.py` biết ngay `GET` gọi method nào.
- Đặt method theo nghiệp vụ dễ hơn.
- Kiểm soát URL rõ hơn.
- Phù hợp project có nhiều API custom.

Nhược điểm:

- `urls.py` dài hơn.
- Phải tự khai báo mapping.
- Dễ sai tên method nếu viết nhầm.

---

## 8. Cách đọc code khi gặp manual mapping

Khi vào dự án gặp đoạn này:

```python
path(
    "users/<int:user_id>/tasks/",
    UserTaskViewSet.as_view({
        "get": "get_user_tasks",
        "post": "create_user_task",
    })
)
```

Bạn đọc theo 4 bước:

1. Xem URL: `users/<int:user_id>/tasks/`
2. Xem HTTP method: `GET` hay `POST`?
3. Xem mapping trong `as_view({...})`.
4. Vào class `UserTaskViewSet` tìm method tương ứng.

Mapping:

```text
GET  -> get_user_tasks
POST -> create_user_task
```

Ví dụ nếu request là:

```text
GET /users/5/tasks/
```

Thì flow là:

```text
urls.py
-> UserTaskViewSet.as_view({"get": "get_user_tasks"})
-> UserTaskViewSet.get_user_tasks(request, user_id=5)
```

Nếu request là:

```text
POST /users/5/tasks/
```

Thì flow là:

```text
urls.py
-> UserTaskViewSet.as_view({"post": "create_user_task"})
-> UserTaskViewSet.create_user_task(request, user_id=5)
```

---

## 9. Ví dụ gần với project thực tế

Giả sử project có API lấy task theo project.

```python
# urls.py

urlpatterns = [
    path(
        "projects/<int:project_id>/tasks/",
        ProjectTaskViewSet.as_view({
            "get": "get_tasks",
            "post": "create_task",
        }),
        name="project-tasks"
    ),
]
```

View:

```python
# views.py

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status


class ProjectTaskViewSet(ViewSet):
    def get_tasks(self, request, project_id=None):
        return Response({
            "project_id": project_id,
            "tasks": []
        })

    def create_task(self, request, project_id=None):
        title = request.data.get("title")

        return Response(
            {
                "project_id": project_id,
                "title": title,
                "message": "Task created"
            },
            status=status.HTTP_201_CREATED
        )
```

Request:

```text
GET /projects/10/tasks/
```

Gọi:

```text
get_tasks(request, project_id=10)
```

Request:

```text
POST /projects/10/tasks/
```

Gọi:

```text
create_task(request, project_id=10)
```

---

## 10. Chỗ dễ nhầm

### Nhầm 1: Tưởng ViewSet tự gọi `get()`

Sai.

Với ViewSet, nếu bạn viết:

```python
class TaskViewSet(ViewSet):
    def get(self, request):
        pass
```

thì không đúng style thường dùng.

ViewSet nên viết action:

```python
class TaskViewSet(ViewSet):
    def list(self, request):
        pass
```

hoặc custom action:

```python
class TaskViewSet(ViewSet):
    def get_tasks(self, request):
        pass
```

Sau đó map:

```python
TaskViewSet.as_view({
    "get": "get_tasks"
})
```

### Nhầm 2: Tưởng Router là bắt buộc

Sai.

Router chỉ là một cách tự động map URL.

Bạn có thể dùng manual mapping:

```python
TaskViewSet.as_view({
    "get": "list"
})
```

hoặc dùng router:

```python
router.register("tasks", TaskViewSet)
```

Cả hai đều được.

### Nhầm 3: Tưởng method name phải là list, create

Không hẳn.

Nếu dùng CRUD chuẩn thì thường là:

- `list`
- `create`
- `retrieve`
- `update`
- `destroy`

Nhưng nếu manual mapping, project có thể đặt tên theo business:

```python
TaskViewSet.as_view({
    "get": "get_task_summary",
    "post": "approve_task",
})
```

Miễn là trong class có method tương ứng:

```python
class TaskViewSet(ViewSet):
    def get_task_summary(self, request):
        pass

    def approve_task(self, request):
        pass
```

---

## 11. Công thức nhớ nhanh

APIView:

```text
HTTP method -> class method cùng tên

GET  -> get()
POST -> post()
```

ViewSet manual mapping:

```text
HTTP method -> action được khai báo trong as_view({...})

GET  -> list()
POST -> create()
GET  -> get_something()
POST -> approve_something()
```

Công thức chính:

```python
SomeViewSet.as_view({
    "http_method": "action_method_name"
})
```

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

---

## 12. Khi join dự án, cần đọc như nào?

Khi gặp một API, đừng đọc view trước.

Hãy đọc theo thứ tự:

1. `urls.py`
2. Tìm `path` tương ứng.
3. Xem `ViewSet.as_view({...})`.
4. Xác định HTTP method map vào method nào.
5. Vào `views.py` tìm method đó.
6. Đọc serializer/query/response bên trong method.

Ví dụ:

```python
path(
    "daily-report/task/",
    DailyReportTaskViewSet.as_view({
        "get": "get_task_logged",
    })
)
```

Bạn hiểu ngay:

```text
GET /daily-report/task/
-> DailyReportTaskViewSet.get_task_logged()
```

Sau đó mới vào method `get_task_logged()` để đọc logic.

---

## 13. Kết luận

Manual ViewSet mapping là cách project tự khai báo:

```text
HTTP method nào sẽ gọi action nào trong ViewSet
```

Nó quan trọng vì trong project thực tế bạn sẽ thường gặp:

```python
SomeViewSet.as_view({
    "get": "some_business_method",
    "post": "another_business_method",
})
```

Bạn chỉ cần nhớ:

- APIView dùng `get`/`post` trực tiếp.
- ViewSet dùng action.
- `as_view({...})` là nơi nối HTTP method với action.

Bài này chưa cần thực hành sâu. Chỉ cần nhìn code và đọc được flow:

```text
URL -> HTTP method -> as_view mapping -> ViewSet method
```
