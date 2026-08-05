# Pagination / Ordering / Searching / Throttling — Có Sẵn, Repo Chưa Dùng Cái Nào

> Tiếp theo `14-dependency-injection-thuc-su-qua-injector.md`. 4 tính năng trong bài này đều là thật, có source rõ ràng trong `ninja`/`ninja-extra`, nhưng đã grep toàn bộ `leadplusone_api/source_code/` — **cả 4 đều cho 0 kết quả**. Viết ra để biết framework có gì sẵn, không phải vì repo đang dùng.

3 tính năng đầu (pagination/ordering/searching) cùng 1 họ: decorator đặt trên method `list`, tự thêm query param + tự xử lý list trả về. Throttling khác nhóm (rate-limit), nhưng cũng cùng cách khai (`throttle=` giống `permissions=` đã học ở bài 08).

---

## 1. Pagination — `@paginate`

Docstring thật trong `ninja/pagination.py:176-188`:

```python
def paginate(func_or_pgn_class=NOT_SET, **paginator_params):
    """
    @api.get(...
    @paginate
    def my_view(request): ...

    or

    @api.get(...
    @paginate(PageNumberPagination)
    def my_view(request): ...
    """
```

Dùng thật:

```python
from ninja_extra.pagination import paginate, PageNumberPaginationExtra

@http_get("/list", response=List[TaskSchema])
@paginate(PageNumberPaginationExtra, page_size=20)
async def list_tasks(self, request):
    return Task.objects.all()   # trả nguyên queryset, decorator tự cắt trang
```

`PageNumberPaginationExtra` (`ninja_extra/pagination/models/page_by_number.py:26-46`) trả response kiểu DRF quen thuộc: `{count, next, previous, results}`. Setting mặc định class dùng nếu không chỉ định: `PAGINATION_CLASS` trong `NINJA_EXTRA` (bài 13).

> Thực tế: repo có sẵn 1 class **tự viết tay** — `BasePagination` (`__Common/viewsets/_base_viewset.py:92-160`), cắt list bằng slicing Python thủ công (`list[query_from:query_to]`), dùng chung cho cả module DRF cũ và ninja-extra mới. `@paginate`/`PageNumberPaginationExtra` của framework **chưa dùng ở đâu** — không sai, chỉ là project chọn tái dùng code cũ thay vì đổi sang cơ chế mới của framework.

---

## 2. Ordering — `@ordering`

`ninja_extra/ordering/decorator.py:28-47`:

```python
def ordering(func_or_ordering_class=NOT_SET, **ordering_params): ...
```

Dùng thật (theo đúng cách `Ordering` class xử lý — `ninja_extra/ordering/models.py:14-34`, tự thêm query param `ordering` rồi gọi `.order_by(*fields)`):

```python
from ninja_extra.ordering import ordering, Ordering

@http_get("/list", response=List[TaskSchema])
@ordering(Ordering, ordering_fields=["created_at", "priority"])
async def list_tasks(self, request):
    return Task.objects.all()
```

```text
GET /tasks/list?ordering=-created_at   → tự order_by("-created_at")
```

> Thực tế: **chưa dùng** trong repo — grep `@ordering`/`ninja_extra.ordering` ra 0 kết quả.

---

## 3. Searching — `@searching`

`ninja_extra/searching/decorators.py:28-47` — cùng cấu trúc decorator với `ordering`. `Searching` class (`ninja_extra/searching/models.py:29-52`) tự thêm query param `search`, hỗ trợ tiền tố lookup kiểu DRF:

```text
^field   → istartswith
=field   → iexact
@field   → search (full-text, nếu DB hỗ trợ)
$field   → iregex
```

Dùng thật:

```python
from ninja_extra.searching import searching, Searching

@http_get("/list", response=List[TaskSchema])
@searching(Searching, search_fields=["title", "^assignee_name"])
async def list_tasks(self, request):
    return Task.objects.all()
```

```text
GET /tasks/list?search=report   → tìm "report" trong title (icontains) và assignee_name (istartswith, do có tiền tố ^)
```

> Thực tế: **chưa dùng** trong repo — grep `@searching`/`ninja_extra.searching` ra 0 kết quả.

---

## 4. Throttling — `throttle=`

Đặt cùng cách với `permissions=` đã học ở bài 08 — khai ở `NinjaExtraAPI(throttle=...)`, `@api_controller(..., throttle=...)`, hoặc `@http_get(..., throttle=...)`:

```python
from ninja_extra.throttling import UserRateThrottle

@api_controller("/tasks")
class TaskController(ControllerBase):
    @http_post("/create", throttle=[UserRateThrottle(rate="10/min")])
    async def create_task(self, request, payload: TaskCreateSchema):
        ...
```

Class có sẵn (`ninja_extra/throttling/model.py`): `AnonRateThrottle` (scope `"anon"`), `UserRateThrottle` (scope `"user"`), `DynamicRateThrottle` (scope tùy chỉnh theo tham số). Vượt rate → tự raise lỗi 429, không cần tự viết `if too_many_requests: return 429`.

**⚠️ Lưu ý setting key khác nhau giữa 2 package** (đã nói ở bài 13, nhắc lại vì dễ nhầm ở đúng chỗ này):

```python
# ninja core — key rời
NINJA_DEFAULT_THROTTLE_RATES = {"anon": "1000/day", "user": "10000/day"}

# ninja-extra — key nằm trong dict NINJA_EXTRA
NINJA_EXTRA = {"THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"}}
```

> Thực tế: **chưa dùng** trong repo — grep `throttle` (không phân biệt hoa thường) toàn `source_code/` ra 0 kết quả liên quan (chỉ có 1 dòng comment không liên quan ở `F94_AI_Tools/auth/client_auth.py`).

---

## 5. Kết Luận

Cần chốt:

- 4 tính năng đều thật, có decorator/class rõ ràng (`@paginate`, `@ordering`, `@searching`, `throttle=`) — nhưng **0 usage** trong `leadplusone_api` tính đến hiện tại.
- Pagination của project dùng `BasePagination` tự viết tay (`__Common/viewsets/_base_viewset.py`), không phải `@paginate` của framework — 2 cơ chế khác nhau, không nên nhầm khi đọc code.
- Nếu sau này cần thêm ordering/searching cho 1 endpoint list, đây là cách "đúng chuẩn framework" thay vì tự viết `request.GET.get("ordering")` tay.

Bài tiếp theo (`16-testing-voi-ninja-extra.md`) — bài cuối cùng của roadmap — giới thiệu `ninja_extra.testing.TestClient`, công cụ test controller mà không cần dựng `NinjaAPI` đầy đủ.
