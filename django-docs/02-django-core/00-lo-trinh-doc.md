# Tầng 02 — Django Core

> Đây là giáo trình chính. Đọc **đúng theo số 01 → 10**, mỗi bài dựa trên bài trước.
> Điều kiện: đã đọc `01-bat-dau/`.

| Bài | File | Chủ đề |
|:--|:--|:--|
| 01 | `01-request-response.md` | Vòng đời một request: từ gõ URL tới lúc thấy trang web |
| 02 | `02-urls.md` | URL Dispatcher — `path()`, `include()`, phân luồng |
| 03 | `03-views.md` | Views (function-based) — bộ não xử lý |
| 04 | `04-models.md` | Model cơ bản — field, quan hệ, CRUD, `Meta` |
| 05 | `05-models-nang-cao.md` | Model bổ sung từ docs chính thức — `null` vs `blank`, `through`, verbose name |
| 06 | `06-orm.md` | ORM & QuerySet API — filter, lookup, `select_related`, `Q`, `F` |
| 07 | `07-migration.md` | `makemigrations` / `migrate` — versioning database |
| 08 | `08-forms.md` | Form & ModelForm, validation, CSRF |
| 09 | `09-templates.md` | Template engine — `{{ }}`, `{% %}`, kế thừa layout |
| 10 | `10-admin-panel.md` | Django Admin — `ModelAdmin`, customize |

**Ghi chú thứ tự:**

- Bài 04-05 (định nghĩa bảng) phải đọc **trước** bài 06 (truy vấn bảng).
- Bài 07 Migration đi liền sau 04-06 vì nó là hệ quả trực tiếp của việc sửa model.

**Đọc xong tầng này →** `03-class-based-views/` (viết lại bài 03 theo kiểu class),
sau đó `05-drf-roadmap/` nếu làm API.
