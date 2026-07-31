# So Sánh 3 Kiểu Viết API: DRF vs Django Ninja vs ninja-extra

> Note: Bài cuối cùng của folder `ninja-extra-roadmap/`. Không dạy lại DRF (đã học ở `drf-roadmap/`), và không dạy lại khái niệm Ninja/ninja-extra (đã học ở bài 01-05 trong folder này). Mục tiêu ở đây là đặt 3 kiểu viết API vào cùng một sơ đồ request → response, để thấy rõ chúng khác nhau ở đâu và giống nhau ở đâu.

Ví dụ thật dùng trong bài: `MPF_WEB_F26_My_Page/controllers/article_writer.py` (dự án `leadplusone_api`, viết bằng `ninja-extra`).

---

## 1. Cái Giống Nhau Trước — IN/OUT Không Đổi

Dù viết bằng DRF, Ninja thuần, hay ninja-extra, request/response vẫn là một khối:

```text
IN chung:  HTTP request  — path, JSON body, header (token auth)
OUT chung: HTTP response — status code + JSON body
```

Khác biệt chỉ nằm ở **ai lo phần validate input / serialize output / khai báo route ở giữa**. Ba bài dưới đây so từng khâu đó.

---

## 2. Flow — DRF (đã biết)

```text
Request → urls.py → APIView.post() → Serializer.is_valid() → business logic → Response(data)
```

| Thành phần | Vai trò |
|:---|:---|
| `urls.py` | Khai `path("...", MyView.as_view())` — route tách biệt hoàn toàn khỏi code xử lý |
| `Serializer` | Class riêng, tự viết field (`CharField`, `IntegerField`...) để validate + serialize |
| `APIView`/`ViewSet` | Class chứa method `get`/`post`... nhận `request.data` thô, tự parse |

---

## 3. Flow — Django Ninja "Thuần" (Function-Based)

```text
Request → router.post("/path")(function) → Ninja tự parse JSON → ép vào Pydantic Schema
        → function(request, payload: Schema) → return dict/object → Ninja tự serialize theo response={...}
```

| Thành phần | Vai trò |
|:---|:---|
| Router | Giống `urls.py` nhưng khai route ngay tại chỗ định nghĩa function, không tách file riêng |
| Pydantic Schema | Thay cho Serializer — viết class kế thừa `Schema` với type hint (`str`, `int`, `Optional[str]`...), Ninja tự validate + tự sinh OpenAPI docs từ đó |
| Function | Không có class — mỗi endpoint là 1 function độc lập |

---

## 4. Flow — ninja-extra (Kiểu Trong `article_writer.py`)

```text
Request → @api_controller định prefix path → class Controller(ControllerBase)
        → @http_get/@http_post trên method → Pydantic Schema validate payload
        → self.<service>.xxx() → return → Ninja tự serialize theo response={...}
```

Đối chiếu với file thật `MPF_WEB_F26_My_Page/controllers/article_writer.py`:

| Tên | Vai trò 1 câu |
|:---|:---|
| `api_controller("/article-writer", ...)` (dòng 48) | Decorator gắn prefix path `/article-writer` cho cả class, giống `router.register()` bên DRF |
| `ControllerBase` (dòng 49) | Class cha bắt buộc, cung cấp context (`self.context.request`...) cho controller |
| `__init__` (dòng 51-56) | Khởi tạo các service dùng trong controller (`auth_service`, `persona_service`, `style_service`, `ai_service`, `thread_service`) — tương đương DI thủ công |
| `@http_put`/`@http_get`/`@http_post`/`@http_patch`/`@http_delete` | Decorator trên method, khai path + `response={status: Type}` — route nằm ngay tại method, không tách file |
| `UserStyleSettingSchema` (import dòng 10) | Pydantic Schema — thay cho Serializer, dùng type hint để validate payload |

Ví dụ một endpoint cụ thể trong file (dòng 62-68):

```python
@http_put("/user-style-setting/create", response={201: Dict[str, Any], **COMMON_ERROR_RESPONSES})
async def style_setting_create(self, request, payload: UserStyleSettingSchema):
    user_id, error = await self.auth_service.get_user_or_401(request)
    if error:
        return error
    await self.style_service.upsert(user_id, payload)
    return 201, {"code": "success", "detail": "Style setting created successfully"}
```

Trace theo sơ đồ flow ở trên:

```text
PUT /article-writer/user-style-setting/create
    → api_controller prefix "/article-writer" ghép với path method "/user-style-setting/create"
    → Ninja parse JSON body, validate bằng UserStyleSettingSchema → payload
    → method chạy: self.auth_service, self.style_service (khởi tạo sẵn ở __init__)
    → return (201, {...}) → Ninja serialize theo response={201: Dict[str, Any], ...}
```

---

## 5. Vì Sao Có 2 Kiểu Ninja (Thuần vs ninja-extra)?

```text
Ninja thuần  = function-based, đơn giản, nhẹ.
ninja-extra  = thêm lớp "class-based controller" lên trên,
               cho code có tổ chức giống DRF ViewSet.
```

`ninja-extra` cho phép nhóm nhiều endpoint liên quan vào 1 class, share `__init__`, share service instances. Đó là lý do `article_writer.py` chọn `ninja-extra`: controller này cần nhiều endpoint liên quan (style-setting, persona, titles, structure, content, thread...) dùng chung 5 service (`auth_service`, `persona_service`, `style_service`, `ai_service`, `thread_service`). Nếu viết function-based thuần thì phải khởi tạo lại 5 service đó ở mỗi function.

---

## 6. Bảng So Sánh Nhanh

| | DRF | Ninja thuần | ninja-extra |
|:---|:---|:---|:---|
| Route khai ở đâu | `urls.py` riêng | Ngay tại `router.post(...)` | Ngay tại `@http_get/@http_post` trên method |
| Validate input | `Serializer` (tự viết field) | Pydantic `Schema` (type hint) | Pydantic `Schema` (type hint) |
| Serialize output | `Response(serializer.data)` | Tự sinh theo `response={...}` | Tự sinh theo `response={...}` |
| Đơn vị tổ chức code | Class (`APIView`/`ViewSet`) | Function độc lập | Class (`ControllerBase`) |
| Share state/service giữa nhiều endpoint | Qua `self` trong ViewSet | Không có sẵn — tự truyền tay | Qua `__init__` của Controller |
| OpenAPI docs | Cần cấu hình thêm (`drf-yasg`/`drf-spectacular`) | Tự sinh từ Schema | Tự sinh từ Schema |

---

## 7. Kết Luận

Cần chốt:

- IN/OUT của cả 3 kiểu giống nhau: HTTP request vào, HTTP response (status + JSON) ra.
- Khác biệt nằm ở giữa: DRF dùng `Serializer` + route tách trong `urls.py`; Ninja thuần dùng Pydantic `Schema` + route khai tại chỗ, function độc lập; ninja-extra thêm `ControllerBase` để gom nhiều endpoint liên quan vào 1 class, share service qua `__init__`.
- Chọn `ninja-extra` khi có nhiều endpoint cùng domain cần dùng chung nhiều service (như `article_writer.py` dùng chung 5 service cho 15+ endpoint) — tránh phải khởi tạo lặp lại service ở từng function.
