# DRF Serializers: Góc nhìn từ người đã biết Django Form

Mình sẽ bám theo docs chính thức của Django REST Framework về Serializers, nhưng sẽ tiếp cận theo góc nhìn bạn đã biết `ModelForm` trong Django Template để dễ nối kiến thức cũ sang DRF.

## 1. Serializer là gì?

Trong Django Template, bạn đã quen với flow:
`request.POST -> Form/ModelForm -> is_valid() -> cleaned_data -> save() -> render/redirect`

Trong Django REST Framework, flow tương tự là:
`request.data -> Serializer -> is_valid() -> validated_data -> save() -> Response(JSON)`

Theo docs DRF, serializer có 2 nhiệm vụ chính:
1. Convert object/queryset/model instance -> Python data -> JSON response.
2. Convert request data JSON -> Python data -> validate -> create/update object.

Docs cũng nói rõ serializer trong DRF hoạt động rất giống Django Form và ModelForm; DRF cung cấp Serializer để kiểm soát output linh hoạt, và ModelSerializer như shortcut khi làm việc với model/queryset.

---

## 2. Mapping với kiến thức bạn đã biết

| Django Template | DRF |
|:---|:---|
| `forms.Form` | `serializers.Serializer` |
| `forms.ModelForm` | `serializers.ModelSerializer` |
| `request.POST` | `request.data` |
| `form.is_valid()` | `serializer.is_valid()` |
| `form.cleaned_data` | `serializer.validated_data` |
| `form.errors` | `serializer.errors` |
| `form.save()` | `serializer.save()` |
| render HTML | return JSON |

Nên bạn có thể hiểu đơn giản:
**Serializer = Form/ModelForm dành cho API**

Nhưng serializer mạnh hơn ở chỗ nó vừa xử lý input validation, vừa xử lý output JSON.

---

## 3. Có 2 loại quan trọng cần học trước

### Loại 1: Serializer

Dùng khi bạn muốn tự khai báo field thủ công.

```python
from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=["todo", "doing", "done"])
```

Nó giống:
```python
class TaskForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(required=False)
    status = forms.ChoiceField(...)
```

**Dùng Serializer khi:**
- Data không map trực tiếp với một model.
- API chỉ dùng để validate input.
- API dạng search/filter/report.
- Bạn muốn custom hoàn toàn input/output.

**Ví dụ thực tế:**
```python
class TaskFilterSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False)
    status = serializers.ChoiceField(
        choices=["todo", "doing", "done"],
        required=False
    )
    project_id = serializers.IntegerField(required=False)
```
Serializer này không dùng để save DB, chỉ dùng để validate query/filter input.

### Loại 2: ModelSerializer

Dùng khi serializer map với Django model.

**Ví dụ model:**
```python
class Project(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Serializer:**
```python
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "status", "created_at"]
```

Theo docs, `ModelSerializer` tự động tạo field dựa trên model, tự động tạo một số validator, và có sẵn implementation đơn giản cho `.create()` và `.update()`.

Nó rất giống `ModelForm`:
```python
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "status"]
```

**Khác biệt là:**
- ModelForm dùng cho HTML form.
- ModelSerializer dùng cho JSON API.

---

## 4. Serializer dùng cho output như thế nào?

Giả sử có object:
```python
project = Project.objects.get(id=1)
serializer = ProjectSerializer(project)
return Response(serializer.data)
```

Response JSON sẽ giống:
```json
{
  "id": 1,
  "name": "Website Redesign",
  "status": "doing",
  "created_at": "2026-05-15T10:00:00Z"
}
```
Đây gọi là: **Serialization** (object/model/queryset -> JSON-friendly data).

Nếu là list/queryset:
```python
projects = Project.objects.all()
serializer = ProjectSerializer(projects, many=True)
return Response(serializer.data)
```

**Điểm cần nhớ:**
- Một object -> không cần `many=True`
- Nhiều object -> cần `many=True`
- Serializer xử lý phần data phức tạp như model object/queryset; nó không bắt buộc phải bọc mọi dict response.

Ví dụ response có metadata:

```python
projects = Project.objects.all()
serializer = ProjectSerializer(projects, many=True)

return Response({
    "total_records": projects.count(),
    "data": serializer.data,
})
```

Ở đây `projects` cần serializer để thành list data trả ra. Dict chứa `total_records` và `data` đã là Python data render được nên có thể đưa thẳng vào `Response`.

Docs cũng ghi rõ khi serialize queryset/list thì truyền `many=True` vào serializer.

---

## 5. Serializer dùng cho input như thế nào?

Giả sử frontend gửi JSON:
```json
{
  "name": "New Project",
  "status": "todo"
}
```

View xử lý:
```python
serializer = ProjectSerializer(data=request.data)

if serializer.is_valid():
    project = serializer.save()
    return Response(ProjectSerializer(project).data)

return Response(serializer.errors, status=400)
```

**Flow là:**
`request.data` -> `serializer = ProjectSerializer(data=request.data)` -> `serializer.is_valid()` -> `serializer.validated_data` -> `serializer.save()` -> create object

Tương tự Django Form:
```python
form = ProjectForm(request.POST)

if form.is_valid():
    project = form.save()
```

Docs nhấn mạnh: khi deserialize data, bạn cần gọi `.is_valid()` trước khi dùng `validated_data` hoặc `.save()`; nếu lỗi thì xem `.errors`.

---

## 6. `validated_data` là gì?

Ví dụ request gửi:
```json
{
  "name": "New Project",
  "status": "todo"
}
```

Sau khi: `serializer.is_valid()`
Bạn có thể xem: `serializer.validated_data`

Nó giống `cleaned_data` của form:
`form.cleaned_data` ≈ `serializer.validated_data`

**Điểm quan trọng:**
- `request.data` là data thô từ client.
- `validated_data` là data đã qua validate.

Khi xử lý nghiệp vụ, ưu tiên dùng: `serializer.validated_data`.
Không nên lấy trực tiếp từ: `request.data["name"]` trừ khi có lý do rõ ràng.

---

## 7. `.save()` hoạt động như thế nào?

Với ModelSerializer, DRF có sẵn `.create()` và `.update()` đơn giản.

**Case tạo mới:**
```python
serializer = ProjectSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
project = serializer.save()
```
Khi không truyền instance ban đầu, `.save()` sẽ gọi `.create()`.

**Case update:**
```python
project = Project.objects.get(id=1)

serializer = ProjectSerializer(project, data=request.data)
serializer.is_valid(raise_exception=True)
project = serializer.save()
```
Khi truyền instance ban đầu, `.save()` sẽ gọi `.update()`.

Docs cũng giải thích `.save()` sẽ create instance mới hoặc update instance hiện có tùy vào việc bạn có truyền instance khi khởi tạo serializer hay không.

---

## 8. `is_valid(raise_exception=True)`

Thường trong dự án thực tế bạn sẽ thấy:
```python
serializer.is_valid(raise_exception=True)
```
Thay vì:
```python
if serializer.is_valid():
    ...
else:
    return Response(serializer.errors, status=400)
```
Vì `raise_exception=True` sẽ tự raise lỗi validation, DRF xử lý và trả HTTP 400 Bad Request mặc định.

**Ví dụ:**
```python
serializer = ProjectSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
project = serializer.save()

return Response(ProjectSerializer(project).data)
```
Trong code thực tế, đây là style phổ biến hơn.

---

## 9. Field-level validation

Dùng khi validate một field riêng lẻ.
Ví dụ task title không được quá ngắn:

```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status"]

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must have at least 3 characters.")
        return value
```

Cú pháp: `def validate_<field_name>(self, value):`

Nó giống `clean_<field_name>` trong Django Form. Docs cũng nói field-level validation trong serializer tương tự `clean_<field_name>` của Django forms.

---

## 10. Object-level validation

Dùng khi validate nhiều field cùng lúc.
Ví dụ task có `start_date` và `end_date`, yêu cầu `end_date` phải sau `start_date`.

```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "start_date", "end_date"]

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError(
                "End date must be after start date."
            )
        return data
```

Cú pháp: `def validate(self, data):`

Dùng khi rule cần nhiều field:
- `start_date` < `end_date`
- `cost_hour` > 0 nếu `status` = done
- project phải active thì mới tạo task
- deadline không được nhỏ hơn ngày hiện tại

Docs gọi đây là object-level validation, dùng `.validate()` khi cần access nhiều field cùng lúc.

---

## 11. `partial=True` dùng khi nào?

Khi update một phần object, ví dụ PATCH.

Giả sử model có: `title`, `description`, `status`, `deadline`.
Client chỉ gửi: `{"status": "done"}`

Nếu bạn viết:
```python
serializer = TaskSerializer(task, data=request.data)
serializer.is_valid(raise_exception=True) # Có thể lỗi vì thiếu field required
```

Khi update một phần, dùng:
```python
serializer = TaskSerializer(task, data=request.data, partial=True)
serializer.is_valid(raise_exception=True)
serializer.save()
```

Docs nói mặc định serializer cần đủ các field required, nhưng có thể dùng `partial=True` để cho phép partial update.

**Mapping:**
- PUT -> update toàn bộ object.
- PATCH -> update một phần object -> `partial=True`.

---

## 12. `read_only_fields`

Dùng khi field chỉ được trả ra response, không cho client gửi vào để sửa.

Ví dụ:
```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
```

**Ý nghĩa:**
- Client không được tự set `id`
- Client không được tự set `created_at`
- Client không được tự set `updated_at`

Docs cũng có shortcut `read_only_fields` để khai báo nhiều field read-only trong Meta.

---

## 13. `write_only=True`

Dùng khi field chỉ nhận input, không trả ra response.

Ví dụ password:
```python
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
```
Response sẽ không trả password. Docs cũng có ví dụ dùng `extra_kwargs = {'password': {'write_only': True}}` khi tạo user.

---

## 14. `source`

Dùng khi field trong JSON khác tên field/model attribute.
Ví dụ model Task có quan hệ project. Bạn muốn response có `project_name`:

```python
class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        source="project.name",
        read_only=True
    )

    class Meta:
        model = Task
        fields = ["id", "title", "project", "project_name"]
```

Response:
```json
{
  "id": 1,
  "title": "Fix bug",
  "project": 3,
  "project_name": "Internal Tool"
}
```

Ý nghĩa: `project_name` trong API lấy từ `task.project.name`. Đây là case rất hay gặp trong dự án thực tế.

---

## 15. Relationship trong serializer

Giả sử:
```python
class Project(models.Model):
    name = models.CharField(max_length=255)

class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
```

### Cách 1: Trả project id
```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "project"]
```
Response:
```json
{
  "id": 1,
  "title": "Fix bug",
  "project": 3
}
```
Đây là default của ModelSerializer. Theo docs, relationship như foreign key mặc định được map sang PrimaryKeyRelatedField.

### Cách 2: Trả thêm project name
```python
class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "project", "project_name"]
```
Đây là cách rất thực tế: input dùng project id, output thêm project_name cho frontend hiển thị.

### Cách 3: Nested serializer
```python
class ProjectShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]

class TaskSerializer(serializers.ModelSerializer):
    project = ProjectShortSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "project"]
```
Response:
```json
{
  "id": 1,
  "title": "Fix bug",
  "project": {
    "id": 3,
    "name": "Internal Tool"
  }
}
```

Docs nói Serializer cũng là một loại field và có thể dùng để biểu diễn nested relationship; nếu nested là list thì truyền `many=True`.

**Lưu ý quan trọng:**
- Nested read thì dễ.
- Nested write/create/update thì phức tạp hơn. Bạn phải tự viết `.create()` hoặc `.update()` để handle lưu nhiều object liên quan.

---

## 16. SerializerMethodField

Dùng khi field response cần tính toán custom.

```python
class TaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "deadline", "is_overdue"]

    def get_is_overdue(self, obj):
        return obj.deadline < timezone.now().date()
```

Cú pháp: `field_name = serializers.SerializerMethodField()` và hàm `def get_<field_name>(self, obj):`.

**Dùng khi:**
- Field không có trực tiếp trong DB.
- Cần tính toán / format dữ liệu.
- Cần check permission/user hiện tại.

Ví dụ thực tế (cần context):
```python
class TaskSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "can_edit"]

    def get_can_edit(self, obj):
        request = self.context.get("request")
        return obj.assignee == request.user
```

Muốn dùng request trong serializer thì view truyền context:
`serializer = TaskSerializer(task, context={"request": request})`

---

## 17. Nên chia serializer theo mục đích

Trong dự án thực tế, không nên lúc nào cũng dùng một serializer cho tất cả API.

Ví dụ với Task:
- `TaskListSerializer`: Dùng cho GET list (ít field, nhẹ).
- `TaskDetailSerializer`: Dùng cho GET detail (nhiều field).
- `TaskCreateSerializer`: Dùng cho POST (field input).
- `TaskUpdateSerializer`: Dùng cho PUT/PATCH (chỉ các field được phép sửa).

Tư duy thực tế: Không nên dùng một serializer có quá nhiều field cho mọi case.

---

## 18. Flow thực tế trong view

### List API
```python
class TaskViewSet(ViewSet):
    def list(self, request):
        queryset = Task.objects.select_related("project").all()
        serializer = TaskListSerializer(queryset, many=True)
        return Response({"data": serializer.data})
```
Flow: GET /tasks/ -> query Task -> serialize many=True -> return JSON

### Detail API
```python
class TaskViewSet(ViewSet):
    def retrieve(self, request, pk=None):
        task = get_object_or_404(Task.objects.select_related("project"), pk=pk)
        serializer = TaskDetailSerializer(task)
        return Response({"data": serializer.data})
```
Flow: GET /tasks/1/ -> get one task -> serialize one object -> return JSON

### Create API
```python
class TaskViewSet(ViewSet):
    def create(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskDetailSerializer(task).data, status=201)
```
Flow: POST /tasks/ -> request.data -> validate -> save/create -> return created data

### Update API
```python
class TaskViewSet(ViewSet):
    def partial_update(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response(TaskDetailSerializer(task).data)
```
Flow: PATCH /tasks/1/ -> get task -> validate partial data -> save/update -> return updated data

---

## 19. Những lỗi người mới hay gặp

**Lỗi 1: Quên many=True**
- Sai: `serializer = TaskSerializer(tasks)`
- Đúng: `serializer = TaskSerializer(tasks, many=True)`

**Lỗi 2: Dùng .data trước .is_valid()**
- Sai: `print(serializer.data)` rồi mới `serializer.is_valid()`
- Đúng: `is_valid(raise_exception=True)` rồi mới dùng `.validated_data` hoặc `.data`.

**Lỗi 3: Nhầm validated_data với data**
- `serializer.validated_data`: Dữ liệu input đã validate, dùng cho create/update/business logic.
- `serializer.data`: Dữ liệu output để trả response.

**Lỗi 4: Cho client sửa field không nên sửa**
- Ví dụ không set `read_only_fields` cho id, owner, created_at. Cần thiết lập rõ ràng.

**Lỗi 5: Nested serializer gây N+1 query**
- Nếu list task mà không `select_related("project")`, serializer lấy nested object sẽ query N lần. Serializer quyết định output, query optimization vẫn nằm ở queryset.

---

## 20. Bạn nên học serializers theo thứ tự này

1. Serializer là gì, khác gì Form/ModelForm.
2. Serializer vs ModelSerializer.
3. `serializer.data`.
4. `data=request.data`.
5. `is_valid()`.
6. `validated_data`.
7. `errors`.
8. `save()`.
9. `.create()` / `.update()`.
10. `many=True`.
11. `read_only_fields` / `write_only`.
12. `validate_<field>()`.
13. `validate()`.
14. `source`.
15. `SerializerMethodField`.
16. Nested serializer.
17. Tách List/Detail/Create/Update serializer.
