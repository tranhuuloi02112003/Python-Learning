# Django ORM Trong API Basic

Bài này tập trung vào cách đọc ORM trong API thực tế.

Khi đọc API trong project, phần khó thường không nằm ở:

- APIView
- ViewSet
- Response
- Serializer

mà nằm ở đoạn query database:

```python
tasks = Task.objects.filter(
    project_id=project_id,
    status="doing",
    assignee=request.user,
)
```

Vì vậy bạn cần học ORM ở mức đọc hiểu flow API, chưa cần học query nâng cao.

---

## 1. Vì sao cần học ORM trong API?

API thực tế thường có flow:

```text
URL
-> ViewSet method
-> Serializer validate input
-> ORM query database
-> Serializer format output
-> Response
```

Ví dụ:

```python
def get_tasks(self, request):
    tasks = Task.objects.filter(status="doing")

    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

Trong đoạn này:

```python
Task.objects.filter(status="doing")
```

là ORM query.

---

## 2. `objects`

Trong Django, mỗi model thường có `.objects` để query database.

Ví dụ model:

```python
class Task(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
```

Query:

```python
Task.objects.all()
```

Hiểu đơn giản:

```text
Task    -> model/table
objects -> manager để query
all()   -> lấy tất cả record
```

---

## 3. `all()`

Dùng để lấy tất cả object.

```python
tasks = Task.objects.all()
```

Tương đương ý nghĩa:

```text
Lấy toàn bộ task trong database
```

Trong API:

```python
def get_tasks(self, request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

Lưu ý: `all()` có thể lấy quá nhiều data nếu table lớn. Nhưng ở mức basic, bạn chỉ cần hiểu nó lấy toàn bộ record.

---

## 4. `filter()`

`filter()` dùng để lấy danh sách object thỏa điều kiện.

```python
tasks = Task.objects.filter(status="doing")
```

Ý nghĩa:

```text
Lấy các task có status = doing
```

Ví dụ nhiều điều kiện:

```python
tasks = Task.objects.filter(
    status="doing",
    project_id=project_id,
)
```

Ý nghĩa:

```text
Lấy task có status = doing
và thuộc project_id truyền vào
```

Trong API:

```python
def get_project_tasks(self, request, project_id=None):
    tasks = Task.objects.filter(project_id=project_id)

    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

---

## 5. `get()`

`get()` dùng để lấy đúng một object.

```python
task = Task.objects.get(id=task_id)
```

Ý nghĩa:

```text
Lấy task có id = task_id
```

Nhưng `get()` có rủi ro:

```text
Không có object -> báo lỗi DoesNotExist
Có nhiều object -> báo lỗi MultipleObjectsReturned
```

Ví dụ:

```python
def get_task_detail(self, request, task_id=None):
    task = Task.objects.get(id=task_id)

    serializer = TaskSerializer(task)

    return self._response_status_200(serializer.data)
```

Nếu task không tồn tại, API có thể bị lỗi `500` nếu không handle.

---

## 6. Cách an toàn hơn với `get()`

Có thể dùng `try/except`:

```python
def get_task_detail(self, request, task_id=None):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return self._response_status_404_not_found("Task not found")

    serializer = TaskSerializer(task)

    return self._response_status_200(serializer.data)
```

Flow:

```text
Tìm task theo id
Nếu không có -> trả 404
Nếu có -> serialize data -> trả 200
```

---

## 7. `filter().first()`

Một cách khác hay gặp là:

```python
task = Task.objects.filter(id=task_id).first()
```

Nếu không có task, kết quả là `None`, không raise exception.

Ví dụ:

```python
def get_task_detail(self, request, task_id=None):
    task = Task.objects.filter(id=task_id).first()

    if not task:
        return self._response_status_404_not_found("Task not found")

    serializer = TaskSerializer(task)

    return self._response_status_200(serializer.data)
```

So sánh nhanh:

```text
get()
-> Không có data thì raise lỗi

filter().first()
-> Không có data thì trả None
```

Khi mới đọc project, bạn sẽ gặp cả hai kiểu.

---

## 8. `exists()`

`exists()` dùng để kiểm tra có data hay không.

```python
has_task = Task.objects.filter(status="doing").exists()
```

Ý nghĩa:

```text
Có task nào status = doing không?
```

Ví dụ trong API:

```python
def create_task(self, request):
    title = request.data.get("title")

    is_exists = Task.objects.filter(title=title).exists()

    if is_exists:
        return self._response_status_400_bad_request(
            "Task title already exists"
        )

    task = Task.objects.create(title=title)

    serializer = TaskSerializer(task)

    return self._response_status_200(serializer.data)
```

Flow:

```text
Check title đã tồn tại chưa
Nếu có -> trả 400
Nếu chưa -> tạo task
```

---

## 9. `exclude()`

`exclude()` dùng để loại trừ điều kiện.

```python
tasks = Task.objects.exclude(status="done")
```

Ý nghĩa:

```text
Lấy các task có status khác done
```

Ví dụ:

```python
tasks = Task.objects.filter(project_id=project_id).exclude(status="done")
```

Ý nghĩa:

```text
Lấy task thuộc project này
nhưng loại bỏ task đã done
```

---

## 10. `order_by()`

`order_by()` dùng để sắp xếp.

```python
tasks = Task.objects.order_by("created_at")
```

Ý nghĩa:

```text
Sắp xếp tăng dần theo created_at
```

Sắp xếp giảm dần:

```python
tasks = Task.objects.order_by("-created_at")
```

Dấu `-` nghĩa là descending.

Ví dụ:

```python
def get_tasks(self, request):
    tasks = Task.objects.filter(
        status="doing"
    ).order_by("-created_at")

    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

Ý nghĩa:

```text
Lấy task đang doing
sắp xếp task mới nhất lên trước
```

---

## 11. Query theo URL param

Ví dụ URL:

```python
path(
    "projects/<int:project_id>/tasks/",
    TaskViewSet.as_view({
        "get": "get_project_tasks",
    })
)
```

View:

```python
def get_project_tasks(self, request, project_id=None):
    tasks = Task.objects.filter(project_id=project_id)

    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

Request:

```text
GET /projects/10/tasks/
```

Flow:

```text
project_id = 10
Task.objects.filter(project_id=10)
serialize tasks
return response
```

Đây là flow rất hay gặp.

---

## 12. Query theo `request.user`

Trong API thực tế, nhiều query sẽ lọc theo user hiện tại.

Ví dụ:

```python
tasks = Task.objects.filter(assignee=request.user)
```

Ý nghĩa:

```text
Lấy task được assign cho user đang login
```

Ví dụ API:

```python
def get_my_tasks(self, request):
    tasks = Task.objects.filter(
        assignee=request.user
    ).order_by("-created_at")

    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

Flow:

```text
Lấy user đang gọi API
Query task theo user đó
Trả danh sách task của user
```

Khi đọc project, cứ thấy `request.user` trong query thì hiểu là data đang phụ thuộc vào user đang login.

---

## 13. Query theo query params

Client có thể gọi API dạng:

```text
GET /tasks/?status=doing
```

Trong view:

```python
status_param = request.query_params.get("status")
```

Ví dụ:

```python
def get_tasks(self, request):
    status_param = request.query_params.get("status")

    tasks = Task.objects.all()

    if status_param:
        tasks = tasks.filter(status=status_param)

    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

Flow:

```text
Nếu client truyền ?status=doing
-> lọc task theo status

Nếu không truyền status
-> lấy tất cả task
```

---

## 14. Chain query

Django ORM cho phép nối nhiều query lại.

```python
tasks = Task.objects.filter(
    project_id=project_id
).exclude(
    status="done"
).order_by(
    "-created_at"
)
```

Đọc theo thứ tự:

```text
Lấy task theo project_id
Loại task status = done
Sắp xếp mới nhất trước
```

Trong project thật, bạn sẽ gặp nhiều đoạn chain như vậy.

---

## 15. `Q()` cơ bản

`Q()` dùng khi cần điều kiện `OR` hoặc điều kiện phức tạp.

Bình thường:

```python
Task.objects.filter(status="todo", assignee=request.user)
```

nghĩa là:

```text
status = todo AND assignee = request.user
```

Nếu muốn `OR`:

```python
from django.db.models import Q

tasks = Task.objects.filter(
    Q(status="todo") | Q(status="doing")
)
```

Ý nghĩa:

```text
Lấy task có status = todo
hoặc status = doing
```

Ví dụ search:

```python
tasks = Task.objects.filter(
    Q(title__icontains=keyword) |
    Q(description__icontains=keyword)
)
```

Ý nghĩa:

```text
Tìm task có title chứa keyword
hoặc description chứa keyword
```

---

## 16. Lookup cơ bản: `__icontains`, `__in`, `__gte`, `__lte`

### `__icontains`

Tìm gần đúng, không phân biệt hoa thường nhiều trường hợp.

```python
tasks = Task.objects.filter(title__icontains="bug")
```

Ý nghĩa:

```text
Lấy task có title chứa chữ bug
```

### `__in`

Lọc trong danh sách.

```python
tasks = Task.objects.filter(status__in=["todo", "doing"])
```

Ý nghĩa:

```text
Lấy task có status là todo hoặc doing
```

### `__gte`

Greater than or equal.

```python
tasks = Task.objects.filter(cost_hour__gte=1)
```

Ý nghĩa:

```text
Lấy task có cost_hour >= 1
```

### `__lte`

Less than or equal.

```python
tasks = Task.objects.filter(cost_hour__lte=8)
```

Ý nghĩa:

```text
Lấy task có cost_hour <= 8
```

---

## 17. Query qua ForeignKey

Ví dụ model:

```python
class Project(models.Model):
    name = models.CharField(max_length=255)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
```

Lọc theo project id:

```python
tasks = Task.objects.filter(project_id=project_id)
```

Lọc theo field của project:

```python
tasks = Task.objects.filter(project__name="Ecommerce")
```

Ý nghĩa:

```text
Task liên kết tới Project
lọc các task có project.name = Ecommerce
```

Dấu `__` dùng để đi qua quan hệ.

---

## 18. `select_related()` cơ bản

Khi model có ForeignKey, ví dụ:

```python
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
```

Nếu trong serializer có:

```python
project_name = serializers.CharField(
    source="project.name",
    read_only=True
)
```

thì code sẽ cần đọc `task.project.name`.

Khi đó có thể dùng:

```python
tasks = Task.objects.select_related("project").all()
```

Ý nghĩa đơn giản:

```text
Lấy task kèm project luôn
Giảm số query khi truy cập task.project
```

Ví dụ:

```python
def get_tasks(self, request):
    tasks = Task.objects.select_related("project").all()

    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

Ở mức join project, bạn chỉ cần hiểu:

```text
select_related dùng cho ForeignKey / OneToOne
giúp lấy object liên quan hiệu quả hơn
```

Chưa cần học tối ưu sâu.

---

## 19. `prefetch_related()` cơ bản

`prefetch_related()` thường dùng cho quan hệ nhiều object, như ManyToMany hoặc reverse ForeignKey.

Ví dụ:

```python
class Project(models.Model):
    name = models.CharField(max_length=255)


class Task(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="tasks",
        on_delete=models.CASCADE
    )
```

Nếu lấy project và muốn lấy các task của project:

```python
projects = Project.objects.prefetch_related("tasks").all()
```

Ý nghĩa đơn giản:

```text
Lấy project
và chuẩn bị sẵn danh sách tasks liên quan
```

Ở mức basic, nhớ:

```text
select_related -> hay dùng cho ForeignKey từ object hiện tại đi tới 1 object khác
prefetch_related -> hay dùng cho quan hệ nhiều object
```

---

## 20. `create()`

`create()` dùng để tạo object mới.

```python
task = Task.objects.create(
    title="Fix bug",
    status="todo",
)
```

Trong API:

```python
def create_task(self, request):
    serializer = TaskCreateSerializer(data=request.data)

    if not serializer.is_valid():
        return self._response_status_400_bad_request(serializer.errors)

    task = Task.objects.create(**serializer.validated_data)

    response_serializer = TaskSerializer(task)

    return self._response_status_200(response_serializer.data)
```

Flow:

```text
Validate input
Lấy validated_data
Create object trong database
Serialize object vừa tạo
Return response
```

---

## 21. `save()`

`save()` dùng để lưu thay đổi object.

```python
task = Task.objects.get(id=task_id)
task.status = "done"
task.save()
```

Trong API:

```python
def mark_done(self, request, task_id=None):
    task = Task.objects.filter(id=task_id).first()

    if not task:
        return self._response_status_404_not_found("Task not found")

    task.status = "done"
    task.save()

    serializer = TaskSerializer(task)

    return self._response_status_200(serializer.data)
```

Flow:

```text
Tìm task
Nếu không có -> 404
Nếu có -> đổi status
save()
return data mới
```

---

## 22. `delete()`

`delete()` dùng để xóa object.

```python
task.delete()
```

Ví dụ:

```python
def delete_task(self, request, task_id=None):
    task = Task.objects.filter(id=task_id).first()

    if not task:
        return self._response_status_404_not_found("Task not found")

    task.delete()

    return self._response_status_200({
        "message": "Task deleted"
    })
```

---

## 23. Ví dụ API gần với project thực tế

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    def get_tasks(self, request):
        status_param = request.query_params.get("status")
        keyword = request.query_params.get("keyword")

        tasks = Task.objects.select_related("project").filter(
            assignee=request.user
        )

        if status_param:
            tasks = tasks.filter(status=status_param)

        if keyword:
            tasks = tasks.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword)
            )

        tasks = tasks.order_by("-created_at")

        serializer = TaskSerializer(tasks, many=True)

        return self._response_status_200(serializer.data)
```

Đọc flow:

```text
Lấy status từ query params
Lấy keyword từ query params
Query task của user đang login
Nếu có status -> lọc thêm status
Nếu có keyword -> search title/description
Sắp xếp task mới nhất trước
Serialize danh sách
Return response 200
```

Đây là kiểu API rất thực tế.

---

## 24. Cách đọc ORM khi vào dự án

Khi gặp đoạn query, đọc theo thứ tự:

1. Model nào đang được query? `Task.objects`, `Project.objects`, `User.objects`?
2. Query lấy một object hay nhiều object? `get()`/`first()` -> một object, `filter()`/`all()` -> nhiều object.
3. Điều kiện lọc là gì? `status`, `project_id`, `request.user`, `role`?
4. Có query params không? `request.query_params.get(...)`
5. Có URL param không? `project_id`, `task_id`, `pk`?
6. Có đi qua quan hệ không? `project__name`, `user__email`?
7. Có sắp xếp không? `order_by(...)`
8. Có `select_related`/`prefetch_related` không? Nếu có, thường là để tối ưu query relation.

---

## 25. Chỗ dễ nhầm

### Nhầm 1: `filter()` trả về nhiều object

```python
tasks = Task.objects.filter(status="doing")
```

Dù chỉ có một task phù hợp, `filter()` vẫn trả về queryset.

Muốn lấy object đầu tiên:

```python
task = Task.objects.filter(status="doing").first()
```

### Nhầm 2: `get()` có thể làm API lỗi nếu không bắt exception

```python
task = Task.objects.get(id=task_id)
```

Nếu không có task, sẽ lỗi.

An toàn hơn:

```python
task = Task.objects.filter(id=task_id).first()

if not task:
    return self._response_status_404_not_found("Task not found")
```

### Nhầm 3: `project_id` và `project__id`

Hai cách này thường cùng ý nghĩa khi lọc ForeignKey theo id:

```python
Task.objects.filter(project_id=10)
```

và:

```python
Task.objects.filter(project__id=10)
```

Nhưng `project_id` ngắn hơn và hay dùng hơn.

### Nhầm 4: `serializer = TaskSerializer(tasks)` thiếu `many=True`

Nếu `tasks` là queryset, phải dùng:

```python
serializer = TaskSerializer(tasks, many=True)
```

---

## 26. Công thức nhớ nhanh

`all()`:

```text
lấy tất cả
```

`filter()`:

```text
lấy nhiều object theo điều kiện
```

`get()`:

```text
lấy đúng một object, không có thì lỗi
```

`first()`:

```text
lấy object đầu tiên, không có thì None
```

`exists()`:

```text
kiểm tra có tồn tại không
```

`exclude()`:

```text
loại trừ điều kiện
```

`order_by("-created_at")`:

```text
sắp xếp mới nhất trước
```

`Q()`:

```text
dùng cho OR/search phức tạp
```

`select_related()`:

```text
tối ưu ForeignKey/OneToOne
```

`prefetch_related()`:

```text
tối ưu quan hệ nhiều object
```

---

## 27. Kết luận

Ở mức join dự án, bạn chưa cần học ORM quá sâu.

Trước mắt cần đọc được:

- `Task.objects.filter(...)`
- `Task.objects.get(...)`
- `Task.objects.filter(...).first()`
- `Task.objects.filter(...).exists()`
- `Task.objects.exclude(...)`
- `Task.objects.order_by(...)`
- `Task.objects.select_related(...)`
- `Task.objects.prefetch_related(...)`
- `Q(...)`

Và hiểu ORM trong API flow:

```text
request data / params
-> ORM query
-> serializer
-> response
```

---

## 28. QuerySet (lazy evaluation)

Trong Django, **QuerySet** thường là “câu query chưa chạy ngay”.

Ví dụ:

```python
queryset = Employee.objects.filter(is_active=True)
```

Lúc này Django mới **chuẩn bị SQL**, chưa lấy data thật từ DB.
Data chỉ được lấy khi bạn “ép chạy query”, ví dụ:

```python
list(queryset)
queryset.count()
queryset[0:10]
```

Trong list API, flow hay gặp là:

```text
filter -> sort -> pagination -> build response
```

Lý do: filter/sort/pagination chạy ở DB thường nhẹ hơn là kéo hết data về Python rồi mới xử lý.

---

## 29. `annotate()`

`annotate()` dùng để **tạo field tạm** ngay trong query.

Ví dụ:

```python
from django.db.models import F

Employee.objects.annotate(
    display_name=F("account_name")
)
```

Sau đó mỗi `employee` trong queryset sẽ có thêm field tạm:

```python
employee.display_name
```

Trong case thực tế, bạn sẽ gặp kiểu:

```text
resolved_experience_months = ...
```

Đây là field tạm để DB có thể sort/filter theo “experience đã resolve”.

---

## 30. `F()`

`F("field_name")` là **tham chiếu tới cột** trong DB (làm toán trên từng row trong DB).

Ví dụ:

```python
from django.db.models import F

Employee.objects.annotate(
    next_month=F("month_of_work") + 1
)
```

Ý nghĩa:

```text
next_month = month_of_work + 1 (cho từng row)
```

---

## 31. `Value()`

`Value(...)` là **giá trị cố định** đưa vào query.

Ví dụ:

```python
from django.db.models import Value

Employee.objects.annotate(
    default_score=Value(0)
)
```

Tức field tạm `default_score` luôn bằng 0.

Trong code thực tế bạn có thể gặp:

```python
from decimal import Decimal
from django.db.models import Value

Value(Decimal("0.8"))
```

để biểu diễn hệ số cố định (ví dụ 0.8).

---

## 32. `Coalesce()`

`Coalesce(a, b)` nghĩa là:

```text
Nếu a có giá trị thì lấy a
Nếu a là NULL thì lấy b
```

Ví dụ:

```python
from django.db.models import F, Value
from django.db.models.functions import Coalesce

Coalesce(F("month_of_work"), Value(0))
```

Tương tự Python:

```python
month_of_work if month_of_work is not None else 0
```

---

## 33. `Case` / `When`

`Case/When` là **if / elif / else** trong SQL.

Ví dụ Python:

```python
if account_name == "loctv":
    external = 12
elif account_name == "hoangplv":
    external = 6
else:
    external = 0
```

Django ORM:

```python
from django.db.models import Case, When, Value, IntegerField

Case(
    When(account_name__iexact="loctv", then=Value(12)),
    When(account_name__iexact="hoangplv", then=Value(6)),
    default=Value(0),
    output_field=IntegerField(),
)
```

`iexact` nghĩa là so sánh bằng nhưng không phân biệt hoa thường.

---

## 34. List comprehension để generate nhiều `When(...)`

Đoạn này:

```python
[
    When(
        account_name__iexact=prefix,
        then=Value(experience.get("same_role", 0)),
    )
    for prefix, experience in FIXED_MEMBER_EXTERNAL_EXPERIENCE_MONTHS.items()
]
```

nghĩa là tạo danh sách nhiều `When(...)` từ dict.

Nếu dict là:

```python
{
    "loctv": {"same_role": 12},
    "hoangplv": {"same_role": 6},
}
```

thì nó tạo ra:

```python
[
    When(account_name__iexact="loctv", then=Value(12)),
    When(account_name__iexact="hoangplv", then=Value(6)),
]
```

Dấu `*` phía trước list là để “bung list” vào `Case(...)`:

```python
Case(*when_list)
```

tương đương:

```python
Case(When(...), When(...))
```

---

## 35. `ExpressionWrapper`

Khi công thức hơi phức tạp, Django cần biết **kết quả là kiểu gì**.

Ví dụ:

```python
from django.db.models import F, Value, IntegerField, ExpressionWrapper

ExpressionWrapper(
    F("month_of_work") + Value(1),
    output_field=IntegerField(),
)
```

Ý nghĩa:

```text
Django ơi, kết quả phép tính này là integer.
```

Trong case có hệ số 0.8, 0.5, thường dùng `DecimalField` cho phần trung gian.

---

## 36. `Round()`

`Round(expression, precision=0)` làm tròn số trong DB.

Ví dụ:

```text
13.8 -> 14
9.2 -> 9
```

Trong Django:

```python
from django.db.models import F
from django.db.models.functions import Round

Round(F("score"), precision=0)
```

---

## 37. `Cast()`

`Cast()` dùng để ép kiểu dữ liệu.

Ví dụ:

```python
from django.db.models import F, IntegerField
from django.db.models.functions import Cast, Round

Cast(
    Round(F("score"), precision=0),
    output_field=IntegerField(),
)
```

Tương đương ý tưởng:

```text
round(score) rồi ép về integer
```

(giống Python `int(round(score))`), nhưng đang chạy trong DB query.

---

## 38. Áp vào công thức business (ví dụ thực tế)

Business:

```text
experience = month_of_work + round(same_role * 0.8 + different_role * 0.5)
```

Django ORM phải viết thành (chạy trong DB):

```python
from decimal import Decimal

from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    IntegerField,
    Value,
)
from django.db.models.functions import Cast, Coalesce, Round

resolved_experience_months = ExpressionWrapper(
    Coalesce(F("month_of_work"), Value(0))
    + Cast(
        Round(
            ExpressionWrapper(
                Coalesce(F("same_role_external_experience_months"), Value(0))
                * Value(Decimal("0.8"))
                + Coalesce(F("different_role_external_experience_months"), Value(0))
                * Value(Decimal("0.5")),
                output_field=DecimalField(max_digits=7, decimal_places=2),
            ),
            precision=0,
        ),
        output_field=IntegerField(),
    ),
    output_field=IntegerField(),
)
```

Bạn sẽ hay gặp pattern này khi cần:

- Resolve NULL về 0 (`Coalesce`)
- Nhân hệ số cố định (`Value(Decimal("0.8"))`, `Value(Decimal("0.5"))`)
- Làm tròn trong DB (`Round`)
- Ép về int để cộng/so sánh/sort (`Cast(..., IntegerField())`)
- Bọc lại để Django biết type cuối (`ExpressionWrapper(..., output_field=...)`)
