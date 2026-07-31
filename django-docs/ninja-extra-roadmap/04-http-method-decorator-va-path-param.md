# `@http_get`/`@http_post`/... và Path Param

> Tiếp theo `03-ninja-extra-controller-va-di.md`. Bài này đi vào chi tiết decorator method và cách khai path param như `{persona_id}`.

---

## 1. Import Các Decorator

Dòng 4 trong `article_writer.py`:

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

Ví dụ đơn giản nhất, dòng 70:

```python
@http_get("/user-style-setting/detail", response={200: Dict[str, Any], **COMMON_ERROR_RESPONSES})
async def style_setting_detail(self, request):
    ...
```

Ghép với prefix `/article-writer` từ `api_controller` (bài 03), URL đầy đủ là:

```text
GET /article-writer/user-style-setting/detail
```

---

## 3. Path Có Param — `{persona_id}`

Dòng 96-97:

```python
@http_put("/persona/{persona_id}/update", response={200: Dict[str, Any], **COMMON_ERROR_RESPONSES})
async def persona_update(self, request, persona_id: int, payload: PersonaSettingSchema):
    ...
```

Đọc cú pháp này:

```text
"/persona/{persona_id}/update"
    → {persona_id} trong path string là chỗ Ninja lấy giá trị từ URL

def persona_update(self, request, persona_id: int, payload: ...):
    → persona_id: int  → tên PHẢI KHỚP với tên trong {persona_id}
    → Ninja tự lấy giá trị từ URL, tự ép sang int
    → nếu URL truyền persona_id không phải số → Ninja tự trả lỗi 422, không vào tới code bên trong
```

Ví dụ request thật:

```text
PUT /article-writer/persona/7/update
    → persona_id = 7 (đã ép kiểu int)
    → payload lấy từ JSON body, validate theo PersonaSettingSchema
```

So với DRF, `path("persona/<int:persona_id>/update", ...)` trong `urls.py` + `def update(self, request, persona_id):` trong view — Ninja gộp 2 bước "khai path param" và "nhận giá trị trong function signature" làm một, không tách file `urls.py`.

---

## 4. Nhiều Path Param Trong 1 Endpoint

`article_writer.py` không có ví dụ 2 path param, nhưng cú pháp mở rộng tự nhiên:

```python
@http_get("/persona/{persona_id}/note/{note_id}")
async def note_detail(self, request, persona_id: int, note_id: int):
    ...
```

Quy tắc không đổi: mỗi `{tên}` trong path string cần có 1 tham số cùng tên trong function signature.

---

## 5. Thứ Tự Tham Số Trong Function Signature

Nhìn lại `persona_update`:

```python
async def persona_update(self, request, persona_id: int, payload: PersonaSettingSchema):
```

Thứ tự cố định:

```text
1. self       — vì đây là method trong class (ControllerBase)
2. request    — luôn có, giống DRF
3. path param — theo đúng thứ tự xuất hiện trong path string
4. payload    — Schema lấy từ JSON body (nếu có), luôn để cuối
```

---

## 6. Kết Luận

Cần chốt:

- `@http_get`/`@http_post`/`@http_put`/`@http_patch`/`@http_delete` — mỗi decorator ứng với 1 HTTP method, đặt ngay trên method trong Controller.
- Path param dùng cú pháp `{ten_param}` trong path string, và cần 1 tham số cùng tên, có type hint, trong function signature — Ninja tự lấy giá trị từ URL và ép kiểu.
- Thứ tự tham số cố định: `self`, `request`, các path param theo đúng thứ tự trong path, rồi mới tới `payload`.

Bài tiếp theo (`05-vi-du-full-trace-article-writer.md`) trace toàn bộ 1 endpoint thật từ request tới response, ghép lại tất cả khái niệm đã học ở bài 01-04.
