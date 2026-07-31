# Pydantic Schema — Validate Input & Serialize Output

> Tiếp theo `01-tong-quan-django-ninja.md`. Bài này đi sâu vào 2 việc: Schema validate input, và `response={...}` serialize output.

---

## 1. Pydantic Schema Là Gì?

`Schema` là class Ninja dùng để validate input, thay cho `Serializer` bên DRF. Điểm khác biệt: bạn viết **type hint** thay vì viết field object.

```python
# DRF Serializer (đã biết)
class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    priority = serializers.IntegerField(required=False)

# Ninja Schema (mới)
class TaskSchema(Schema):
    title: str
    priority: Optional[int] = None
```

| DRF Serializer | Ninja Schema |
|:---|:---|
| `serializers.CharField(max_length=200)` | `title: str` |
| `serializers.IntegerField(required=False)` | `priority: Optional[int] = None` |
| `serializer.is_valid()` gọi thủ công trong view | Ninja tự validate trước khi vào function, lỗi tự trả `422` |
| Viết `Meta.fields` nếu là `ModelSerializer` | Không cần — field là thuộc tính class, gõ thẳng |

---

## 2. Ví Dụ Thật — `UserStyleSettingSchema`

Trong `article_writer.py`, endpoint tạo style setting dùng schema import sẵn:

```python
from MPF_WEB_F26_My_Page.schemas import (
    PersonaSettingSchema,
    UserStyleSettingSchema,
    ...
)
```

Và dùng trong method:

```python
@http_put("/user-style-setting/create", response={201: Dict[str, Any], **COMMON_ERROR_RESPONSES})
async def style_setting_create(self, request, payload: UserStyleSettingSchema):
    ...
```

Cách đọc dòng này:

```text
payload: UserStyleSettingSchema
    → Ninja nhận JSON body của request PUT
    → tự ép JSON đó vào UserStyleSettingSchema
    → nếu field nào sai type/thiếu required field → tự trả lỗi 422, KHÔNG vào tới code bên trong method
    → nếu hợp lệ → payload là object đã validate, dùng thẳng payload.<field_name>
```

Đây là điểm khác lớn nhất so với DRF: DRF cần bạn tự gọi `serializer.is_valid()` rồi tự check, Ninja làm việc này **trước khi function chạy**.

---

## 3. `response={...}` — Serialize Output Theo Status Code

Ninja không dùng `Response(data, status=200)` như DRF. Thay vào đó, bạn khai trước **map status code → type** ngay trên decorator:

```python
@http_put("/user-style-setting/create", response={201: Dict[str, Any], **COMMON_ERROR_RESPONSES})
```

Đọc `response={201: Dict[str, Any], **COMMON_ERROR_RESPONSES}`:

```text
201  → nếu method return status 201, data phải khớp shape Dict[str, Any]
COMMON_ERROR_RESPONSES → dict có sẵn, khai các status lỗi dùng chung (400, 401, 404...)
```

Trong method, bạn chỉ cần `return` tuple `(status, data)` hoặc `return data` (mặc định lấy status đầu tiên khai trong `response`):

```python
return 201, {"code": "success", "detail": "Style setting created successfully"}
```

Ninja tự làm phần còn lại:

```text
- Đối chiếu 201 có trong response={...} không
- Serialize {"code": ..., "detail": ...} thành JSON
- Set HTTP status = 201
```

So với DRF:

```python
# DRF — bạn tự gọi Response() với status
return Response({"code": "success", "detail": "..."}, status=201)

# Ninja — bạn return tuple, response={...} đã khai type từ decorator
return 201, {"code": "success", "detail": "..."}
```

---

## 4. `Any` Khi Không Muốn Ràng Buộc Type Chặt

Nhiều endpoint AI trong `article_writer.py` dùng response lỏng hơn:

```python
AI_ACTION_RESPONSE = {200: Any, 402: ErrorResponse, **COMMON_ERROR_RESPONSES}
```

`Any` nghĩa là Ninja **không validate/ép kiểu** dữ liệu trả về ở status 200 — trả gì cũng được, miễn là serialize JSON được. Đây là cách nới lỏng khi response shape thay đổi tùy nhánh logic (VD: `suggest_titles` trả `{"thread_id":..., "titles":...}`, còn `rewrite_title` trả thẳng `ai_response` là list).

---

## 5. Kết Luận

Cần chốt:

- `Schema` validate input bằng type hint, tự chạy trước khi vào function — khác DRF phải tự gọi `is_valid()`.
- `response={status: Type, ...}` khai trước shape output theo từng status code, ngay trên decorator.
- `return (status, data)` — Ninja tự đối chiếu với `response={...}` rồi serialize + set status.
- Dùng `Any` khi muốn nới lỏng, không ép kiểu output.

Bài tiếp theo (`03-ninja-extra-controller-va-di.md`) trả lời câu hỏi: nếu Ninja thuần là function độc lập, vậy `ninja-extra` giải quyết bài toán "nhiều endpoint dùng chung service" như thế nào.
