# Auto-CRUD — `ModelControllerBase`

> Tiếp theo `16-testing-voi-ninja-extra.md`. `article_writer.py` (ví dụ xuyên suốt bài 01-10) không dùng tính năng này — bài này giới thiệu nó như 1 chủ đề độc lập của framework, tương tự cách bài 11-16 giới thiệu các tính năng khác chưa xuất hiện trong file đó.

---

## 1. ninja-extra Có Auto-CRUD — `ModelControllerBase`

DRF, với `ModelViewSet` + `router.register()`, tự sinh 5 route chuẩn chỉ từ 1-2 dòng:

```python
router.register("tasks", TaskViewSet, basename="task")
# Tự sinh:
#   GET    /tasks/       -> list()
#   POST   /tasks/       -> create()
#   GET    /tasks/<pk>/  -> retrieve()
#   PUT    /tasks/<pk>/  -> update()
#   DELETE /tasks/<pk>/  -> destroy()
```

ninja-extra có tính năng tương đương: `ModelControllerBase` + `ModelConfig`, nằm ở `ninja_extra/controllers/model/`. Field thật của `ModelConfig` (đọc trực tiếp từ `schemas.py`):

```python
class ModelConfig(PydanticModel):
    model: Type[Model]                    # model Django thật, bắt buộc
    allowed_routes: List[str] = [         # bật/tắt từng route CRUD
        "create", "find_one", "update", "patch", "delete", "list"
    ]
    async_routes: bool = False            # bật thì sinh async handler
    create_schema / retrieve_schema / update_schema / patch_schema  # để trống thì tự sinh
    pagination: ModelPagination = ModelPagination()
    schema_config: ModelSchemaConfig      # include/exclude field, depth quan hệ...
```

Dùng thật (tái tạo đúng field trên, ví dụ minh họa với model `PersonaSetting` đã quen từ các bài trước):

```python
from ninja_extra import api_controller, ModelControllerBase
from ninja_extra.controllers.model import ModelConfig

@api_controller("/persona-model")
class PersonaModelController(ModelControllerBase):
    model_config = ModelConfig(
        model=PersonaSetting,
        allowed_routes=["list", "create", "find_one", "update", "delete"],
    )
```

Chỉ cần khai `model=...` là tự sinh đủ 5 route CRUD + tự sinh Pydantic schema từ field của model — đúng ý tưởng DRF `ModelViewSet` + `ModelSerializer`. Điều kiện: cần cài thêm package `ninja-schema` (source có check `if NinjaSchemaModelSchemaConfig is None: raise RuntimeError("ninja-schema package is required...")`).

---

## 2. Vì Sao `article_writer.py` Không Dùng Cách Này?

Dù có model rất hợp để auto-CRUD (`PersonaSetting`): các endpoint persona trong `article_writer.py` có business logic phụ (check `user_id` sở hữu, set default, giới hạn theo `feature=Feature.ARTICLE_WRITER`...) — auto-CRUD chỉ hợp cho CRUD thuần, không tự thêm được logic tùy biến. Đây cũng là lý do 20+ method trong file này vẫn viết tay `@http_get/post/put/patch/delete` từng dòng — không phải vì framework thiếu tính năng, mà vì bài toán thực tế cần nhiều hơn CRUD thuần:

```python
@api_controller("/tasks")
class TaskController(ControllerBase):
    @http_get("/list")
    async def list_tasks(self, request): ...

    @http_post("/create")
    async def create_task(self, request, payload: TaskCreateSchema): ...

    @http_get("/{task_id}/detail")
    async def task_detail(self, request, task_id: int): ...

    @http_put("/{task_id}/update")
    async def task_update(self, request, task_id: int, payload: TaskUpdateSchema): ...

    @http_delete("/{task_id}/delete")
    async def task_delete(self, request, task_id: int): ...
```

Path cũng được đặt tự do hơn khi viết tay, không bị ép theo convention REST cứng nhắc:

```python
@http_patch("/{task_id}/set-priority-high", ...)
```

Path dạng `/{id}/set-priority-high` không phải REST chuẩn (`PATCH /tasks/{id}/` với body `{"priority": "high"}` mới là REST chuẩn) — nhưng viết tay cho phép đặt path tùy ý theo hành động nghiệp vụ.

> Thực tế: `article_writer.py` trong project `leadplusone_api` có 20+ method, toàn bộ đều là `@http_get/post/put/patch/delete` viết tay — không dùng `ModelControllerBase` ở đâu cả (grep toàn repo cũng không thấy `ModelControllerBase`/`ModelConfig` được dùng ở bất kỳ feature app nào khác). Path dạng hành động nghiệp vụ như `/persona/{persona_id}/set-default` cũng xuất hiện thật trong file này.

---

## 3. Kết Luận — Chốt Toàn Bộ Roadmap

Cần chốt riêng bài này:

- ninja-extra **có** auto-CRUD qua `ModelControllerBase` + `ModelConfig` — tương đương DRF `ModelViewSet` + `ModelSerializer`, cần thêm package `ninja-schema`.
- `article_writer.py` không dùng vì các endpoint có business logic phụ (check quyền sở hữu, set default, giới hạn theo feature...), không phải CRUD thuần — auto-CRUD chỉ hợp khi bài toán đúng là CRUD thuần trên 1 model.

Chốt toàn bộ roadmap (17 bài):

- Bài 01-10: đủ để đọc hiểu `article_writer.py` — Schema, response protocol, `api_controller`/`ControllerBase`, http decorator, async/await, auth ở cấp API instance, và kiến trúc tách feature app.
- Bài 11-17: các chủ đề framework có nhưng `article_writer.py` không dùng tới — 1 số **đang dùng thật** ở feature app khác (`Query`, `Form`/`File`, exception handler riêng), 1 số **framework có nhưng repo chưa đụng tới cái nào** (`RouteContext`, settings, auto-DI qua `injector`, pagination/ordering/searching/throttling native, `TestClient`, `ModelControllerBase`).
- Điểm chung xuyên suốt cả 17 bài: ninja/ninja-extra luôn có 1 cách viết ngắn hơn DRF cho cùng bài toán (Schema thay Serializer, decorator route thay `urls.py`, `response={...}` thay `Response()`, auto-DI thay `__init__` tay, `ModelControllerBase` thay `ModelViewSet`...) — nhưng **không bắt buộc** phải dùng cách mới; project có quyền chọn cách quen thuộc (viết tay, tái dùng code cũ) miễn là chạy đúng, và `leadplusone_api` đang chọn vậy ở khá nhiều chỗ.
