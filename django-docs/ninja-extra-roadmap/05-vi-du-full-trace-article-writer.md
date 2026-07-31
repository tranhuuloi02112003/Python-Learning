# Ví Dụ Thật — Trace Full 1 Endpoint Từ Request Tới Response

> Tiếp theo bài 01-04. Bài này ghép lại toàn bộ khái niệm đã học, trace 2 endpoint thật trong `article_writer.py`: 1 endpoint đơn giản, 1 endpoint phức tạp hơn (có AI + credit guard).

---

## 1. Endpoint Đơn Giản — `style_setting_create`

Code thật, dòng 62-68:

```python
@http_put("/user-style-setting/create", response={201: Dict[str, Any], **COMMON_ERROR_RESPONSES})
async def style_setting_create(self, request, payload: UserStyleSettingSchema):
    user_id, error = await self.auth_service.get_user_or_401(request)
    if error:
        return error
    await self.style_service.upsert(user_id, payload)
    return 201, {"code": "success", "detail": "Style setting created successfully"}
```

Trace từng bước với request thật:

```text
PUT /article-writer/user-style-setting/create
Header: Authorization: Bearer <token>
Body:   {"style_guideline": "...", "length_instruction": "...", "content_constraints": "..."}
```

```text
Bước 1 — Routing
    api_controller("/article-writer") (bài 03) + http_put("/user-style-setting/create") (bài 04)
    → ghép URL: /article-writer/user-style-setting/create
    → Ninja biết method nào xử lý request này: style_setting_create

Bước 2 — Khởi tạo Controller
    ArticleWriterController.__init__() chạy (bài 03)
    → self.auth_service, self.style_service... đã sẵn sàng

Bước 3 — Validate input
    payload: UserStyleSettingSchema (bài 02)
    → Ninja parse JSON body, ép vào UserStyleSettingSchema
    → nếu thiếu field bắt buộc → trả 422 ngay, KHÔNG chạy tới bước 4

Bước 4 — Business logic (code bạn tự viết)
    user_id, error = await self.auth_service.get_user_or_401(request)
        → đọc token trong header, tự resolve ra user_id
        → nếu token sai/thiếu → error khác None
    if error: return error
        → return sớm, dùng nguyên response error đã build sẵn trong auth_service
    await self.style_service.upsert(user_id, payload)
        → lưu/update style setting vào DB, dùng self.style_service đã khởi tạo ở __init__

Bước 5 — Response
    return 201, {"code": "success", "detail": "..."}
    → Ninja đối chiếu status 201 có trong response={201: Dict[str, Any], ...} (bài 02)
    → serialize dict thành JSON, set HTTP status = 201
```

Response thật trả về:

```json
HTTP/1.1 201 Created
{
    "code": "success",
    "detail": "Style setting created successfully"
}
```

---

## 2. Endpoint Phức Tạp Hơn — `suggest_titles`

Code thật, dòng 187-228 (rút gọn phần import):

```python
@http_post("/suggest-titles", response=AI_ACTION_RESPONSE)
async def suggest_titles(self, request, payload: SuggestTitlesSchema):
    user_id, error = await self.auth_service.get_user_or_401(request)
    if error:
        return error

    guard = AiCreditGuard(request.user)
    organization_id, error = await sync_to_async(guard.pre_check)()
    if error:
        return error

    try:
        ai_response, meta = await self._execute_ai(
            user_id, payload,
            action="suggest_titles",
            default_prompt=SUGGEST_TITLES,
            method_name="suggest_titles",
        )
    except ValueError as e:
        if str(e) == "Persona not found":
            return 404, {"code": "not_found", "detail": "Persona not found"}
        raise
    await sync_to_async(guard.charge)(organization_id, meta)
    if not ai_response:
        return AI_RESPONSE_INVALID_ERROR

    list_titles = [
        {"idx": idx + 1, "title": title, "is_selected": False}
        for idx, title in enumerate(ai_response)
    ]
    thread = await self.thread_service.create_thread(
        user_id=user_id, title=payload.keyword, titles=list_titles,
        persona_id=payload.persona_id, keyword=payload.keyword,
        message=payload.message, goal=payload.goal, experience=payload.experience,
    )
    return {"thread_id": thread.id, "titles": list_titles}
```

Endpoint này phức tạp hơn vì có thêm 2 việc **không thuộc khái niệm Ninja/ninja-extra**, mà là logic nghiệp vụ của dự án — cần phân biệt rõ để không nhầm là "cú pháp Ninja":

```text
1. AiCreditGuard  → kiểm tra + trừ credit trước/sau khi gọi AI (nghiệp vụ billing)
2. self._execute_ai(...) → helper nội bộ gọi AI thật, raise ValueError nếu persona không tồn tại
```

Trace phần **thuộc về Ninja/ninja-extra** (những gì đã học ở bài 01-04):

```text
Routing:      @http_post("/suggest-titles") + prefix "/article-writer" → POST /article-writer/suggest-titles
Validate:     payload: SuggestTitlesSchema → Ninja tự parse + validate JSON body
Service DI:   self.auth_service, self.thread_service → dùng lại từ __init__, không tạo mới
Response:     response=AI_ACTION_RESPONSE = {200: Any, 402: ErrorResponse, **COMMON_ERROR_RESPONSES}
    → return {"thread_id":..., "titles":...} khớp status 200, type Any (không ép kiểu chặt)
    → return 404, {...} khớp COMMON_ERROR_RESPONSES
```

Trace phần **thuộc về nghiệp vụ dự án** (không phải Ninja):

```text
guard.pre_check()  → check credit đủ không, trả lỗi 402 nếu thiếu (định nghĩa trong AI_ACTION_RESPONSE)
self._execute_ai() → build prompt, gọi AI service, raise ValueError nếu thiếu persona
guard.charge()     → trừ credit sau khi AI chạy xong (thành công hay lỗi parse vẫn trừ, vì AI đã chạy)
```

---

## 3. Vì Sao Phải Tách 2 Phần Này Rõ Ràng?

```text
Nếu đọc code mà không tách được "cái gì là Ninja/ninja-extra" và "cái gì là business logic":
    → dễ nhầm AiCreditGuard là 1 phần của framework (không phải)
    → dễ bỏ sót rằng return 404 ở giữa hàm vẫn hợp lệ, miễn khớp response={...} đã khai
```

Quy tắc đọc 1 endpoint ninja-extra bất kỳ:

```text
1. Đọc decorator (@http_xxx + response=...) → biết path, method, và các status/type được phép trả
2. Đọc tham số function → biết path param nào, payload Schema nào
3. Đọc thân hàm → phân biệt dòng nào gọi self.<service> (đã có sẵn từ __init__)
                  và dòng nào là logic nghiệp vụ thuần (guard, try/except...)
4. Đối chiếu từng return với response={...} đã khai ở bước 1
```

---

## 4. Kết Luận

Cần chốt:

- Một request đi qua đúng thứ tự: routing (`api_controller` + `http_xxx`) → khởi tạo Controller (`__init__`) → validate input (`Schema`) → business logic (`self.<service>`) → response (đối chiếu `response={...}`).
- `AiCreditGuard`, `_execute_ai`, thread management... là logic nghiệp vụ riêng của dự án, không phải cú pháp Ninja/ninja-extra — cần phân biệt để không học nhầm.
- Đọc 1 endpoint ninja-extra bất kỳ theo 4 bước ở mục 3 sẽ áp dụng được cho toàn bộ file, không chỉ 2 ví dụ ở đây.

Bài cuối cùng (`06-so-sanh-drf-vs-ninja-vs-ninja-extra.md`) đặt 3 kiểu viết API (DRF, Ninja thuần, ninja-extra) cạnh nhau để so sánh trực tiếp — giờ bạn đã có đủ nền tảng Ninja/ninja-extra để đọc bài đó dễ hơn.
