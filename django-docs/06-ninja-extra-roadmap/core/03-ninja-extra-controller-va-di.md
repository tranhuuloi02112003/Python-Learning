# ninja-extra: `api_controller` + `ControllerBase` + Dependency Injection

> Tiếp theo `02-pydantic-schema-va-response.md`. Bài này trả lời: Ninja thuần là function độc lập, vậy khi nhiều endpoint cần dùng chung service thì sao?

---

## 1. Vấn Đề Cần Giải Quyết

Ở bài 01, mỗi endpoint Ninja thuần là 1 function riêng. Nếu nhiều endpoint đều cần gọi `AuthService`, `TaskService`... thì Ninja thuần buộc bạn khởi tạo lại service đó **trong từng function**:

```python
# Ninja thuần — lặp lại ở mọi function
@router.post("/create")
def create_task(request, payload: TaskCreateSchema):
    auth_service = AuthService()          # lặp lại
    task_service = TaskService()          # lặp lại
    ...

@router.post("/complete")
def complete_task(request, payload: CompleteTaskSchema):
    auth_service = AuthService()          # lặp lại
    task_service = TaskService()          # lặp lại
    ...
```

`ninja-extra` giải quyết việc này bằng cách thêm **class** vào giữa router và function — giống ý tưởng DRF `ViewSet` gom nhiều action vào 1 class.

---

## 2. `api_controller` — Gắn Prefix Path Cho Cả Class

```python
@api_controller("/tasks", tags=["Task Management"])
class TaskController(ControllerBase):
```

Đọc dòng này:

```text
@api_controller("/tasks", ...)
    → mọi method http_get/http_post... bên trong class này
      đều có URL bắt đầu bằng "/tasks"
tags=["Task Management"]
    → chỉ để nhóm hiển thị trong OpenAPI/Swagger docs, không ảnh hưởng logic
```

So với DRF:

```text
@api_controller("/tasks")   ≈  router.register("tasks", TaskViewSet)
```

Cả hai đều là "khai 1 prefix path dùng chung cho nhiều endpoint của cùng 1 resource".

---

## 3. `ControllerBase` — Class Cha Bắt Buộc

```python
class TaskController(ControllerBase):
```

`ControllerBase` là class cha **bắt buộc** phải kế thừa để `@api_controller` hoạt động đúng. Nó cung cấp:

- `self.context` — nơi chứa `request` hiện tại và metadata khác của ninja-extra.
- Cơ chế để `@http_get`/`@http_post`... nhận diện method nào thuộc controller nào.

Tư duy đơn giản: `ControllerBase` với ninja-extra ≈ `ViewSet`/`APIView` với DRF — class nền để framework biết "đây là 1 nhóm endpoint có tổ chức", không phải function rời rạc.

---

## 4. `__init__` — Nơi Khai Dependency Cho Controller

Mỗi khi có request tới, ninja-extra không tự gọi `TaskController()` như 1 class Python bình thường — nó tạo controller qua 1 dependency injector chạy ngầm (chi tiết cơ chế thật, verify bằng source code, để ở bài `advanced/14-dependency-injection-thuc-su-qua-injector.md`). Điều cần biết ngay ở bài này: injector đó vẫn luôn gọi `__init__` của bạn, nên có 2 cách viết đều hợp lệ.

**Cách 1 — tự khởi tạo service trong `__init__`:**

```python
def __init__(self):
    self.auth_service = AuthService()
    self.task_service = TaskService()
    self.notification_service = NotificationService()
```

**Cách 2 — khai type hint, để injector tự resolve:**

```python
def __init__(self, auth_service: AuthService, task_service: TaskService, notification_service: NotificationService):
    self.auth_service = auth_service
    self.task_service = task_service
    self.notification_service = notification_service
```

Cả 2 cách cho ra cùng kết quả: sau `__init__`, mọi method trong class dùng lại qua `self.xxx`, không cần khởi tạo lại:

```python
async def create_task(self, request, payload: TaskCreateSchema):
    user_id, error = await self.auth_service.get_user_or_401(request)   # dùng lại, không tạo mới
    ...
    await self.task_service.create(user_id, payload)                    # dùng lại, không tạo mới
```

So sánh trực tiếp với Ninja thuần (không có class nào để đặt `__init__`):

| | Ninja thuần | ninja-extra |
|:---|:---|:---|
| Nơi khởi tạo service | Lặp lại trong từng function | 1 lần trong `__init__` của Controller (tự viết hoặc để injector tự resolve) |
| Nơi dùng service | Biến local trong function | `self.<service_name>` trong mọi method |
| Số lần gõ `AuthService()` cho 15 endpoint | 15 lần | 1 lần (hoặc 0 lần nếu dùng Cách 2) |

> Thực tế: `ArticleWriterController` trong `article_writer.py` (project `leadplusone_api`) dùng Cách 1 — `__init__` tự khởi tạo 5 service (`auth_service`, `persona_service`, `style_service`, `ai_service`, `thread_service`) dùng chung cho hơn 20 method. Cách 2 (khai type hint để injector tự resolve) chưa được dùng ở đâu trong repo — cả 2 cách đều đúng, đào sâu sự khác biệt và khi nào nên chọn cách nào ở bài 14.

---

## 5. Kết Luận

Cần chốt:

- `api_controller("/prefix", ...)` gắn prefix path dùng chung cho cả class — giống `router.register()` bên DRF.
- `ControllerBase` là class cha bắt buộc, cho ninja-extra biết đây là 1 nhóm endpoint có tổ chức.
- `__init__` là nơi khai dependency cho controller — có thể tự khởi tạo service (`self.x = X()`) hoặc khai type hint để framework tự resolve; cả 2 chạy qua cùng 1 cơ chế injector phía dưới. Đây là lý do chính chọn ninja-extra thay vì Ninja thuần khi có nhiều endpoint chung service.

Bài tiếp theo (`04-http-method-decorator-va-path-param.md`) đi vào chi tiết `@http_get`/`@http_post`/`@http_put`/`@http_patch`/`@http_delete` và cách khai path param như `{task_id}`.
