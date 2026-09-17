# Ví Dụ — Trace Full 1 Endpoint Từ Request Tới Response

> Tiếp theo bài 01-04. Bài này ghép lại toàn bộ khái niệm đã học, trace 2 endpoint minh họa trong 1 `TaskController` tự tạo: 1 endpoint đơn giản, 1 endpoint phức tạp hơn (có gọi service ngoài + guard kiểm tra hạn mức).

---

## 1. Endpoint Đơn Giản — `create_task`

```python
@http_post("/create", response={201: Dict[str, Any], **COMMON_ERROR_RESPONSES})
async def create_task(self, request, payload: TaskCreateSchema):
    user_id, error = await self.auth_service.get_user_or_401(request)
    if error:
        return error
    await self.task_service.create(user_id, payload)
    return 201, {"code": "success", "detail": "Task created successfully"}
```

Trace từng bước với request thật:

```text
POST /tasks/create
Header: Authorization: Bearer <token>
Body:   {"title": "Write report", "priority": 1}
```

```text
Bước 1 — Routing
    api_controller("/tasks") (bài 03) + http_post("/create") (bài 04)
    → ghép URL: /tasks/create
    → Ninja biết method nào xử lý request này: create_task

Bước 2 — Khởi tạo Controller
    TaskController.__init__() chạy (bài 03)
    → self.auth_service, self.task_service... đã sẵn sàng

Bước 3 — Validate input
    payload: TaskCreateSchema (bài 02)
    → Ninja parse JSON body, ép vào TaskCreateSchema
    → nếu thiếu field bắt buộc → trả 422 ngay, KHÔNG chạy tới bước 4

Bước 4 — Business logic (code bạn tự viết)
    user_id, error = await self.auth_service.get_user_or_401(request)
        → đọc token trong header, tự resolve ra user_id
        → nếu token sai/thiếu → error khác None
    if error: return error
        → return sớm, dùng nguyên response error đã build sẵn trong auth_service
    await self.task_service.create(user_id, payload)
        → lưu task vào DB, dùng self.task_service đã khởi tạo ở __init__

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
    "detail": "Task created successfully"
}
```

---

## 2. Endpoint Phức Tạp Hơn — `generate_report`

```python
@http_post("/generate-report", response=REPORT_ACTION_RESPONSE)
async def generate_report(self, request, payload: GenerateReportSchema):
    user_id, error = await self.auth_service.get_user_or_401(request)
    if error:
        return error

    guard = QuotaGuard(request.user)
    organization_id, error = await sync_to_async(guard.pre_check)()
    if error:
        return error

    try:
        report_data, meta = await self._execute_report(
            user_id, payload,
            action="generate_report",
            method_name="generate_report",
        )
    except ValueError as e:
        if str(e) == "Task not found":
            return 404, {"code": "not_found", "detail": "Task not found"}
        raise
    await sync_to_async(guard.charge)(organization_id, meta)
    if not report_data:
        return REPORT_INVALID_ERROR

    report = await self.report_service.save_report(
        user_id=user_id, task_id=payload.task_id, content=report_data,
    )
    return {"report_id": report.id, "content": report_data}
```

Endpoint này phức tạp hơn vì có thêm 2 việc **không thuộc khái niệm Ninja/ninja-extra**, mà là logic nghiệp vụ — cần phân biệt rõ để không nhầm là "cú pháp Ninja":

```text
1. QuotaGuard              → kiểm tra + trừ hạn mức trước/sau khi gọi service ngoài (nghiệp vụ billing)
2. self._execute_report(...) → helper nội bộ gọi service ngoài thật, raise ValueError nếu task không tồn tại
```

Trace phần **thuộc về Ninja/ninja-extra** (những gì đã học ở bài 01-04):

```text
Routing:      @http_post("/generate-report") + prefix "/tasks" → POST /tasks/generate-report
Validate:     payload: GenerateReportSchema → Ninja tự parse + validate JSON body
Service DI:   self.auth_service, self.report_service → dùng lại từ __init__, không tạo mới
Response:     response=REPORT_ACTION_RESPONSE = {200: Any, 402: ErrorResponse, **COMMON_ERROR_RESPONSES}
    → return {"report_id":..., "content":...} khớp status 200, type Any (không ép kiểu chặt)
    → return 404, {...} khớp COMMON_ERROR_RESPONSES
```

Trace phần **thuộc về nghiệp vụ** (không phải Ninja):

```text
guard.pre_check()      → check hạn mức đủ không, trả lỗi 402 nếu thiếu (định nghĩa trong REPORT_ACTION_RESPONSE)
self._execute_report()  → gọi service ngoài, raise ValueError nếu thiếu task
guard.charge()          → trừ hạn mức sau khi service ngoài chạy xong
```

---

## 3. Vì Sao Phải Tách 2 Phần Này Rõ Ràng?

```text
Nếu đọc code mà không tách được "cái gì là Ninja/ninja-extra" và "cái gì là business logic":
    → dễ nhầm QuotaGuard là 1 phần của framework (không phải)
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

> Thực tế: pattern `generate_report` ở trên mô phỏng đúng cấu trúc endpoint `suggest_titles` trong `article_writer.py` (project `leadplusone_api`) — ở đó, `QuotaGuard` tương ứng `AiCreditGuard` (kiểm tra/trừ credit AI) và service ngoài là AI thật, còn `_execute_report` tương ứng `_execute_ai`.

---

## 4. Kết Luận

Cần chốt:

- Một request đi qua đúng thứ tự: routing (`api_controller` + `http_xxx`) → khởi tạo Controller (`__init__`) → validate input (`Schema`) → business logic (`self.<service>`) → response (đối chiếu `response={...}`).
- Guard kiểm tra hạn mức, helper gọi service ngoài, quản lý bản ghi liên quan... là logic nghiệp vụ riêng của từng project, không phải cú pháp Ninja/ninja-extra — cần phân biệt để không học nhầm.
- Đọc 1 endpoint ninja-extra bất kỳ theo 4 bước ở mục 3 sẽ áp dụng được cho mọi controller, không chỉ 2 ví dụ ở đây.

Bài cuối cùng (`06-so-sanh-drf-vs-ninja-vs-ninja-extra.md`) đặt 3 kiểu viết API (DRF, Ninja thuần, ninja-extra) cạnh nhau để so sánh trực tiếp — giờ bạn đã có đủ nền tảng Ninja/ninja-extra để đọc bài đó dễ hơn.
