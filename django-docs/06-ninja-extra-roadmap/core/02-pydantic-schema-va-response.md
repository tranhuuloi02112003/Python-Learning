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

## 2. Ví Dụ Cụ Thể — Schema Cho 1 Endpoint Tạo Task

```python
class TaskCreateSchema(Schema):
    title: str
    priority: Optional[int] = None
```

Dùng trong method:

```python
@http_post("/create", response={201: Dict[str, Any], **COMMON_ERROR_RESPONSES})
async def create_task(self, request, payload: TaskCreateSchema):
    ...
```

Cách đọc dòng này:

```text
payload: TaskCreateSchema
    → Ninja nhận JSON body của request POST
    → tự ép JSON đó vào TaskCreateSchema
    → nếu field nào sai type/thiếu required field → tự trả lỗi 422, KHÔNG vào tới code bên trong method
    → nếu hợp lệ → payload là object đã validate, dùng thẳng payload.title, payload.priority
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
return 201, {"code": "success", "detail": "Task created successfully"}
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

## 4. Vì Sao `return 201, {...}` Hoạt Động Được — 3 Kiểu Return Của Ninja

Ninja quy định sẵn (nằm trong chính source code của thư viện, không phải project tự đặt ra): 1 method có thể `return` theo đúng 3 kiểu, Ninja tự nhận diện kiểu nào và xử lý tương ứng:

```text
1. return HttpResponse (object HttpResponse thật của Django)
   → Ninja trả nguyên như vậy, không đụng vào — giống hệt cách DRF trả Response()

2. return tuple 2 phần tử: (status_code, data)
   → Ninja hiểu vế đầu là status, vế sau là body cần serialize
   → cách ngắn gọn hay gặp: return 201, {"code": "success", ...}

3. return giá trị khác (dict, list, str...)
   → Ninja coi đó là body, tự lấy status mặc định (thường là status đầu tiên khai trong response={...})
```

So với DRF — DRF **chỉ có 1 cách**, bắt buộc phải bọc qua object `Response`:

```python
# DRF — luôn phải import Response, tạo instance
from rest_framework.response import Response
return Response({"code": "success", "detail": "..."}, status=201)
```

```python
# Ninja — 3 cách đều hợp lệ, thường chọn cách ngắn nhất (tuple)
return 201, {"code": "success", "detail": "..."}   # tuple — ngắn gọn nhất
return {"code": "success", "detail": "..."}         # raw dict — dùng status mặc định
```

Ninja tự lo phần "biến giá trị Python thường thành `HttpResponse` thật" ở tầng dưới (set `Content-Type: application/json`, tự `json.dumps`...) — đây là lý do bạn không cần import gì thêm khi viết `return 201, {...}` trong controller.

> Thực tế: trong project `leadplusone_api`, controller `article_writer.py` cũng dùng đúng kiểu `return (status, data)` này ở mọi endpoint — không có endpoint nào trả `HttpResponse` thô.

---

## 5. `Any` Khi Không Muốn Ràng Buộc Type Chặt

Với các endpoint mà response shape thay đổi tùy nhánh logic (VD: 1 hành động có thể trả về `{"thread_id":..., "titles":[...]}` hoặc trả thẳng 1 list, tùy tình huống), có thể khai response lỏng hơn bằng `Any`:

```python
FLEXIBLE_RESPONSE = {200: Any, 402: ErrorResponse, **COMMON_ERROR_RESPONSES}
```

`Any` nghĩa là Ninja **không validate/ép kiểu** dữ liệu trả về ở status 200 — trả gì cũng được, miễn là serialize JSON được.

> Thực tế: `article_writer.py` trong `leadplusone_api` dùng đúng pattern này (`AI_ACTION_RESPONSE = {200: Any, 402: ErrorResponse, ...}`) cho các endpoint gọi AI, vì response shape khác nhau giữa các hành động (gợi ý tiêu đề trả object, viết lại tiêu đề trả thẳng list).

---

## 6. Kết Luận

Cần chốt:

- `Schema` validate input bằng type hint, tự chạy trước khi vào function — khác DRF phải tự gọi `is_valid()`.
- `response={status: Type, ...}` khai trước shape output theo từng status code, ngay trên decorator.
- `return (status, data)` — Ninja tự đối chiếu với `response={...}` rồi serialize + set status. Đây là 1 trong 3 kiểu return Ninja hỗ trợ (mục 4) — DRF chỉ có 1 cách duy nhất (`Response(...)`).
- Dùng `Any` khi muốn nới lỏng, không ép kiểu output.

Bài tiếp theo (`03-ninja-extra-controller-va-di.md`) trả lời câu hỏi: nếu Ninja thuần là function độc lập, vậy `ninja-extra` giải quyết bài toán "nhiều endpoint dùng chung service" như thế nào.
