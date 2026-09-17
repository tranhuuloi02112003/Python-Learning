# Lộ Trình Đọc — Django Ninja / ninja-extra

> File này là mục lục, không tính vào số thứ tự bài học (giống `05-drf-roadmap/00-lo-trinh-doc.md`). Đọc file này trước để biết bắt đầu từ đâu.

Toàn bộ ví dụ minh họa dùng 1 domain xuyên suốt (`TaskController`, tự tạo, không cần biết trước project nào) — riêng mỗi bài đều có 1 dòng `> Thực tế:` đối chiếu với file thật `article_writer.py` trong project `leadplusone_api`.

---

## `core/` — Đọc Trước Tiên (bài 01-10)

Đủ để đọc hiểu `article_writer.py` từ đầu tới cuối. Đọc đúng thứ tự số.

| Bài | Chủ đề |
|:--|:---|
| 01 | Django Ninja là gì — flow cơ bản, router, function-based |
| 02 | Pydantic Schema validate input, `response={...}` serialize output |
| 03 | `api_controller` + `ControllerBase` + `__init__` (dependency) |
| 04 | `@http_get/post/put/patch/delete` + path param `{id}` |
| 05 | Trace full 1 endpoint đơn giản + 1 endpoint phức tạp, từ request tới response |
| 06 | So sánh 3 kiểu viết API: DRF vs Ninja thuần vs ninja-extra |
| 07 | `async`/`await`/`sync_to_async` |
| 08 | Auth khai ở cấp API instance (`auth=`), khác DRF khai theo từng view |
| 09 | Kiến trúc: mỗi feature app 1 `NinjaExtraAPI` riêng + versioning |
| 10 | 1 project có thể vừa có DRF, vừa có ninja-extra (hiện trạng thật của `leadplusone_api`) |

---

## `focus/` — Đọc Tiếp Theo (bài 11-12)

Framework có, và **đang dùng thật** ở feature app khác trong `leadplusone_api` (không phải `article_writer.py`, nhưng sẽ gặp khi đọc/viết endpoint mới).

| Bài | Chủ đề |
|:--|:---|
| 11 | `Query()` (query string), `Form()`/`File()` (multipart form data, upload) |
| 12 | Exception handler toàn cục — `@api.exception_handler`, hierarchy `APIException` của ninja-extra |

---

## `advanced/` — Đọc Sau Cùng (bài 13-17)

Framework có sẵn, nhưng **grep toàn repo `leadplusone_api` ra 0 kết quả** — chưa dùng ở đâu cả. Biết để không nhầm khi gặp ở project khác, hoặc để cân nhắc dùng khi viết feature mới.

| Bài | Chủ đề |
|:--|:---|
| 13 | `self.context` (`RouteContext`) + settings toàn cục (`NINJA_*` vs `NINJA_EXTRA`) |
| 14 | Dependency Injection thật qua thư viện `injector` (đào sâu bài 03) |
| 15 | Pagination / Ordering / Searching / Throttling native |
| 16 | Testing — `ninja_extra.testing.TestClient`/`TestAsyncClient` |
| 17 | Auto-CRUD — `ModelControllerBase` (tương đương DRF `ModelViewSet`) |

---

## Tư Tưởng Chung Của Cả Roadmap

```text
ninja/ninja-extra luôn có 1 cách viết ngắn hơn DRF cho cùng bài toán
(Schema thay Serializer, decorator route thay urls.py, response={...} thay Response(),
auto-DI thay __init__ tay, ModelControllerBase thay ModelViewSet...)
— nhưng KHÔNG BẮT BUỘC phải dùng cách mới. Project có quyền chọn cách quen thuộc
(viết tay, tái dùng code cũ) miễn là chạy đúng — leadplusone_api đang chọn vậy
ở khá nhiều chỗ (core/09, focus, và toàn bộ advanced/).
```
