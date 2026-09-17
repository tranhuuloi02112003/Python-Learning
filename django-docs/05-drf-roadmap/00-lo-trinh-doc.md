# 🗺️ Roadmap: Django Template → Django REST Framework → Dự Án Thực Tế

> **Mục tiêu:** Chuyển từ Django Template developer → có thể join dự án API backend thực tế.
> **Điểm xuất phát:** Đã hoàn thành dự án Django Template (TaskLog PRO).


## Thứ Tự Đọc (bài 01-20)

Đọc đúng theo số. `core/` → `focus/` → `advanced/` → `test/`.

| Bài | File | Chủ đề |
|:--|:--|:--|
| 01 | `core/01-django-core-recap.md` | Ôn Django core trước khi vào DRF |
| 02 | `core/02-api-view-and-url-flow.md` | `@api_view` — API function-based đơn giản nhất |
| 03 | `focus/03-drf-request-response.md` | `request.data`, `Response()` — nền tảng trước CRUD |
| 04 | `focus/04-response-status-error-flow.md` | Status code và error flow |
| 05 | `focus/05-drf-serializers.md` | Serializer nhìn từ `ModelForm` |
| 06 | `focus/06-serializer-project-basic.md` | Serializer kiểu project thật |
| 07 | `focus/07-drf-apiview.md` | `APIView` class-based |
| 08 | `focus/08-viewset-router-basic.md` | `ViewSet` + `Router` |
| 09 | `focus/09-viewset-as-view-manual-mapping.md` | `as_view({...})` map tay |
| 10 | `focus/10-authentication-permission-basic.md` | Authentication / Permission |
| 11 | `focus/11-custom-response-base-class-basic.md` | Custom Response / Base class của team |
| 12 | `focus/12-django-orm-in-api-basic.md` | ORM trong API (N+1, select/prefetch) |
| 13 | `focus/13-django-transactions-in-api-basic.md` | `transaction.atomic()` khi write API |
| 14 | `focus/14-slack-notification-service-basic.md` | Service gửi Slack notification |
| 15 | `advanced/15-genericapiview-and-mixins.md` | `GenericAPIView` + Mixins |
| 16 | `advanced/16-generic-class-based-views.md` | Generic class-based views |
| 17 | `advanced/17-compare-apiview-generic-view-viewset.md` | So sánh 3 tầng APIView/Generic/ViewSet |
| 18 | `test/18-testing-foundation.md` | Nền tảng testing Django |
| 19 | `test/19-model-testing.md` | Model testing |
| 20 | `test/20-dry-run-debug.md` | Dry-run debug |

---

## Phần 1: Đánh Giá Kiến Thức Hiện Tại

### ✅ Đã nắm vững (giữ nguyên giá trị)

Các phần này là **xương sống** của Django – dù Template hay DRF đều cần:

| Kiến thức | Dùng ở Template | Dùng ở DRF |
|:----------|:---:|:---:|
| Project/App structure | ✅ | ✅ |
| `settings.py`, `INSTALLED_APPS` | ✅ | ✅ |
| `urls.py`, `include()`, `path()` | ✅ | ✅ |
| `models.py` | ✅ | ✅ |
| Migrations | ✅ | ✅ |
| ORM (filter, get, create, update) | ✅ | ✅ |
| Selectors / Services pattern | ✅ | ✅ |
| `views.py` (logic xử lý) | ✅ | ✅ (đổi cách viết) |

### ⏸️ Giảm ưu tiên (biết là đủ, không cần đào sâu thêm)

| Kiến thức Template | Lý do |
|:-------------------|:------|
| `extends` / `block` / `include` | DRF không render HTML |
| `context_processors` | Không có template context trong API |
| `csrf_token` | API dùng token auth, không dùng CSRF form |
| `messages` framework | API trả status code + JSON message |
| `redirect()` | API trả JSON, frontend tự điều hướng |
| ModelForm UI rendering | Thay bằng Serializer |
| Custom template tags/filters | Không có template |
| Form rendering nâng cao | Thay bằng Serializer validation |

---

## Phần 2: Flow So Sánh – Template vs DRF

### Luồng xử lý request

```txt
── Django Template ──────────────────────────────────────
Request → urls.py → views.py → selectors/services → forms/models → render(template.html)
                                                                          ↓
                                                                    HTML Response

── Django REST Framework ────────────────────────────────
Request → urls.py → ViewSet → selectors/services → models/serializers → Response(JSON)
                                                                              ↓
                                                                        JSON Response
```

**Sự thay đổi cốt lõi:** `forms.py` + `templates/` → `serializers.py` + `Response()`

### Mapping từng thành phần

| Django Template | Django REST Framework | Ghi chú |
|:----------------|:----------------------|:--------|
| `render(request, "template.html", context)` | `Response(data, status=200)` | Trả HTML → trả JSON |
| `template.html` | JSON response | Frontend tự render UI |
| `ModelForm` | `ModelSerializer` | Cùng validate + save, khác output |
| `request.POST` | `request.data` | DRF parse JSON/form-data tự động |
| `request.GET` | `request.GET` / `request.query_params` | Giống nhau |
| `messages.success()` | Status code + message trong JSON | `200`, `400`, `404`... |
| `redirect("/url/")` | `Response({"redirect": "/url/"})` | Frontend tự xử lý |
| `{% csrf_token %}` | Token Authentication | JWT / Session / API Key |
| `def view(request):` | `class ViewSet(GenericViewSet):` | FBV → CBV/ViewSet |

### Ví dụ cụ thể song song

**Template (đã biết):**

```python
# views.py
def project_list(request):
    projects = get_projects()
    return render(request, "projects/list.html", {"projects": projects})

# forms.py
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "status"]

# template
{% for project in projects %}
    {{ project.name }}
{% endfor %}
```

**DRF (sẽ học):**

```python
# views.py
class ProjectViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Project.objects.filter(status="active")
        serializer = ProjectSerializer(queryset, many=True)
        return Response({"data": serializer.data}, status=200)

# serializers.py
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "status"]

# Response JSON (không có template)
{
    "data": [
        {"id": 1, "name": "Project A", "status": "active"}
    ]
}
```

---

## Phần 3: Lộ Trình Học – 6 Phase

Mỗi phase dưới đây **đã có bài riêng** trong roadmap này. Bảng sau là bản đồ phase → bài;
nội dung chi tiết nằm ở file được trỏ tới, không chép lại ở đây.

| Phase | Mục tiêu | Bài đọc |
|:--:|:--|:--|
| 0 | Ôn ORM cho chắc: `filter`/lookup, `related_name`, `select_related`/`prefetch_related`, `annotate`/`Q`/`F`, `transaction.atomic()` | `02-django-core/06-orm.md` (nền tảng)<br>`focus/12-django-orm-in-api-basic.md`<br>`focus/13-django-transactions-in-api-basic.md` |
| 1 | API flow cơ bản: `request.data`, `query_params`, `Response()`, status code | `core/02-api-view-and-url-flow.md`<br>`focus/03-drf-request-response.md`<br>`focus/04-response-status-error-flow.md` |
| 2 | Serializer thay `ModelForm` | `focus/05-drf-serializers.md`<br>`focus/06-serializer-project-basic.md` |
| 3 | Views: `APIView` → `ViewSet` → `Router` → Generic | `focus/07-drf-apiview.md`<br>`focus/08-viewset-router-basic.md`<br>`focus/09-viewset-as-view-manual-mapping.md`<br>`advanced/15` → `advanced/17` |
| 4 | Permission / Authentication — ai được gọi API nào | `focus/10-authentication-permission-basic.md` |
| 5 | Pagination / Filter / Search | *Chưa có bài riêng — nội dung nằm ngay dưới* |

> **Phase 0 quan trọng nhất.** Dù làm Template hay API, ORM là nơi bạn code nhiều nhất.
> Học Serializer mà ORM chưa chắc thì sẽ tắc ở mọi API list/filter.

---

### Phase 5: Pagination / Filter / Search (chưa có bài riêng)

> **Mục tiêu:** API list thực tế luôn cần phân trang, lọc, tìm kiếm.

```python
# Request
GET /api/tasks/?page=2&page_size=10&status=active&q=bug&ordering=-created_at

# View xử lý
class TaskViewSet(GenericViewSet):
    def list(self, request):
        queryset = Task.objects.select_related("project")

        # Filter
        status = request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Search
        q = request.query_params.get("q")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

        # Ordering
        ordering = request.query_params.get("ordering", "-created_at")
        queryset = queryset.order_by(ordering)

        # Pagination (team thường có helper riêng)
        page = self.paginate_queryset(queryset)
        serializer = TaskSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
```

---

## Phần 4: Checklist Đọc Source Dự Án Thực Tế

Khi vào một module mới, **KHÔNG đọc lan man từ model**. Hãy **trace theo 1 endpoint cụ thể:**

### Ví dụ: Trace endpoint `GET /api/department/list`

```txt
Bước 1: main/urls.py
    → path("api/department/", include("F22_Department_Management.urls"))

Bước 2: F22_Department_Management/urls.py
    → path("list", views.DepartmentView.as_view({"get": "get_department_list"}))

Bước 3: views.py → class DepartmentView
    → def get_department_list(self, request, ...)
    → queryset = DepartmentInfo.objects.all()
    → serializer = DepartmentListSerializer(queryset, many=True)
    → return self._response_status_200(data_return=serializer.data)

Bước 4: serializers.py → DepartmentListSerializer
    → fields nào? read_only nào? SerializerMethodField nào?

Bước 5: models.py → DepartmentInfo
    → Field types? Quan hệ? Meta?
```

### 📋 Checklist cho mỗi endpoint

| # | Câu hỏi | Trả lời |
|:--|:--------|:--------|
| 1 | Endpoint URL? | `/api/department/list` |
| 2 | HTTP Method? | `GET` |
| 3 | Root urls.py route vào app nào? | `F22_Department_Management` |
| 4 | App urls.py gọi view nào? | `DepartmentView` |
| 5 | View kế thừa từ class nào? | `ResponseStatus` → `BaseHandleAPI` → `GenericViewSet` |
| 6 | Method nào xử lý? | `get_department_list` |
| 7 | Lấy params từ đâu? | `request.GET` / `request.data` |
| 8 | Query model nào? | `DepartmentInfo` |
| 9 | Có selectors/services không? | Có / Không |
| 10 | Có `select_related` / `prefetch_related`? | ... |
| 11 | Serializer nào? | `DepartmentListSerializer` |
| 12 | Response format? | `{"data": [...]}` |
| 13 | Error handling ở đâu? | `raise_exception=True` / try-catch |

> 💡 **Tip:** Trace xong 3-5 endpoint khác nhau (GET list, GET detail, POST create, PUT update, DELETE) → bạn sẽ nắm được pattern chung của dự án.

---

## Phần 5: Custom Base Class Của Dự Án

> **Học SAU khi đã hiểu DRF cơ bản.** Không nhảy vào đây trước.

Dự án thực tế thường bọc DRF thêm một lớp base class của team:

```txt
DRF GenericViewSet
    └── BaseHandleAPI        ← Team tự viết: helper xử lý chung
        └── ResponseStatus   ← Team tự viết: chuẩn hóa format response
            └── DepartmentView   ← View cụ thể của module
```

**Thứ tự đọc khi gặp code kiểu này:**

1. Hiểu `GenericViewSet` gốc của DRF là gì (Phase 3).
2. Mở `_base_viewset.py` → xem `BaseHandleAPI` thêm gì.
3. Mở `response_status.py` → xem `ResponseStatus` bọc response ra sao.
4. Sau đó mới đọc view cụ thể của module.

> Danh sách helper (`_response_status_200`, `ProcessData`, `pagination_list_data`,
> `get_filter_obj`...), cách trace chúng, và 3 chỗ dễ nhầm khi đọc code kiểu này
> được giải thích đầy đủ ở `focus/11-custom-response-base-class-basic.md`.

---

## Phần 6: Docker / Local Env / Swagger

> **Mục tiêu:** Tự chạy được backend local, vào Swagger test API, đọc log khi lỗi.

### Docker – Học vừa đủ

Dự án thường có 2 service chính: `mysql-server` + `api-server`.

**Các lệnh cần biết:**

```bash
# Khởi động tất cả services
docker compose up -d

# Dừng tất cả
docker compose down

# Xem log (quan trọng nhất khi debug!)
docker compose logs -f api-server
docker compose logs -f mysql-server

# Vào trong container chạy lệnh Django
docker compose exec api-server bash
python manage.py migrate
python manage.py createsuperuser
```

**Concepts Docker cần hiểu:**

| Concept | Giải thích đơn giản |
|:--------|:--------------------|
| **Image** | "Bản thiết kế" – chứa code + dependencies |
| **Container** | "Ngôi nhà" – instance đang chạy từ image |
| **Volume** | "Ổ cứng gắn ngoài" – giữ data khi container restart (MySQL data) |
| **Port mapping** | `8000:8000` – port máy host : port trong container |
| **Environment** | `.env` file – chứa DB password, SECRET_KEY... |
| **docker-compose.yml** | File định nghĩa tất cả services + quan hệ giữa chúng |

> 💡 **Tip:** Mở `docker-compose.yml` đọc trước để biết service nào phụ thuộc service nào (VD: `api-server` depends_on `mysql-server`).

### Swagger – Test API nhanh

```txt
Sau khi chạy Docker, mở: http://localhost:8000/doc/

→ Swagger UI hiển thị tất cả API endpoints
→ Click vào endpoint → Try it out → Execute
→ Xem request/response format thực tế
```

---

## Phần 7: Những Gì Tạm Hoãn (Chưa Cần Vội)

| Kiến thức | Lý do hoãn |
|:----------|:-----------|
| Django Template nâng cao | Dự án API không dùng |
| Custom template tags | Không có template |
| Context processors nâng cao | Không có template context |
| Django Admin nâng cao | Biết cơ bản là đủ |
| Docker production | Học sau khi dev ổn |
| CI/CD | DevOps lo, dev biết concept là đủ |
| Celery / Redis | Async task – học khi gặp |
| Caching | Performance – học khi cần optimize |
| Signals nâng cao | Ít dùng, dễ gây side effect |
| Testing nâng cao | Học sau khi đã code được feature |

> Không phải không quan trọng – nhưng **không phải thứ giúp đọc hiểu dự án API nhanh nhất**.

---

## Phần 8: Tổng Kết

### Sơ đồ lộ trình

```txt
                    ┌─ Bạn đang ở đây
                    ▼
╔══════════════════════════════════════════════╗
║  Phase 0: Ôn Django Core                    ║  ← NỀN TẢNG
║  settings, urls, models, migrations, apps   ║
╠══════════════════════════════════════════════╣
║  Phase 1: Ôn ORM chắc                       ║  ← NỀN TẢNG (1-2 tuần)
║  filter, lookup, related, select_related,    ║
║  prefetch_related, annotate, Q, F,           ║
║  values, values_list                         ║
╠══════════════════════════════════════════════╣
║  Phase 2: API Flow cơ bản                   ║  ← HIỂU CONCEPT (3-5 ngày)
║  request, response, status code, HTTP method ║
╠══════════════════════════════════════════════╣
║  Phase 3: Serializer                         ║  ← TRỌNG TÂM (1-2 tuần)
║  ModelSerializer, validate, fields, source,  ║
║  SerializerMethodField, many=True            ║
╠══════════════════════════════════════════════╣
║  Phase 4: APIView / ViewSet                  ║  ← ÁP DỤNG (1 tuần)
║  GenericViewSet, as_view, request.data       ║
╠══════════════════════════════════════════════╣
║  Phase 5: Permission + Pagination + Filter  ║  ← BỔ SUNG (1 tuần)
║  IsAuthenticated, query_params, ordering     ║
╠══════════════════════════════════════════════╣
║  Phase 6: Custom base class của dự án        ║  ← ĐỌC SOURCE (3-5 ngày)
║  BaseHandleAPI, ResponseStatus, helpers      ║
╠══════════════════════════════════════════════╣
║  Phase 7: Docker + Swagger                   ║  ← CHẠY THỰC TẾ (2-3 ngày)
║  compose up, logs, test API, đọc log lỗi    ║
╠══════════════════════════════════════════════╣
║  Phase 8: Trace endpoint + tự sửa API       ║  ← MỤC TIÊU CUỐI
║  Trace 3-5 endpoint → sửa 1 API đơn giản   ║
╚══════════════════════════════════════════════╝
```

### 10 Bước Dễ Nhớ

```txt
 1. Ôn Django project/app/settings/urls/models/migrations
 2. Ôn ORM thật chắc (filter, lookup, related, annotate, Q)
 3. Học Serializer như "phiên bản API của ModelForm"
 4. Học DRF ViewSet / APIView / Response / request.data
 5. Học flow:  urls.py → ViewSet → ORM/service → Serializer → JSON
 6. Đọc custom BaseHandleAPI / ResponseStatus của team
 7. Chạy Docker local + Swagger
 8. Trace từng API nhỏ (dùng checklist 13 câu hỏi)
 9. Tự sửa một API list/detail/create/update đơn giản
10. Sau đó mới học test API
```

### Chuyển tư duy – Một câu duy nhất

```txt
CŨ:  request → urls.py → view → form/model    → template → HTML Response
MỚI: request → urls.py → ViewSet → ORM/service → serializer → JSON Response
```

> **Bạn không cần học lại từ đầu.** Chỉ cần thay `forms + templates` bằng `serializers + Response`.
> Toàn bộ phần còn lại (urls, models, ORM, services) – bạn đã biết rồi.

> **Tổng thời gian ước tính:** 6-10 tuần nếu học đều đặn mỗi ngày.
> **Nguyên tắc:** Mỗi phase xong → viết 1 mini API project nhỏ để thực hành trước khi sang phase tiếp.
