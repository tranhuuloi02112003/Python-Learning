# ninja-extra: `api_controller` + `ControllerBase` + Dependency Injection

> Tiếp theo `02-pydantic-schema-va-response.md`. Bài này trả lời: Ninja thuần là function độc lập, vậy khi nhiều endpoint cần dùng chung service thì sao?

---

## 1. Vấn Đề Cần Giải Quyết

Ở bài 01, mỗi endpoint Ninja thuần là 1 function riêng. Nếu 15 endpoint đều cần gọi `AuthService`, `StyleService`... thì Ninja thuần buộc bạn khởi tạo lại service đó **trong từng function**:

```python
# Ninja thuần — lặp lại ở mọi function
@router.post("/suggest-titles")
def suggest_titles(request, payload: SuggestTitlesSchema):
    auth_service = AuthService()          # lặp lại
    persona_service = PersonaService()    # lặp lại
    ...

@router.post("/rewrite-title")
def rewrite_title(request, payload: RewriteTitleSchema):
    auth_service = AuthService()          # lặp lại
    persona_service = PersonaService()    # lặp lại
    ...
```

`ninja-extra` giải quyết việc này bằng cách thêm **class** vào giữa router và function — giống ý tưởng DRF `ViewSet` gom nhiều action vào 1 class.

---

## 2. `api_controller` — Gắn Prefix Path Cho Cả Class

Trong `article_writer.py`, dòng 48:

```python
@api_controller("/article-writer", tags=["My Page"])
class ArticleWriterController(ControllerBase):
```

Đọc dòng này:

```text
@api_controller("/article-writer", ...)
    → mọi method http_get/http_post... bên trong class này
      đều có URL bắt đầu bằng "/article-writer"
tags=["My Page"]
    → chỉ để nhóm hiển thị trong OpenAPI/Swagger docs, không ảnh hưởng logic
```

So với DRF:

```text
@api_controller("/article-writer")   ≈  router.register("article-writer", ArticleWriterViewSet)
```

Cả hai đều là "khai 1 prefix path dùng chung cho nhiều endpoint của cùng 1 resource".

---

## 3. `ControllerBase` — Class Cha Bắt Buộc

```python
class ArticleWriterController(ControllerBase):
```

`ControllerBase` là class cha **bắt buộc** phải kế thừa để `@api_controller` hoạt động đúng. Nó cung cấp:

- `self.context` — nơi chứa `request` hiện tại và metadata khác của ninja-extra.
- Cơ chế để `@http_get`/`@http_post`... nhận diện method nào thuộc controller nào.

Tư duy đơn giản: `ControllerBase` với ninja-extra ≈ `ViewSet`/`APIView` với DRF — class nền để framework biết "đây là 1 nhóm endpoint có tổ chức", không phải function rời rạc.

---

## 4. `__init__` — Dependency Injection Thủ Công

Dòng 51-56 trong `article_writer.py`:

```python
def __init__(self):
    self.auth_service = AuthService()
    self.persona_service = PersonaService(feature=Feature.ARTICLE_WRITER)
    self.style_service = StyleService(feature=Feature.ARTICLE_WRITER)
    self.ai_service = ArticleWriterAIService()
    self.thread_service = ArticleWriterThreadService()
```

Đây là "Dependency Injection thủ công": mỗi khi Ninja tạo instance `ArticleWriterController` để xử lý 1 request, `__init__` chạy 1 lần, khởi tạo sẵn 5 service. Sau đó **mọi method trong class** dùng lại qua `self.xxx`, không cần khởi tạo lại:

```python
async def style_setting_create(self, request, payload: UserStyleSettingSchema):
    user_id, error = await self.auth_service.get_user_or_401(request)   # dùng lại, không tạo mới
    ...
    await self.style_service.upsert(user_id, payload)                   # dùng lại, không tạo mới
```

So sánh trực tiếp:

| | Ninja thuần | ninja-extra |
|:---|:---|:---|
| Nơi khởi tạo service | Lặp lại trong từng function | 1 lần trong `__init__` của Controller |
| Nơi dùng service | Biến local trong function | `self.<service_name>` trong mọi method |
| Số lần gõ `AuthService()` cho 15 endpoint | 15 lần | 1 lần |

---

## 5. Kết Luận

Cần chốt:

- `api_controller("/prefix", ...)` gắn prefix path dùng chung cho cả class — giống `router.register()` bên DRF.
- `ControllerBase` là class cha bắt buộc, cho ninja-extra biết đây là 1 nhóm endpoint có tổ chức.
- `__init__` là nơi khởi tạo service 1 lần duy nhất; các method dùng lại qua `self.xxx` — đây là lý do chính chọn ninja-extra thay vì Ninja thuần khi có nhiều endpoint chung service.

Bài tiếp theo (`04-http-method-decorator-va-path-param.md`) đi vào chi tiết `@http_get`/`@http_post`/`@http_put`/`@http_patch`/`@http_delete` và cách khai path param như `{persona_id}`.
