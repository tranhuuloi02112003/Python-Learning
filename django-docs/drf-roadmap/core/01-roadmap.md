# 🗺️ Roadmap: Django Template → Django REST Framework → Dự Án Thực Tế

> **Mục tiêu:** Chuyển từ Django Template developer → có thể join dự án API backend thực tế.
> **Điểm xuất phát:** Đã hoàn thành dự án Django Template (TaskLog PRO).

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

### Phase 0: Ôn Lại ORM Chắc ⭐⭐⭐

> **Đây là phần QUAN TRỌNG NHẤT.** Dù Template hay DRF, ORM là nơi bạn sẽ code nhiều nhất.

**Nhóm 1 – Query cơ bản (đã biết, ôn lại):**

```python
Model.objects.all()
Model.objects.filter(status="active")
Model.objects.exclude(status="archived")
Model.objects.get(id=1)                    # Raise DoesNotExist nếu không có
Model.objects.filter(id=999).first()       # Trả None nếu không có
```

**Nhóm 2 – Lookup nâng cao:**

```python
# Pattern: field__lookup=value
Task.objects.filter(title__icontains="bug")          # LIKE '%bug%'
Task.objects.filter(created_at__gte=start_date)      # >= ngày
Task.objects.filter(status__in=["active", "pending"]) # IN list

# Pattern: relation__field__lookup=value (query xuyên bảng)
Task.objects.filter(project__name__icontains="web")   # Query qua ForeignKey
```

**Nhóm 3 – Quan hệ Model:**

```python
# ForeignKey + related_name
class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)

# Chiều thuận:  task.project.name
# Chiều ngược:  project.tasks.all()
# Trong annotate: Count("tasks")  ← dùng related_name
```

**Nhóm 4 – Tối ưu query (N+1 problem):**

```python
# ForeignKey / OneToOne → select_related (SQL JOIN, 1 query)
Task.objects.select_related("project")

# ManyToMany / Reverse FK → prefetch_related (2 query riêng, ghép trong Python)
Project.objects.prefetch_related("tasks")
```

**Nhóm 5 – Annotate / Q / F (HAY GẶP trong API list/filter/search):**

```python
from django.db.models import Count, Q, F

# Thêm field tính toán tạm
Project.objects.annotate(task_count=Count("tasks"))

# OR condition
Task.objects.filter(Q(title__icontains="bug") | Q(description__icontains="bug"))

# Update dựa trên giá trị hiện tại (không kéo về Python)
Task.objects.filter(id=1).update(priority=F("priority") + 1)
```

**Nhóm 6 – Transaction khi write API:**

```python
from django.db import transaction

with transaction.atomic():
    project.save()
    Task.objects.bulk_create(new_tasks)
```

Khi một API create/update nhiều record liên quan nhau, đọc thêm:
`focus/13-django-transactions-in-api-basic.md`.

---

### Phase 1: API Flow Cơ Bản

> **Mục tiêu:** Hiểu API nhận gì, trả gì.

**Học:**

| Concept | Ý nghĩa |
|:--------|:---------|
| HTTP Methods | `GET` (đọc), `POST` (tạo), `PUT` (update toàn bộ), `PATCH` (update 1 phần), `DELETE` (xóa) |
| `request.data` | Body data (thay `request.POST`) – DRF tự parse JSON |
| `request.query_params` | URL params (giống `request.GET`) |
| `Response(data, status)` | Trả JSON + HTTP status code |
| Status codes | `200` OK, `201` Created, `400` Bad Request, `404` Not Found, `500` Server Error |

**Ví dụ nhỏ nhất:**

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloView(APIView):
    def get(self, request):
        return Response(
            {"message": "Hello from DRF!"},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        name = request.data.get("name")        # Thay request.POST.get("name")
        return Response(
            {"message": f"Created: {name}"},
            status=status.HTTP_201_CREATED
        )
```

---

### Phase 2: Serializer

> **Mục tiêu:** Thay thế `ModelForm`. Validate data + convert Model ↔ JSON.

**Mapping tư duy từ ModelForm:**

```python
# ── ModelForm (đã biết) ──
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "status", "project"]

# form.is_valid() → validate
# form.save()     → lưu vào DB
# form.errors     → lỗi validation

# ── Serializer (sẽ học) ──
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status", "project"]
        read_only_fields = ["id"]

# serializer.is_valid()  → validate (GIỐNG)
# serializer.save()      → lưu vào DB (GIỐNG)
# serializer.errors      → lỗi validation (GIỐNG)
# serializer.data        → dict/JSON output (MỚI – ModelForm không có)
```

**Các khái niệm cần học:**

```python
class TaskSerializer(serializers.ModelSerializer):
    # SerializerMethodField – field tính toán custom
    project_name = serializers.SerializerMethodField()

    # Source – lấy field từ quan hệ
    owner_email = serializers.CharField(source="owner.email", read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "project", "project_name", "owner_email", "status"]
        read_only_fields = ["id"]                # Không cho update qua API

    def get_project_name(self, obj):
        """Hàm cho SerializerMethodField – tên = get_<field_name>"""
        return obj.project.name if obj.project else None

    def validate_title(self, value):
        """Validate từng field – giống clean_<field>() trong ModelForm"""
        if len(value) < 3:
            raise serializers.ValidationError("Title phải >= 3 ký tự")
        return value

    def validate(self, data):
        """Validate toàn bộ – giống clean() trong ModelForm"""
        if data.get("status") == "done" and not data.get("project"):
            raise serializers.ValidationError("Task done phải có project")
        return data
```

**Sử dụng trong view:**

```python
# Serialize (Model → JSON) – khi GET
serializer = TaskSerializer(task)                    # 1 object
serializer = TaskSerializer(queryset, many=True)     # nhiều objects
return Response(serializer.data)

# Deserialize (JSON → Model) – khi POST/PUT
serializer = TaskSerializer(data=request.data)       # Tạo mới
serializer = TaskSerializer(task, data=request.data) # Update
if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=201)
return Response(serializer.errors, status=400)
```

---

### Phase 3: Views – APIView / ViewSet

> **Mục tiêu:** Hiểu các kiểu view trong DRF và cách routing.

**Từ đơn giản → phức tạp:**

```txt
APIView        → Tự viết get(), post(), put(), delete()
                 Giống FBV nhưng dạng class.

GenericAPIView → Thêm queryset, serializer_class, lookup_field
                 Có sẵn get_queryset(), get_object()...

ViewSet        → Nhóm nhiều action vào 1 class
                 Dùng .as_view({"get": "list", "post": "create"})

ModelViewSet   → ViewSet + tự động CRUD đầy đủ
                 list, create, retrieve, update, destroy có sẵn
```

**Ví dụ ViewSet (hay gặp trong dự án thực tế):**

```python
# views.py
class TaskViewSet(GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        """GET /api/tasks/"""
        queryset = self.get_queryset().select_related("project")
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        """POST /api/tasks/"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=201)

# urls.py
urlpatterns = [
    path("list", TaskViewSet.as_view({"get": "list"})),
    path("create", TaskViewSet.as_view({"post": "create"})),
]
```

**Dự án thực tế thường dùng custom base class:**

```python
# Team tự viết base class bọc lại DRF
class TaskView(ResponseStatus):                      # ← Custom base class
    def get_task_list(self, request, *args, **kwargs):
        queryset = Task.objects.all()
        serializer = TaskListSerializer(queryset, many=True)
        return self._response_status_200(data_return=serializer.data)  # ← Custom response

# ResponseStatus → kế thừa từ BaseHandleAPI → kế thừa từ GenericViewSet
# Bản chất vẫn là DRF, chỉ bọc thêm helper
```

> ⚠️ **Thứ tự học:** Hiểu `GenericViewSet` trước → rồi mới đọc custom base class của team.

---

### Phase 4: Permission / Authentication

> **Mục tiêu:** Hiểu ai được gọi API nào.

```python
from rest_framework.permissions import IsAuthenticated, AllowAny

class TaskViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]     # Phải login mới gọi được

    def list(self, request, *args, **kwargs):
        user = request.user                    # User hiện tại (từ token)
        queryset = Task.objects.filter(owner=user)
        ...
```

**Các câu hỏi hay gặp khi debug:**
- `request.user` là ai? → Check authentication
- User có quyền gọi API này không? → Check `permission_classes`
- API trả `401` hay `403`? → `401` = chưa login, `403` = login rồi nhưng không có quyền

---

### Phase 5: Pagination / Filter / Search

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

Dự án thực tế thường có custom base class bọc lại DRF:

```txt
__Common/viewsets/_base_viewset.py    → BaseHandleAPI (kế thừa GenericViewSet)
__Common/viewsets/response_status.py  → ResponseStatus (kế thừa BaseHandleAPI)
```

**Chuỗi kế thừa:**

```txt
DRF GenericViewSet
    └── BaseHandleAPI        ← Team tự viết: thêm helper xử lý chung
        └── ResponseStatus   ← Team tự viết: chuẩn hóa response format
            └── DepartmentView   ← View cụ thể của module
```

**Các helper cần hiểu:**

| Helper | Chức năng |
|:-------|:----------|
| `_response_status_200(data_return=...)` | Trả response thành công chuẩn |
| `_response_status_400_bad_request(...)` | Trả response lỗi validation |
| `ProcessData` | Xử lý/transform data trước khi trả |
| `pagination_list_data(...)` | Phân trang kết quả list |
| `get_filter_obj(...)` | Lọc queryset theo query params |

**Thứ tự đọc:**
1. Hiểu `GenericViewSet` gốc của DRF là gì
2. Mở `_base_viewset.py` → xem `BaseHandleAPI` thêm gì
3. Mở `response_status.py` → xem `ResponseStatus` bọc response như nào
4. Sau đó mới đọc view cụ thể của module

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
