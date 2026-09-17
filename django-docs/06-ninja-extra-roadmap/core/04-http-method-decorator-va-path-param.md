# `@http_get`/`@http_post`/... và Path Param

> Tiếp theo `03-ninja-extra-controller-va-di.md`. Bài này đi vào chi tiết decorator method và cách khai path param như `{task_id}`.

---

## 1. Import Các Decorator

```python
from ninja_extra import api_controller, http_get, http_post, http_put, http_patch, http_delete, ControllerBase
```

Mỗi decorator ứng với 1 HTTP method — tư duy giống hệt DRF, chỉ khác tên gọi:

| HTTP Method | ninja-extra decorator | DRF (đã biết) |
|:---|:---|:---|
| GET | `@http_get(...)` | `def get(self, request):` trong `APIView` |
| POST | `@http_post(...)` | `def post(self, request):` |
| PUT | `@http_put(...)` | `def put(self, request):` |
| PATCH | `@http_patch(...)` | `def partial_update(self, request):` |
| DELETE | `@http_delete(...)` | `def destroy(self, request):` |

---

## 2. Path Không Có Param

Ví dụ đơn giản nhất:

```python
@http_get("/list", response={200: List[Dict[str, Any]], **COMMON_ERROR_RESPONSES})
async def list_tasks(self, request):
    ...
```

Ghép với prefix `/tasks` từ `api_controller` (bài 03), URL đầy đủ là:

```text
GET /tasks/list
```

---

## 3. Path Có Param — `{task_id}`

```python
@http_put("/{task_id}/update", response={200: Dict[str, Any], **COMMON_ERROR_RESPONSES})
async def task_update(self, request, task_id: int, payload: TaskUpdateSchema):
    ...
```

Đọc cú pháp này:

```text
"/{task_id}/update"
    → {task_id} trong path string là chỗ Ninja lấy giá trị từ URL

def task_update(self, request, task_id: int, payload: ...):
    → task_id: int  → tên PHẢI KHỚP với tên trong {task_id}
    → Ninja tự lấy giá trị từ URL, tự ép sang int
    → nếu URL truyền task_id không phải số → Ninja tự trả lỗi 422, không vào tới code bên trong
```

Ví dụ request thật:

```text
PUT /tasks/7/update
    → task_id = 7 (đã ép kiểu int)
    → payload lấy từ JSON body, validate theo TaskUpdateSchema
```

So với DRF, `path("tasks/<int:task_id>/update", ...)` trong `urls.py` + `def update(self, request, task_id):` trong view — Ninja gộp 2 bước "khai path param" và "nhận giá trị trong function signature" làm một, không tách file `urls.py`.

> Thực tế: `article_writer.py` trong `leadplusone_api` dùng đúng cú pháp này ở nhiều endpoint, VD `@http_put("/persona/{persona_id}/update", ...)` với `persona_id: int` trong signature.

---

## 4. Nhiều Path Param Trong 1 Endpoint

Cú pháp mở rộng tự nhiên khi cần 2 path param:

```python
@http_get("/{task_id}/comment/{comment_id}")
async def comment_detail(self, request, task_id: int, comment_id: int):
    ...
```

Quy tắc không đổi: mỗi `{tên}` trong path string cần có 1 tham số cùng tên trong function signature.

---

## 5. Vị Trí Tham Số Trong Signature — KHÔNG Quan Trọng

Nhìn lại `task_update`:

```python
async def task_update(self, request, task_id: int, payload: TaskUpdateSchema):
```

Cách viết trên đọc dễ hiểu, nhưng **đây chỉ là quy ước đọc cho dễ, không phải yêu cầu bắt buộc của framework**. Đã verify bằng thực nghiệm (cài `django-ninja` thật, gọi qua `TestClient`, không chỉ đọc docs): đảo thứ tự tham số vẫn chạy đúng y hệt.

```python
# Đảo path param ra sau payload — vẫn chạy đúng, kết quả giống hệt
async def task_update(self, request, payload: TaskUpdateSchema, task_id: int):
```

```text
Test thật: PUT /tasks/{task_id}/comment/{comment_id}
def comment_detail(self, request, comment_id: int, task_id: int):  ← khai comment_id TRƯỚC task_id
                                                                       dù trong path task_id đứng trước
GET /tasks/111/comment/222 → vẫn ra đúng {"task_id": 111, "comment_id": 222}
```

Lý do: Ninja xét **từng tham số độc lập**, không quan tâm nó đứng thứ mấy trong signature:

```text
Với MỖI tham số (bất kể đứng thứ mấy):
  1. Tên có khớp {tên} nào trong path string không?  → khớp: Path param, dừng ở đây
  2. Không khớp → xem type: là Schema (BaseModel)?     → Body
  3. Không khớp path, không phải Schema (là scalar)?   → Query
```

Chỉ có 1 ràng buộc thật (đến từ Python, không phải Ninja): `self` phải là tham số đầu tiên vì đây là bound method của class. `request` theo quy ước luôn đứng ngay sau `self` — đây là style phổ biến để code dễ đọc, không phải điều framework kiểm tra vị trí.

---

## 6. Kết Luận

Cần chốt:

- `@http_get`/`@http_post`/`@http_put`/`@http_patch`/`@http_delete` — mỗi decorator ứng với 1 HTTP method, đặt ngay trên method trong Controller.
- Path param dùng cú pháp `{ten_param}` trong path string, và cần 1 tham số cùng tên, có type hint, trong function signature — Ninja tự lấy giá trị từ URL và ép kiểu.
- Vị trí tham số trong signature **không quan trọng** (đã verify bằng thực nghiệm) — Ninja xét từng tham số độc lập: tên khớp path → Path param; không khớp và là Schema → Body; không khớp và là scalar → Query. `self` phải đứng đầu (ràng buộc của Python, không phải Ninja); thứ tự còn lại chỉ là quy ước đọc cho dễ.

Bài tiếp theo (`05-vi-du-full-trace.md`) trace toàn bộ 1 endpoint từ request tới response, ghép lại tất cả khái niệm đã học ở bài 01-04.
