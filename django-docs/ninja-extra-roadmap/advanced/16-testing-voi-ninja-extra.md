# Testing Controller ninja-extra — Dự Án Đang Làm Gì, Và Framework Có Gì Thêm

> Tiếp theo `15-list-features-va-throttling-chua-dung.md`. Đã đọc trực tiếp toàn bộ file test thật liên quan tới controller ninja-extra trong repo (không chỉ grep suông) để trả lời đúng 2 câu: **dự án đang test kiểu gì, cách nào dùng nhiều nhất** — rồi mới tới **framework còn có gì mà repo chưa dùng**.

---

## 1. Cái Đã Biết Từ DRF — `TestCase` + `self.client`

Cách quen thuộc nhất khi test 1 API view bằng DRF: kế thừa `TestCase`/`APITestCase`, dùng `self.client` (Django test client, gọi HTTP thật vào 1 URL path, không cần server thật chạy), đọc `response.status_code`/`response.json()`:

```python
class MyViewTests(APITestCase):
    def test_something(self):
        response = self.client.get("/api/tasks/list")
        self.assertEqual(response.status_code, 200)
```

Đây **chính là cách được dùng nhiều nhất trong repo cho cả controller ninja-extra** — không đổi gì so với thói quen DRF cũ, xem mục 2.

---

## 2. Dự Án Đang Test Controller ninja-extra Như Thế Nào — 3 Cách, Xếp Theo Mức Độ Phổ Biến

Đã đọc trực tiếp file test của các feature app đã chuyển sang ninja-extra (F26, F51, F94, F16, F21, F27, F15, F22, F29, F17). Không có 1 chuẩn chung — 3 cách khác nhau tồn tại song song.

### Cách 1 — Dùng nhiều nhất (8/10 feature app): giữ nguyên `TestCase` + `self.client`, y hệt mục 1

```python
# MPF_WEB_F51_Credit_Management/unit_tests/test_endpoints.py
resp = self.client.get(f"{BASE}/get-credit-balance")
self.assertEqual(resp.status_code, 401)
```

Dùng ở F51, F94, F16, F21, F27, F15, F22, F29. Gọi HTTP thật vào URL path (literal string hoặc `reverse()`), đi qua đủ route/auth/middleware — về bản chất **không cần biết controller là ninja-extra hay DRF**, `self.client` xử lý như nhau, vì Django tự bridge sync/async ở tầng nhận request.

### Cách 2 — Gọi thẳng method của controller, bỏ qua lớp HTTP (F17, và 1 phần F26)

```python
# MPF_WEB_F17_Request_And_Feedback/unit_tests/test_request_feedback.py
response = async_to_sync(self.controller.create_request_feedback)(
    request, category="bug", description="...", files=[image1, image2], ...
)
self.assertEqual(response["code"], "success")
```

Vì method là `async def`, phải bọc `async_to_sync(...)` để gọi được trong `TestCase` (sync) — tự tạo `request` giả (`FakeRequest`/`RequestFactory`), tự mock service, không đi qua route/middleware nào. `MPF_WEB_F26_My_Page/unit_tests/test_rewrite_article.py` cũng làm y vậy: `async_to_sync(self.controller.style_setting_create)(request, payload=payload)`.

### Cách 3 — Chỉ 1 file, khác cả 2 cách trên (F26)

```python
# MPF_WEB_F26_My_Page/unit_tests/test_informative_document.py
url = reverse(...)
response = self.client.get(url, format="json")
```

`APITestCase` (DRF) + `reverse()` — cùng ý tưởng cách 1 nhưng thêm `reverse()` để không hard-code path.

**Điểm chung cả 3 cách: không app nào dùng `django.test.AsyncClient`**, dù mọi method trong các controller này là `async def`.

---

## 3. Cái Mới Framework Có — `ninja_extra.testing.TestClient`/`TestAsyncClient`

Đây là phần **repo hiện chưa dùng ở đâu cả** (grep `TestClient`/`TestAsyncClient`/`ninja_extra.testing` → 0 kết quả) — khác biệt với 3 cách ở mục 2, cách này không cần Django test server thật lẫn không cần tự dựng `RequestFactory`/`FakeRequest` tay.

Verify source `ninja_extra/testing/client.py`:

```python
class NinjaExtraClientBase(NinjaClientBase):
    def __init__(self, router_or_app, **kw):
        if hasattr(router_or_app, "get_api_controller"):   # đây là 1 Controller class
            api = NinjaExtraAPI(**kw)
            controller_ninja_api_controller = router_or_app.get_api_controller()
            controller_ninja_api_controller.set_api_instance(api)
            router_or_app = api
        super().__init__(router_or_app)

class TestClient(NinjaExtraClientBase):
    def _call(self, func, request, kwargs):
        return NinjaResponse(func(request, **kwargs))

class TestAsyncClient(NinjaExtraClientBase):
    async def _call(self, func, request, kwargs):
        return NinjaResponse(await func(request, **kwargs))
```

Điểm hay nhất, đã verify: `TestClient` nhận **trực tiếp class Controller** (không cần tự tạo `NinjaExtraAPI` trước) — nó tự tạo 1 `NinjaExtraAPI` tạm bên trong, tự mount controller vào:

```python
from ninja_extra.testing import TestClient
from myapp.controllers import TaskController

client = TestClient(TaskController)
response = client.get("/list")
print(response.status_code, response.json())
```

Với controller `async def` (như `article_writer.py`), dùng `TestAsyncClient` — khớp đúng bản chất async, không cần `async_to_sync` như cách 2 ở mục 2:

```python
from ninja_extra.testing import TestAsyncClient

client = TestAsyncClient(ArticleWriterController)
response = await client.get("/persona/list")
```

Cả 2 client build request giả (mock) rồi gọi trực tiếp function xử lý — không qua network/server thật, nên nhanh hơn cách 1 (mục 2), mà vẫn đi "đủ tầng" route hơn cách 2 (không cần tự dựng `FakeRequest` tay).

**So 3 cách hiện có (mục 2) với `TestClient`/`TestAsyncClient`:**

| | Cách 1 (dùng nhiều nhất) | Cách 2 | `TestClient`/`TestAsyncClient` (chưa dùng) |
|:---|:---|:---|:---|
| Gọi qua route thật? | Có | Không | Có (route thật, chỉ bỏ qua network) |
| Cần tự tạo request tay? | Không | Có (`FakeRequest`/`RequestFactory`) | Không |
| Khớp bản chất `async def`? | Gián tiếp (Django tự bridge) | Phải tự `async_to_sync` | Có (`TestAsyncClient` là async thật) |
| Cần Django test server/DB thật chạy? | Có | Không (mock hết) | Không |

Đây là điểm có thể cân nhắc nếu sau này muốn chuẩn hóa lại 3 cách hiện có thành 1 cách chung cho mọi controller ninja-extra trong repo — không có nhu cầu bắt buộc phải đổi ngay.

---

## 4. Kết Luận

Cần chốt:

- Cách test controller ninja-extra được dùng **nhiều nhất trong repo** (8/10 feature app) chính là thói quen DRF cũ: `TestCase` + `self.client` gọi HTTP thật — không cần học gì mới để tiếp tục viết test kiểu này.
- 2 cách khác (gọi thẳng method qua `async_to_sync`, hoặc `APITestCase` + `reverse()`) chỉ xuất hiện ở vài file, không phải chuẩn chung.
- `ninja_extra.testing.TestClient`/`TestAsyncClient` là công cụ framework có sẵn, **chưa được dùng ở đâu trong repo** — gộp ưu điểm của các cách hiện có (gọi qua route thật, không cần tự dựng request tay, khớp đúng async), đáng cân nhắc nếu cần viết nhiều test mới.

Bài tiếp theo (`17-auto-crud-model-controller.md`) — bài cuối cùng của roadmap — quay lại chủ đề auto-CRUD (`ModelControllerBase`), và chốt toàn bộ 17 bài.
