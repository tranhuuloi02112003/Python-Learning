# Kiến Trúc: Mỗi Feature App 1 `NinjaExtraAPI` Riêng + Versioning

> Tiếp theo bài 08. Bài này nói về khác biệt **kiến trúc tổ chức**, không phải cú pháp. (Auto-CRUD qua `ModelControllerBase` — 1 chủ đề riêng, không liên quan kiến trúc multi-instance — được tách sang bài `advanced/17-auto-crud-model-controller.md`.)

---

## 1. Mỗi Feature App Có Thể Có 1 `NinjaExtraAPI` Riêng, Không Nhất Thiết Dùng Chung 1 Router

DRF thường có xu hướng gom mọi ViewSet vào **1 router trung tâm** cho cả project. ninja-extra không ép buộc điều này — mỗi "feature" (module độc lập, VD: quản lý task, quản lý thanh toán...) có thể tự tạo **1 `NinjaExtraAPI` riêng**, đăng ký controller của riêng nó, rồi chỉ cần root `urls.py` include vào 1 prefix:

```python
# tasks/urls.py — feature "tasks" tự có 1 NinjaExtraAPI riêng
api = NinjaExtraAPI(urls_namespace="tasks_api", auth=SimpleTokenAuth())
api.register_controllers(TaskController)
urlpatterns = [path("v1/", include([path("", api.urls)]))]
```

```python
# billing/urls.py — feature "billing" có 1 NinjaExtraAPI KHÁC, độc lập hoàn toàn
api = NinjaExtraAPI(urls_namespace="billing_api", auth=SomeOtherAuth())
api.register_controllers(InvoiceController)
```

```python
# root urls.py — chỉ include từng feature vào 1 prefix riêng
path("tasks/", include("tasks.urls"))
path("billing/", include("billing.urls"))
```

Hệ quả của cách tổ chức này:

```text
- Mỗi feature có Swagger/OpenAPI docs RIÊNG, tại URL riêng — không gộp chung 1 trang
  docs toàn hệ thống như khi dùng 1 NinjaAPI() duy nhất cho cả project.
- Auth (bài 08) cũng có thể khai riêng cho từng feature — feature A dùng 1 auth class,
  feature B dùng auth class khác, vì mỗi feature là 1 NinjaExtraAPI instance độc lập.
```

So với DRF (thường thấy: 1 router trung tâm, mọi app đăng ký ViewSet vào đó, cùng chung 1 trang Swagger):

| | DRF (kiểu phổ biến) | ninja-extra (kiểu tách feature) |
|:---|:---|:---|
| Router/API instance | Thường 1 cái chung cho cả project | Mỗi feature 1 `NinjaExtraAPI` riêng (không bắt buộc, nhưng phổ biến) |
| Trang docs (Swagger) | 1 trang chung | Mỗi feature 1 trang riêng |
| Auth | Có thể khác nhau theo view, nhưng cùng 1 router | Có thể khác nhau theo feature, vì mỗi feature là 1 instance độc lập |

> Thực tế: project `leadplusone_api` không có 1 file `api.py` trung tâm nào cả — mỗi feature app (10 app khác nhau, module chứa `article_writer.py` là 1 trong số đó) tự tạo `NinjaExtraAPI()` + `register_controllers(...)` riêng trong `urls.py` của chính nó, và ít nhất 1 feature (module AI Tools) dùng hẳn 1 auth class khác hoàn toàn với các feature còn lại.

---

## 2. Versioning — Không Có Cơ Chế Built-in, Chỉ Có Pattern Thay Thế

Đã grep toàn bộ source `ninja` + `ninja_extra` (cả 2 package) tìm `version`/`URLPathVersioning`/`NamespaceVersioning` — **không tìm thấy cơ chế versioning built-in nào**, khác với DRF vốn có sẵn `URLPathVersioning`/`NamespaceVersioning`.

Cái duy nhất liên quan tới "version" là tham số `version=` khi tạo `NinjaAPI`/`NinjaExtraAPI` — nhưng đây chỉ là **metadata suông**, hiển thị trong OpenAPI schema/title, **không ảnh hưởng gì tới routing**:

```python
api = NinjaExtraAPI(version="1.0.0", urls_namespace="tasks_api")
# version="1.0.0" chỉ hiện trong docs Swagger, không tự thêm "/v1/" vào path nào cả
```

`urls_namespace` cũng chỉ dùng để tránh trùng tên namespace Django khi có nhiều instance `NinjaAPI` (mặc định tự sinh `"api-" + version` nếu không khai).

**Pattern thay thế thực tế** — chính là ý tưởng đã nói ở mục 1 (mỗi feature 1 `NinjaExtraAPI` riêng): muốn "versioning", tự tạo 1 instance riêng cho mỗi version, mount vào prefix URL riêng:

```python
# v1
api_v1 = NinjaExtraAPI(urls_namespace="tasks_v1")
urlpatterns = [path("v1/tasks/", api_v1.urls)]

# v2 — instance khác hoàn toàn, độc lập
api_v2 = NinjaExtraAPI(urls_namespace="tasks_v2")
urlpatterns += [path("v2/tasks/", api_v2.urls)]
```

> Thực tế: `leadplusone_api` chưa có nhu cầu multi-version API, nhưng đã áp dụng đúng pattern "1 instance + 1 prefix + 1 namespace" cho việc tách feature (không phải version) — ví dụ `MPF_WEB_F94_AI_Tools/urls.py`: `NinjaExtraAPI(urls_namespace="ai_tools_v1", ...)` + `path("v1/", api.urls)`. Tên namespace có hậu tố `_v1` nhưng đây là tách theo **feature**, chưa phải versioning thật theo nghĩa "cùng 1 feature, nhiều version API song song".

---

## 3. Pagination/Ordering/Searching/Throttling?

4 tính năng này (có sẵn trong Ninja/ninja-extra nhưng repo chưa dùng cái nào) được gộp riêng thành 1 bài — xem `advanced/15-list-features-va-throttling-chua-dung.md`.

---

## 4. Kết Luận

Cần chốt:

- ninja-extra không ép 1 router trung tâm — mỗi feature app có thể tự tạo 1 `NinjaExtraAPI` riêng, kéo theo Swagger docs riêng và auth có thể khác nhau giữa các feature.
- Không có cơ chế versioning built-in (không như DRF) — pattern thay thế là tự tách 1 `NinjaExtraAPI` instance riêng cho mỗi version, mount vào prefix URL riêng — dùng chung ý tưởng "1 instance riêng" với mục 1.

Bài tiếp theo (`10-project-vua-drf-vua-ninja-extra.md`) nói về việc 1 project có thể vừa có DRF vừa có ninja-extra — chính là hiện trạng thật của `leadplusone_api`.
