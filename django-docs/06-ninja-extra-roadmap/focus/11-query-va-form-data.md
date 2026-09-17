# `Query()` — Query String, và `Form()`/`File()` — Multipart Form Data

> Tiếp theo `core/10-project-vua-drf-vua-ninja-extra.md`. Từ bài này, các chủ đề không xuất hiện trong `article_writer.py` (file đã dùng xuyên suốt bài 01-10), nhưng có dùng thật ở feature app khác trong `leadplusone_api` — vẫn cần biết vì sẽ gặp khi đọc/viết endpoint mới.

---

## 1. Vấn Đề Cần Giải Quyết — 3 Chỗ Nhét Dữ Liệu Vào 1 Request

Trước khi vào cú pháp, cần hiểu **tại sao** lại có `Query`/`Form`/`File` — chúng không phải tính năng "cho có", mà giải quyết đúng 1 vấn đề: 1 request có 3 chỗ khác nhau để mang dữ liệu, mỗi chỗ hợp 1 việc:

```text
Path      → xác định CHÍNH XÁC resource nào    (VD: /tasks/7  → task số 7, bắt buộc phải có)
Body      → gửi dữ liệu CÓ CẤU TRÚC để tạo/sửa (VD: {"title": "...", "priority": 1})
Query     → thêm điều kiện LỌC/TÙY CHỌN cho 1 request, không xác định resource nào cả
```

**Ví dụ cụ thể:** có endpoint `GET /tasks/list` trả về danh sách task. Giờ muốn thêm: "chỉ lấy task đang active" + "chỉ lấy 10 task đầu". Nhét thông tin này vào đâu?

- **Không thể nhét vào path** — path dùng để chỉ định 1 resource cụ thể (`/tasks/7`), còn đây là lọc cả 1 danh sách, không phải 1 resource.
- **Không nên nhét vào body** — quy ước HTTP là `GET` không có body (nhiều thư viện/proxy/cache không hỗ trợ hoặc bỏ qua body của `GET`). Và vì `GET` được cache/bookmark theo URL, nếu điều kiện lọc không nằm trong URL thì không cache/share link được.
- **→ Query string chính là chỗ dành riêng cho việc này** — phần sau dấu `?` trong URL:

```text
GET /tasks/list?status=active&limit=10
                └──────┬──────┘
                 đây là query string — không xác định resource, chỉ thêm điều kiện lọc
```

**Nếu không có `Query()` thì sao?** Vẫn lấy được dữ liệu — nhưng phải tự làm hết, giống DRF:

```python
# Không dùng Query() — tự đọc, tự ép kiểu, tự validate
status = request.GET.get("status", "active")       # luôn ra string, dù bạn muốn int/bool
limit = request.GET.get("limit", "10")
try:
    limit = int(limit)          # client gửi limit=abc thì crash, phải tự try/except
except ValueError:
    limit = 10
```

`Query()` chỉ là cách Ninja **tự động hóa đúng việc này**: khai `status: str = "active", limit: int = 10` trong signature, Ninja tự đọc từ `?status=...&limit=...`, tự ép `limit` sang `int`, tự trả lỗi 422 nếu client gửi `limit=abc`. Không phải tính năng mới, chỉ đỡ phải tự viết đoạn `try/except` ép kiểu ở trên.

`Form`/`File` (mục 3) giải quyết đúng vấn đề tương tự, chỉ khác nguồn dữ liệu: thay vì lọc 1 danh sách qua `GET`, đây là gửi dữ liệu dạng `multipart/form-data` (thường kèm file) qua `POST` — không dùng JSON body (`Schema`) được vì JSON không mang được file nhị phân.

**Tóm lại:**

| Cần gì | Dùng gì |
|:---|:---|
| Xác định 1 resource cụ thể | Path param `{id}` |
| Gửi dữ liệu có cấu trúc (tạo/sửa), thuần JSON | Body — `Schema` (bài 02) |
| Lọc/tùy chỉnh 1 danh sách, không xác định resource nào | Query — mục 2 |
| Gửi kèm file, hoặc dữ liệu dạng `multipart/form-data` | Form/File — mục 3 |

---

## 2. `Query()` — Nhận Query String (`?status=active&limit=10`)

**"Scalar" là gì?** 1 giá trị đơn — `str`, `int`, `float`, `bool` (VD: `status: str`, `limit: int`). Khác với type "structured" (nhiều giá trị gộp lại) như `Schema`, `dict`, `list` (VD: `payload: TaskCreateSchema` gồm nhiều field). Query string (`?status=active&limit=10`) chỉ mang được các cặp `key=value` dạng text đơn giản, không nhồi được 1 object nhiều field vào đó — vì vậy Ninja dùng type để đoán: scalar → chắc muốn lấy từ query string; structured → chắc muốn lấy từ JSON body.

Đã verify source `ninja/params/functions.py:50-86` (django-ninja 1.4.5):

```python
def Query(default=..., *, alias=None, title=None, description=None,
          gt=None, ge=None, lt=None, le=None,
          min_length=None, max_length=None, pattern=None, ...) -> Any:
    return models.Query(default, alias=alias, ...)
```

Cách dùng đơn giản nhất — tham số scalar trong function signature, **có hoặc không có** giá trị mặc định đều được:

```python
@http_get("/list")
async def list_tasks(self, request, status: str, limit: int = 10):
    #                                ^^^^^^^^^^^          ^^^^^^^^^^^^^^
    #                                KHÔNG default         CÓ default
    #                                → status BẮT BUỘC     → limit TÙY CHỌN
    ...
```

```text
GET /tasks/list?limit=5
    → thiếu status → Ninja tự trả lỗi 422 "field required" (status không có default → bắt buộc)
GET /tasks/list?status=done&limit=5
    → status = "done", limit = 5 (Ninja tự lấy từ query string, tự ép kiểu)
GET /tasks/list?status=done
    → status = "done", limit = 10 (limit không truyền → dùng default)
```

**Điểm hay bị hiểu nhầm:** không cần viết `Query(...)` tường minh để 1 tham số trở thành query param — và **cũng không cần có default**. Đã verify `ninja/signature/details.py:257-280` — thứ tự Ninja tự đoán "tham số này nên lấy từ đâu":

```text
1. Có Param (Query/Path/Body/Form/File...) khai tường minh → dùng đúng cái đó
2. Tên khớp 1 path param trong path string ({task_id}...)  → tự hiểu là Path
3. Type là Schema/dict/list (structured)                    → tự hiểu là Body (payload)
4. Còn lại (scalar, không khớp path)                        → tự hiểu là Query  ← fallback
```

Rule 4 chỉ cần "scalar + không khớp path" — **không đòi hỏi có default**. Default chỉ quyết định query đó bắt buộc (`status: str`) hay tùy chọn (`limit: int = 10`), không quyết định nó có phải Query hay không. Vậy cả `status: str` và `limit: int = 10` ở ví dụ trên đều **tự động** là query param, không cần viết `Query(...)`.

> Đã verify bằng thực nghiệm (cài `django-ninja` thật, gọi qua `ninja.testing.TestClient`, không chỉ đọc docs): `def view(request, limit: int)` (không `Query()`, không default) → gọi thiếu `?limit=` trả đúng `422 "Field required"`; gọi `?limit=5` → nhận đúng `int`. Kết quả giống hệt `limit: int = Query(30)`. Cũng verify luôn: **vị trí tham số trong signature không ảnh hưởng** — 4 quy tắc trên áp dụng độc lập cho từng tham số theo tên/type, không theo thứ tự khai (xem thêm bài `core/04-http-method-decorator-va-path-param.md`, mục 5).

Chỉ cần `Query(...)` tường minh khi muốn thêm validation hoặc đổi tên:

```python
date_option: str = Query("last_3_months", alias="date")
```

`alias="date"` nghĩa là: client gọi `?date=...`, nhưng trong code dùng biến `date_option` — tách tên hiển thị ra ngoài (URL) khỏi tên dùng trong code.

> Thực tế: `Query` **đang dùng rất nhiều** trong repo — `MPF_WEB_F22_GSC_Analytics/controllers.py:43-50`:
> ```python
> site_code: str = Query(None),
> start_date: str = Query(None),
> date_option: str = Query("last_3_months", alias="date"),
> list_tag: str = Query(None, alias="tag"),
> ```
> Cũng thấy `from ninja import Query` ở `F16_SEO_Keyword_Agent`, `F21_GA4_Analytics`, `F27_Chat_Bot`, `F15_FAQs_Chat_Bot`, `article_writer.py`'s sibling file `create_proposal.py` — đây là 1 pattern rất phổ biến trong project, không phải tính năng hiếm dùng.

So với DRF — DRF không có khai báo type-safe cho query param, phải tự đọc và tự ép kiểu tay:

```python
# DRF
status = request.query_params.get("status", "active")   # luôn là str, tự ép int/bool nếu cần
limit = int(request.query_params.get("limit", 10))        # tự try/except nếu client gửi sai kiểu

# Ninja — khai type hint, Ninja tự ép kiểu + tự validate, tự trả 422 nếu sai
async def list_tasks(self, request, status: str = "active", limit: int = 10): ...
```

---

## 3. `Form()` / `File()` — Nhận `multipart/form-data`

**Không phải "đã có `payload: Schema` rồi sao còn cần thêm cái này"** — 2 cơ chế dùng cho 2 loại request khác nhau, không thay thế nhau được:

```text
Content-Type: application/json        → payload: Schema đọc được (JSON — chỉ là text thuần)
Content-Type: multipart/form-data     → Form()/File() đọc được (text field + file nhị phân trộn lẫn)
```

JSON không có chỗ nào để nhúng trực tiếp 1 file nhị phân (ảnh, PDF...) — muốn gửi file, client (browser với `<input type="file">`, hoặc app upload ảnh) phải gửi theo format khác hẳn: `multipart/form-data`. `payload: Schema` chỉ biết parse JSON, không đọc được format này — đó là lý do cần `Form`/`File` riêng.

Cùng họ với `Query()`, khai bằng function tương tự (`ninja/params/functions.py:206-281`), nhưng đọc từ `request.POST` (Form) và `request.FILES` (File) thay vì `request.GET`:

```python
from ninja import Form, File
from ninja.files import UploadedFile

@http_post("/create")
async def create_request_feedback(
    self, request,
    category: str = Form(...),           # (...)  = required, giống Pydantic
    description: str = Form(...),
    files: List[Any] = File(None),        # None = optional
    screenshot_file: Optional[Any] = File(None),
):
    ...
```

`UploadedFile` (`ninja/files.py:9`) là type Ninja cung cấp, bọc lại `django.core.files.uploadedfile.UploadedFile` — có 1 điểm tự động hóa: nếu tham số khai type là `UploadedFile` (dù không viết `File(...)` tường minh), Ninja **tự nhận diện** đó là file param (`ninja/signature/details.py:249-255` — docstring ghi rõ lý do: *"People often forgot to mark UploadedFile as a File"*).

> Thực tế: `Form`/`File` **đang dùng thật** ở `MPF_WEB_F17_Request_And_Feedback/controllers.py:5,68-75` — 1 endpoint nhận feedback kèm ảnh chụp màn hình, trộn cả `Form` field và `File` upload trong cùng 1 method, sau đó forward qua `httpx` sang n8n:
> ```python
> @http_post("/create", response={200: Dict[str, Any], **COMMON_ERROR_RESPONSES}, url_name="request_feedback_create")
> async def create_request_feedback(
>     self, request,
>     category: str = Form(...),
>     description: str = Form(...),
>     page_url: str = Form(...),
>     files: List[Any] = File(None),
>     screenshot_file: Optional[Any] = File(None),
> ):
> ```
> Test tương ứng dùng `django.core.files.uploadedfile.SimpleUploadedFile` để giả lập file upload (`MPF_WEB_F17_Request_And_Feedback/unit_tests/test_request_feedback.py`).
>
> Cũng thấy 1 cách dùng khác ở `MPF_WEB_F16_SEO_Keyword_Agent/controllers.py:7,164` — chỉ upload file, không trộn `Form`:
> ```python
> async def upload_file(self, request, file: UploadedFile = File(...)):
> ```

So với DRF — DRF đọc file/form field thủ công qua `request.data`/`request.FILES`, không có type hint nào ràng buộc:

```python
# DRF
category = request.data.get("category")
uploaded = request.FILES.get("screenshot_file")

# Ninja — khai rõ trong signature, Ninja tự validate required/optional
category: str = Form(...)
screenshot_file: Optional[Any] = File(None)
```

---

## 4. Kết Luận

Cần chốt:

- 3 chỗ nhét dữ liệu vào request, mỗi chỗ hợp 1 việc: Path (xác định resource), Body/`Schema` (dữ liệu có cấu trúc), Query (lọc/tùy chọn cho `GET`) — `Form`/`File` là biến thể của Body khi cần gửi kèm file.
- `Query()` nhận giá trị từ query string (`?key=value`) — nhưng phần lớn trường hợp không cần viết `Query(...)` tường minh, chỉ cần tham số scalar không khớp path param là Ninja tự hiểu đó là query param (mục 2, quy tắc fallback) — **có default hay không đều được**, default chỉ quyết định bắt buộc/tùy chọn. Chỉ cần `Query(...)` khi muốn thêm validation hoặc `alias=` đổi tên.
- `Form()`/`File()` nhận `multipart/form-data` — cùng cú pháp họ với `Query`, đọc từ `request.POST`/`request.FILES`. `UploadedFile` được tự nhận diện là file param dù không viết `File(...)`.
- Cả 2 đang được dùng thật, khá phổ biến trong `leadplusone_api` (Query ở nhiều feature app; Form+File ở feedback/upload) — không phải tính năng lý thuyết.

Bài tiếp theo (`12-error-handling-exception-toan-cuc.md`) đi vào cách ninja/ninja-extra xử lý lỗi tập trung ở 1 chỗ, thay vì `try/except` rải rác trong từng method như `article_writer.py` đang làm.
