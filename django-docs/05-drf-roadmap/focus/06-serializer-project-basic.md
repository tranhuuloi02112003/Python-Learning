# Serializer Project-Style Basic

> Note: Bài này không học lại toàn bộ serializer basic. Bài này tập trung vào cách đọc serializer trong project: field nào là input, field nào là output, custom field lấy từ đâu, và serializer đang được dùng ở bước nào trong API flow.

Bài này tập trung vào cách đọc serializer trong project thực tế.

Serializer trong project không chỉ dùng để convert data đơn giản. Nó thường dùng để:

- Validate dữ liệu request.
- Map model thành JSON response.
- Ẩn field không muốn trả ra.
- Tạo field custom.
- Lấy data từ quan hệ ForeignKey.
- Xử lý `many=True`.
- Phân biệt input field và output field.

Khi join dự án, bạn sẽ gặp serializer rất nhiều.

---

## 1. Vì sao cần học serializer thêm?

Trước đó bạn đã học serializer basic, ví dụ:

```python
class TaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
```

Nhưng trong dự án thực tế, serializer thường làm nhiều việc hơn:

```text
Input từ client -> validate -> validated_data
Model object/queryset -> serializer.data -> response
```

Vì vậy cần học thêm các phần hay gặp trong project:

- `ModelSerializer`
- `fields`
- `read_only_fields`
- `write_only`
- `source`
- `SerializerMethodField`
- `many=True`
- `serializer.data`
- `serializer.errors`
- `validated_data`
- `validate_<field>()`
- `validate()`
- input serializer vs output serializer

---

## 2. Serializer nằm ở đâu trong API flow?

Một API thường có flow:

```text
Request
-> View / ViewSet
-> Serializer validate request.data
-> ORM xử lý database
-> Serializer format response data
-> Response trả về client
```

Ví dụ:

```python
def create_task(self, request):
    serializer = TaskCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return self._response_status_400_bad_request(serializer.errors)

    task = Task.objects.create(**serializer.validated_data)

    response_serializer = TaskSerializer(task)

    return self._response_status_200(response_serializer.data)
```

Trong đoạn trên có 2 loại serializer:

```text
TaskCreateSerializer: validate input
TaskSerializer: format output
```

Đây là pattern rất hay gặp trong project thật.

---

## 3. ModelSerializer

Trong project thực tế, phần lớn serializer sẽ là `ModelSerializer`.

Ví dụ model:

```python
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
```

Serializer:

```python
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_at",
        ]
```

Ý nghĩa:

- `ModelSerializer` tự tạo field dựa trên model.
- Không cần khai báo lại từng field nếu không cần custom.
- `fields` quyết định field nào được serialize.

Ví dụ response:

```json
{
  "id": 1,
  "title": "Fix bug Daily Report",
  "description": "Fix BPO task link",
  "status": "doing",
  "created_at": "2026-05-18T10:00:00Z"
}
```

---

## 4. `fields`

`fields` dùng để khai báo các field sẽ được đưa vào serializer.

```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status"]
```

Nếu model có nhiều field nhưng bạn chỉ muốn API trả ra vài field, dùng `fields`.

Ví dụ model có:

```text
id
title
description
status
created_at
updated_at
internal_note
```

Nhưng serializer chỉ khai báo:

```python
fields = ["id", "title", "status"]
```

Thì response chỉ có:

```json
{
  "id": 1,
  "title": "Task A",
  "status": "todo"
}
```

---

## 5. `read_only_fields`

`read_only_fields` là các field chỉ để trả ra, không cho client gửi lên để sửa.

Ví dụ:

```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "status", "created_at"]
        read_only_fields = ["id", "created_at"]
```

Ý nghĩa:

- `id`: server/database tự tạo.
- `created_at`: server tự tạo.
- Client không được set 2 field này.

Nếu client gửi:

```json
{
  "id": 999,
  "title": "Task A",
  "created_at": "2030-01-01"
}
```

thì `id` và `created_at` không nên được dùng để update/create.

---

## 6. `write_only`

`write_only` là field chỉ nhận input, không trả ra response.

Hay gặp với password, confirm password, token, secret key.

Ví dụ:

```python
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
```

Client gửi lên:

```json
{
  "email": "user@example.com",
  "password": "123456"
}
```

Nhưng response không trả password:

```json
{
  "email": "user@example.com"
}
```

Ý nghĩa:

```text
password dùng để validate/create user
nhưng không serialize ngược lại ra response
```

---

## 7. `source="..."`

`source` dùng để lấy data từ field khác hoặc từ quan hệ.

Ví dụ model:

```python
class Project(models.Model):
    name = models.CharField(max_length=255)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
```

Serializer:

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
  "title": "Task A",
  "project": 10,
  "project_name": "Ecommerce"
}
```

Ý nghĩa:

```text
project là id của ForeignKey
project_name lấy từ task.project.name
```

Đây là phần rất hay gặp trong project thật.

---

## 8. SerializerMethodField

`SerializerMethodField` dùng để tạo field custom bằng method trong serializer.

Ví dụ:

```python
class TaskSerializer(serializers.ModelSerializer):
    is_done = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "status", "is_done"]

    def get_is_done(self, obj):
        return obj.status == "done"
```

Response:

```json
{
  "id": 1,
  "title": "Task A",
  "status": "done",
  "is_done": true
}
```

Quy tắc:

```text
Field tên là is_done
Method xử lý phải là get_is_done(self, obj)
obj là instance model hiện tại
```

Ví dụ khác:

```python
class TaskSerializer(serializers.ModelSerializer):
    display_title = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "display_title"]

    def get_display_title(self, obj):
        return f"[{obj.status}] {obj.title}"
```

---

## 9. `many=True`

`many=True` dùng khi serialize nhiều object.

Ví dụ queryset:

```python
tasks = Task.objects.all()
serializer = TaskSerializer(tasks, many=True)
```

Response:

```json
[
  {
    "id": 1,
    "title": "Task A"
  },
  {
    "id": 2,
    "title": "Task B"
  }
]
```

Nếu chỉ serialize một object:

```python
task = Task.objects.get(id=1)
serializer = TaskSerializer(task)
```

Không dùng `many=True`.

Công thức nhớ:

```text
1 object  -> Serializer(object)
N object -> Serializer(queryset, many=True)
```

---

## 10. `serializer.data`

`serializer.data` là dữ liệu đã được serialize để trả về response.

Ví dụ:

```python
task = Task.objects.get(id=1)
serializer = TaskSerializer(task)

return self._response_status_200(serializer.data)
```

Ý nghĩa:

```text
task là Python/Django model object
serializer.data là dict/JSON-like data có thể trả về client
```

Ví dụ:

```python
serializer.data
```

có thể là:

```json
{
  "id": 1,
  "title": "Task A",
  "status": "todo"
}
```

---

## 11. `data=request.data`

Khi serializer dùng để validate input, ta truyền `data=request.data`.

Ví dụ:

```python
serializer = TaskCreateSerializer(data=request.data)
```

Ý nghĩa:

```text
request.data là dữ liệu client gửi lên
serializer kiểm tra dữ liệu đó có hợp lệ không
```

Ví dụ request body:

```json
{
  "title": "Task A",
  "status": "todo"
}
```

---

## 12. `is_valid()`

Sau khi truyền `data=request.data`, phải gọi:

```python
serializer.is_valid()
```

Ví dụ:

```python
serializer = TaskCreateSerializer(data=request.data)

if not serializer.is_valid():
    return self._response_status_400_bad_request(serializer.errors)
```

Ý nghĩa:

```text
Kiểm tra request data có đúng rule của serializer không
Nếu sai thì serializer.errors có lỗi
Nếu đúng thì serializer.validated_data có dữ liệu sạch
```

---

## 13. `serializer.errors`

Khi validate fail, lỗi nằm trong:

```python
serializer.errors
```

Ví dụ serializer:

```python
class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
```

Client gửi thiếu `title`:

```json
{
  "status": "todo"
}
```

`serializer.errors` có thể là:

```json
{
  "title": ["This field is required."]
}
```

Trong project style:

```python
if not serializer.is_valid():
    return self._response_status_400_bad_request(serializer.errors)
```

---

## 14. `validated_data`

Khi validate thành công, dữ liệu sạch nằm trong:

```python
serializer.validated_data
```

Ví dụ:

```python
serializer = TaskCreateSerializer(data=request.data)
serializer.is_valid(raise_exception=True)

data = serializer.validated_data
```

Nếu request body là:

```json
{
  "title": "Task A",
  "status": "todo"
}
```

thì:

```python
serializer.validated_data
```

là:

```python
{
    "title": "Task A",
    "status": "todo"
}
```

Dùng nó để create/update:

```python
Task.objects.create(**serializer.validated_data)
```

Không nên lấy trực tiếp `request.data` để create nếu đã dùng serializer validate.

Nên dùng:

```python
serializer.validated_data
```

thay vì:

```python
request.data
```

sau khi validate.

---

## 15. `is_valid(raise_exception=True)`

Có 2 cách xử lý validate fail.

### Cách 1: tự check

```python
serializer = TaskCreateSerializer(data=request.data)

if not serializer.is_valid():
    return self._response_status_400_bad_request(serializer.errors)
```

### Cách 2: để DRF tự raise exception

```python
serializer = TaskCreateSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
```

Nếu fail, DRF tự trả lỗi `400`.

Trong project có custom response thì nhiều team thích cách 1 hơn để response đúng format project.

Nhưng bạn sẽ gặp cả 2 kiểu.

---

## 16. `validate_<field>()`

Dùng để validate riêng một field.

Ví dụ muốn title không được quá ngắn:

```python
class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    status = serializers.CharField()

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must have at least 3 characters."
            )

        return value
```

Quy tắc:

```text
validate_title -> validate field title
validate_status -> validate field status
```

`value` là giá trị của field đó.

---

## 17. `validate()`

Dùng để validate liên quan nhiều field với nhau.

Ví dụ:

```python
class TaskUpdateSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError(
                "End date must be greater than start date."
            )

        return attrs
```

Ý nghĩa:

```text
validate_<field>() kiểm tra từng field riêng
validate() kiểm tra logic liên quan nhiều field
```

Ví dụ khác:

```python
class ChangeStatusSerializer(serializers.Serializer):
    current_status = serializers.CharField()
    next_status = serializers.CharField()

    def validate(self, attrs):
        if attrs["current_status"] == "done":
            raise serializers.ValidationError(
                "Done task cannot change status."
            )

        return attrs
```

---

## 18. Input serializer và output serializer

Trong project thật, một API có thể dùng 2 serializer khác nhau.

Ví dụ create task:

```python
class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
```

Dùng để nhận input.

Sau khi create xong, trả output bằng serializer khác:

```python
class TaskDetailSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        source="project.name",
        read_only=True
    )

    class Meta:
        model = Task
        fields = ["id", "title", "description", "project_name", "created_at"]
```

View:

```python
def create_task(self, request):
    input_serializer = TaskCreateSerializer(data=request.data)

    if not input_serializer.is_valid():
        return self._response_status_400_bad_request(input_serializer.errors)

    task = Task.objects.create(**input_serializer.validated_data)

    output_serializer = TaskDetailSerializer(task)

    return self._response_status_200(output_serializer.data)
```

Ý nghĩa:

```text
Input serializer: kiểm tra dữ liệu client gửi lên
Output serializer: format dữ liệu trả về client
```

Đây là pattern rất đáng nhớ.

---

## 19. Ví dụ gần với project thực tế

Model:

```python
class Project(models.Model):
    name = models.CharField(max_length=255)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    cost_hour = models.IntegerField(default=0)
```

Serializer nhận input:

```python
class TaskCreateSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    title = serializers.CharField()
    status = serializers.CharField(required=False)

    def validate_title(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Title is required.")

        return value
```

Serializer trả output:

```python
class TaskResponseSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(
        source="project.name",
        read_only=True
    )

    can_assess = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "cost_hour",
            "project_name",
            "can_assess",
        ]

    def get_can_assess(self, obj):
        return obj.cost_hour > 0
```

View:

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    def create_task(self, request):
        serializer = TaskCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return self._response_status_400_bad_request(serializer.errors)

        data = serializer.validated_data

        project = Project.objects.get(id=data["project_id"])

        task = Task.objects.create(
            project=project,
            title=data["title"],
            status=data.get("status", "todo"),
        )

        response_serializer = TaskResponseSerializer(task)

        return self._response_status_200(response_serializer.data)
```

Flow:

```text
request.data
-> TaskCreateSerializer validate
-> validated_data
-> ORM create Task
-> TaskResponseSerializer format output
-> _response_status_200
```

---

## 20. Cách đọc serializer khi vào dự án

Khi gặp serializer, đọc theo thứ tự này:

1. Serializer kế thừa gì? `Serializer` hay `ModelSerializer`?
2. Nếu là `ModelSerializer`: model là model nào?
3. `fields` gồm field nào?
4. Có `read_only_fields` không?
5. Có `write_only` field không?
6. Có `source="..."` không? Nếu có thì field đó lấy từ đâu?
7. Có `SerializerMethodField` không? Nếu có thì tìm method `get_<field_name>()`.
8. Có `validate_<field>()` không?
9. Có `validate()` không?
10. Serializer đang dùng cho input hay output?

Đây là checklist quan trọng nhất.

---

## 21. Chỗ dễ nhầm

### Nhầm 1: `serializer.data` và `validated_data`

`serializer.data` dùng để trả response.

```python
return self._response_status_200(serializer.data)
```

`validated_data` dùng sau khi validate input thành công.

```python
Task.objects.create(**serializer.validated_data)
```

Nhớ nhanh:

```text
serializer.data -> output
serializer.validated_data -> input đã validate
```

### Nhầm 2: Truyền object và truyền data

Serialize object để trả response:

```python
serializer = TaskSerializer(task)
```

Validate request input:

```python
serializer = TaskCreateSerializer(data=request.data)
```

Nhớ nhanh:

```text
TaskSerializer(task)           -> output
TaskCreateSerializer(data=...) -> input
```

### Nhầm 3: Quên `many=True`

Sai:

```python
tasks = Task.objects.all()
serializer = TaskSerializer(tasks)
```

Đúng:

```python
tasks = Task.objects.all()
serializer = TaskSerializer(tasks, many=True)
```

Vì `tasks` là nhiều object.

### Nhầm 4: Không biết `obj` trong `get_xxx(self, obj)` là gì

Ví dụ:

```python
def get_can_assess(self, obj):
    return obj.cost_hour > 0
```

`obj` chính là object hiện tại đang được serialize.

Nếu serialize 1 task:

```python
TaskResponseSerializer(task)
```

thì `obj` là `task`.

Nếu serialize nhiều task:

```python
TaskResponseSerializer(tasks, many=True)
```

thì DRF sẽ gọi `get_can_assess()` cho từng task.

### Nhầm 5: Không biết `source="project.name"` nghĩa là gì

```python
project_name = serializers.CharField(
    source="project.name",
    read_only=True
)
```

Nghĩa là:

```text
field project_name trong response
lấy data từ obj.project.name
```

Không phải trong model có field `project_name`.

---

## 22. Công thức nhớ nhanh

`ModelSerializer`:

```text
Model object -> JSON-like data
```

`data=request.data`:

```text
Client input -> validate -> validated_data
```

`serializer.data`:

```text
Dữ liệu để trả response
```

`validated_data`:

```text
Dữ liệu đã kiểm tra, dùng để create/update
```

`SerializerMethodField`:

```text
Field custom, lấy data từ get_<field_name>()
```

`source`:

```text
Lấy data từ field khác hoặc quan hệ khác
```

`many=True`:

```text
Dùng khi serialize danh sách/queryset
```

---

## 23. Kết luận

Trong project thực tế, serializer thường dùng cho 2 việc chính:

1. Validate input từ `request.data`.
2. Format output trả về response.

Bạn chưa cần học sâu tất cả serializer advanced.

Trước mắt chỉ cần nắm chắc:

- `ModelSerializer`
- `fields`
- `read_only_fields`
- `write_only`
- `source`
- `SerializerMethodField`
- `many=True`
- `serializer.data`
- `serializer.errors`
- `validated_data`
- `validate_<field>()`
- `validate()`
- input serializer vs output serializer

Khi đọc API thật, nhớ flow:

```text
request.data
-> input serializer
-> is_valid()
-> validated_data
-> ORM/service xử lý
-> output serializer
-> serializer.data
-> custom response
```
