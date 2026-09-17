# Django Docs — Đọc Theo Thứ Tự Này

Toàn bộ tài liệu Django được xếp thành **6 tầng**. Số thư mục = thứ tự đọc.
Mỗi tầng có file `00-lo-trinh-doc.md` liệt kê chi tiết các bài bên trong.

```text
01-bat-dau/            →  02-django-core/  →  03-class-based-views/
                                │                      │
                          04-debug/ (ngang)            ↓
                                              05-drf-roadmap/  →  06-ninja-extra-roadmap/
```

---

## Thứ Tự Đọc

| # | Tầng | Số bài | Đọc khi nào | Mục lục |
|:--:|:--|:--:|:--|:--|
| 01 | `01-bat-dau/` | 3 | **Bắt đầu tại đây.** Chưa biết gì về Django | `01-bat-dau/00-lo-trinh-doc.md` |
| 02 | `02-django-core/` | 10 | Sau tầng 01. Giáo trình chính, đọc tuần tự 01→10 | `02-django-core/00-lo-trinh-doc.md` |
| 03 | `03-class-based-views/` | 8 | Sau `02-django-core/03-views.md` và `02-django-core/08-forms.md` | `03-class-based-views/00-lo-trinh-doc.md` |
| 04 | `04-debug/` | 2 | **Tầng ngang** — bất cứ lúc nào sau `02-django-core/03-views.md` | `04-debug/00-lo-trinh-doc.md` |
| 05 | `05-drf-roadmap/` | 20 | Khi chuyển từ render HTML sang làm API JSON | `05-drf-roadmap/00-lo-trinh-doc.md` |
| 06 | `06-ninja-extra-roadmap/` | 17 | Khi project dùng Django Ninja / ninja-extra thay DRF | `06-ninja-extra-roadmap/00-lo-trinh-doc.md` |

---

## Ba Lộ Trình Theo Mục Tiêu

**A. Làm web fullstack bằng Django Templates (người mới)**

```text
01-bat-dau/ (01→03)  →  02-django-core/ (01→10)  →  03-class-based-views/ (01→08)
```

**B. Làm API backend bằng DRF (đã biết Django Templates)**

```text
02-django-core/ (04,06,07 — ôn Model/ORM/Migration)  →  05-drf-roadmap/ (01→20)
```

**C. Đọc/viết code project dùng ninja-extra**

```text
05-drf-roadmap/ (01→09 — để có gốc so sánh)  →  06-ninja-extra-roadmap/ (01→17)
```

---

## Quy Ước Đặt Tên

- Thư mục: `NN-ten-tang/` — `NN` là thứ tự đọc của tầng.
- File bài học: `NN-ten-bai.md` — `NN` là thứ tự đọc **trong tầng đó**.
- File `00-lo-trinh-doc.md` là mục lục, **không tính** là một bài học.
- Tầng 05 và 06 chia thêm `core/` → `focus/` → `advanced/` → `test/`, nhưng số bài
  vẫn chạy liên tục xuyên qua các thư mục con (01→20 và 01→17), nên cứ đọc theo số.

---

## Việc Còn Dở

- `03-class-based-views/08-mixins-permissions-and-best-practices.md` — file rỗng, chưa viết nội dung.
