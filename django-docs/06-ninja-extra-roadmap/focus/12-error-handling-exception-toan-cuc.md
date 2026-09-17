# Error Handling — Exception Handler Toàn Cục

> Tiếp theo `11-query-va-form-data.md`. `article_writer.py` xử lý lỗi bằng `try/except ValueError` rải rác trong từng method (đã thấy ở bài 05). Bài này giới thiệu 1 cách khác: đăng ký handler xử lý lỗi 1 lần, áp dụng cho toàn bộ API — cả 2 cách cùng tồn tại thật trong repo.

---

## 1. Ninja Core — `exception_handler` / `add_exception_handler`

Đã verify source `ninja/main.py`:

```python
# dòng ~498-502
def add_exception_handler(self, exc_class: Type[Exception], handler: Callable) -> None:
    self._exception_handlers[exc_class] = handler

# dòng ~504-511 — dạng decorator, gọi add_exception_handler bên trong
def exception_handler(self, exc_class: Type[Exception]):
    def decorator(func):
        self.add_exception_handler(exc_class, func)
        return func
    return decorator
```

Dùng:

```python
class MyBusinessError(Exception):
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

api = NinjaAPI()

@api.exception_handler(MyBusinessError)
def handle_business_error(request, exc: MyBusinessError):
    return api.create_response(
        request, {"code": exc.code, "detail": exc.detail}, status=400,
    )
```

Từ đây, **bất kỳ method nào** (ở bất kỳ controller nào đăng ký vào `api` này) chỉ cần `raise MyBusinessError(...)`, không cần tự viết `try/except` + `return 400, {...}` tại từng nơi — Ninja tự bắt exception này và gọi `handle_business_error`.

Cơ chế tìm handler đi theo MRO (`_lookup_exception_handler`, `ninja/main.py:544`) — nghĩa là đăng ký handler cho 1 class cha thì mọi class con cũng tự được bắt, không cần đăng ký riêng từng loại lỗi con.

Ninja cũng đã có sẵn vài handler mặc định (`ninja/errors.py`, tự đăng ký qua `set_default_exc_handlers`): `Http404` → 404, `HttpError` (base, có `.status_code` riêng) → đúng status đó, `ValidationError` (lỗi Schema) → 422, `Exception` (mọi lỗi khác) → 500.

---

## 2. ninja-extra — Sẵn 1 Hệ Thống Exception Kiểu DRF: `APIException`

`ninja_extra/exceptions.py` định nghĩa hẳn 1 hierarchy exception giống DRF, mỗi class có `status_code` + `default_detail` riêng:

```text
APIException (base, kế thừa HttpError)
├── ValidationError       (400)
├── ParseError            (400)
├── AuthenticationFailed  (401)
├── NotAuthenticated      (401)
├── PermissionDenied      (403)
├── NotFound              (404)
├── MethodNotAllowed      (405)
├── NotAcceptable         (406)
├── UnsupportedMediaType  (415)
└── Throttled             (429)
```

Và `NinjaExtraAPI.__init__` (`ninja_extra/main.py:~90`) **tự động** đăng ký sẵn 1 handler cho cả hierarchy này:

```python
self.exception_handler(exceptions.APIException)(self.api_exception_handler)
```

`api_exception_handler` tự lấy `exc.status_code` + `exc.detail` build response JSON `{"detail": ...}`, kèm cả header `Retry-After` nếu là `Throttled`. Nghĩa là: **chỉ cần** `raise NotFound("Persona not found")` ở bất kỳ đâu trong method, không cần `return 404, {...}` hay đăng ký gì thêm — `NinjaExtraAPI` đã tự lo sẵn.

```python
from ninja_extra.exceptions import NotFound

async def persona_update(self, request, persona_id: int, payload: PersonaSettingSchema):
    persona = await self.persona_service.get(user_id, persona_id)
    if not persona:
        raise NotFound("Persona not found")   # thay cho return 404, {...}
    ...
```

---

## 3. Đăng Ký Exception Riêng Của Project — Ví Dụ Thật

Ngoài hierarchy `APIException` có sẵn, project có thể tự viết exception riêng + tự đăng ký handler cho nó, giống ví dụ minh họa ở mục 1.

> Thực tế: `MPF_WEB_F94_AI_Tools/auth/exceptions.py` làm đúng cách này — tự định nghĩa `AIToolAPIError` (kế thừa `Exception` thuần, không phải `APIException`):
> ```python
> class AIToolAPIError(Exception):
>     def __init__(self, status_code, code, detail, field=None, suggestions=None, retriable=False):
>         ...
> ```
> rồi tự đăng ký handler, gọi ngay trong `urls.py` của feature này:
> ```python
> # exceptions.py
> def register_exception_handler(api) -> None:
>     @api.exception_handler(AIToolAPIError)
>     def _handle(request, exc: AIToolAPIError):
>         return api.create_response(request, exc.to_body(), status=exc.status_code)
>
> # urls.py
> api = NinjaExtraAPI(urls_namespace="ai_tools_v1", auth=AIToolAuth())
> register_exception_handler(api)
> ```

---

## 4. Vì Sao `article_writer.py` KHÔNG Dùng Cách Này?

`article_writer.py` xử lý lỗi kiểu thủ công, rải khắp method:

```python
try:
    ai_response, meta = await self._execute_ai(...)
except ValueError as e:
    if str(e) == "Persona not found":
        return 404, {"code": "not_found", "detail": "Persona not found"}
    raise
```

So sánh 2 cách cùng tồn tại trong repo:

| | Cách `article_writer.py` (try/except tại chỗ) | Cách exception handler toàn cục (`F94_AI_Tools`) |
|:---|:---|:---|
| Chỗ xử lý | Từng method tự viết `try/except` | 1 chỗ duy nhất (`register_exception_handler`), áp dụng mọi endpoint |
| Phân biệt loại lỗi | So sánh string `str(e) == "..."` — dễ gõ sai, không có gợi ý IDE | Class exception riêng (`NotFound`, `AIToolAPIError`...) — IDE gợi ý, khó gõ sai |
| Thêm 1 loại lỗi mới | Sửa từng nơi có liên quan | Thêm 1 class exception + raise, không cần sửa chỗ khác |
| Phù hợp khi | Ít loại lỗi, method ít, đọc code tại chỗ dễ hơn tra 2 file | Nhiều method dùng chung nhiều loại lỗi giống nhau |

Không có cách nào "đúng hơn" tuyệt đối — `article_writer.py` chọn cách tại chỗ vì mỗi hành động AI có message lỗi khá riêng biệt (`"Persona not found"`, `AI_RESPONSE_INVALID_ERROR`...), còn `F94_AI_Tools` chọn tập trung vì có nhiều loại lỗi tái sử dụng được ở nhiều endpoint auth khác nhau.

So với DRF: DRF có `EXCEPTION_HANDLER` khai trong `settings.py` (`REST_FRAMEWORK = {"EXCEPTION_HANDLER": "myapp.custom_handler"}`) — cũng là 1 chỗ xử lý toàn cục, nhưng khai qua Django settings, không phải gọi decorator trên instance API như Ninja.

---

## 5. Kết Luận

Cần chốt:

- `api.exception_handler(ExcClass)` / `add_exception_handler` đăng ký 1 handler xử lý toàn cục cho 1 loại exception (và mọi exception con của nó, theo MRO) — không cần `try/except` lặp lại ở từng method.
- `ninja-extra` có sẵn hierarchy `APIException` (giống DRF) + tự động wire handler cho hierarchy này ngay khi tạo `NinjaExtraAPI()` — chỉ cần `raise NotFound(...)` là đủ.
- Project có thể tự viết exception riêng + tự đăng ký handler riêng (ví dụ thật: `AIToolAPIError` ở `F94_AI_Tools`).
- `article_writer.py` không dùng cách này — chọn `try/except` tại chỗ, phù hợp với đặc thù lỗi khá riêng biệt của từng hành động AI. Cả 2 cách cùng hợp lệ, chọn theo bài toán.

Bài tiếp theo (`advanced/13-route-context-va-settings.md`) đi vào `self.context` (đối tượng `RouteContext` mọi controller đều có) và cách Django `settings.py` cấu hình ninja/ninja-extra ở cấp toàn cục.
