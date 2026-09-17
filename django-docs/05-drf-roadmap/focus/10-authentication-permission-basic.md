# Authentication / Permission Basic

Bài này giúp bạn đọc được auth/permission trong API thực tế.

Khi đọc project, bạn sẽ gặp nhiều đoạn như:

```python
permission_classes = [IsAuthenticated]
```

hoặc:

```python
user = request.user
```

Nếu chưa hiểu authentication/permission, bạn sẽ không biết:

- API này có cần login không?
- User hiện tại lấy từ đâu?
- Vì sao request này bị `401`?
- Vì sao request này bị `403`?
- Vì sao query lại filter theo `request.user`?

Phần này học ở mức basic để đọc code trước, chưa cần đi sâu JWT/custom auth.

---

## 1. Authentication là gì?

Authentication là bước xác định:

```text
Người đang gọi API là ai?
```

Ví dụ client gọi API kèm token:

```text
GET /tasks/
Authorization: Bearer <token>
```

Backend kiểm tra token đó hợp lệ hay không.

Nếu hợp lệ, DRF gán user vào:

```python
request.user
```

Ví dụ:

```python
def get_my_tasks(self, request):
    user = request.user
```

Ở đây `request.user` chính là user đang đăng nhập.

---

## 2. Permission là gì?

Permission là bước kiểm tra:

```text
User này có quyền gọi API này không?
```

Ví dụ:

```python
permission_classes = [IsAuthenticated]
```

Nghĩa là:

```text
Chỉ user đã đăng nhập mới được gọi API này.
```

Nếu chưa login mà gọi API, sẽ bị chặn.

---

## 3. Phân biệt Authentication và Permission

Dễ nhớ như này:

```text
Authentication:
Bạn là ai?
```

```text
Permission:
Bạn có quyền làm việc này không?
```

Ví dụ thực tế:

```text
Authentication:
Hệ thống xác định bạn là user A.

Permission:
Hệ thống kiểm tra user A có được xem task này không.
```

---

## 4. `request.user`

`request.user` là user hiện tại đang gọi API.

Ví dụ:

```python
def get_my_tasks(self, request):
    tasks = Task.objects.filter(assignee=request.user)

    serializer = TaskSerializer(tasks, many=True)

    return self._response_status_200(serializer.data)
```

Ý nghĩa:

```text
Lấy danh sách task được assign cho user đang login.
```

Flow:

```text
Client gửi request kèm token/session
-> DRF xác định user
-> gán vào request.user
-> view dùng request.user để query data
```

---

## 5. `permission_classes`

`permission_classes` dùng để khai báo rule truy cập API.

Ví dụ:

```python
from rest_framework.permissions import IsAuthenticated


class TaskViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_my_tasks(self, request):
        ...
```

Ý nghĩa:

```text
Tất cả method trong TaskViewSet yêu cầu user phải đăng nhập.
```

Nếu user chưa login mà gọi API:

```text
GET /tasks/
```

thì API sẽ bị chặn trước khi vào method `get_my_tasks`.

---

## 6. `IsAuthenticated`

`IsAuthenticated` nghĩa là:

```text
Chỉ cho user đã đăng nhập gọi API.
```

Ví dụ:

```python
permission_classes = [IsAuthenticated]
```

Hay gặp ở API:

- Lấy danh sách task của tôi.
- Tạo task.
- Cập nhật task.
- Xóa task.
- Lấy profile.
- Đổi mật khẩu.

Ví dụ:

```python
class ProfileViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_profile(self, request):
        serializer = UserSerializer(request.user)

        return self._response_status_200(serializer.data)
```

Flow:

```text
User phải login
-> request.user có giá trị
-> serialize thông tin user hiện tại
-> trả response
```

---

## 7. `AllowAny`

`AllowAny` nghĩa là:

```text
Ai cũng gọi được API, không cần login.
```

Ví dụ:

```python
from rest_framework.permissions import AllowAny


class AuthViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [AllowAny]

    def login(self, request):
        ...
```

Hay dùng cho:

- Login
- Register
- Forgot password
- Public API
- Health check

Ví dụ:

```python
class AuthViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [AllowAny]

    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return self._response_status_400_bad_request(serializer.errors)

        # xử lý login
        return self._response_status_200({
            "token": "..."
        })
```

---

## 8. `authentication_classes`

`authentication_classes` dùng để khai báo cách xác thực user.

Ví dụ:

```python
authentication_classes = [TokenAuthentication]
```

hoặc:

```python
authentication_classes = [SessionAuthentication]
```

Ở mức basic, bạn chỉ cần hiểu:

```text
authentication_classes quyết định backend đọc thông tin login từ đâu.
```

Ví dụ:

```text
TokenAuthentication:
Đọc token từ request header.

SessionAuthentication:
Đọc session login của Django.

JWTAuthentication:
Đọc JWT token từ Authorization header.
```

Trong dự án thực tế, phần này thường đã config sẵn global trong `settings.py`.

Nên khi mới join, bạn chưa cần tự setup auth từ đầu.

---

## 9. Auth config global và auth config riêng từng view

Project có thể config authentication/permission mặc định trong `settings.py`.

Ví dụ:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

Ý nghĩa:

```text
Mặc định toàn bộ API yêu cầu login.
```

Sau đó API nào public thì override:

```python
class AuthViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [AllowAny]
```

Nghĩa là:

```text
Riêng AuthViewSet cho phép mọi người gọi.
```

---

## 10. `401` và `403` khác nhau thế nào?

Đây là phần rất hay gặp khi debug.

### 401 Unauthorized

Hiểu đơn giản:

```text
Bạn chưa đăng nhập hoặc token không hợp lệ.
```

Ví dụ:

- Gọi API cần login nhưng không gửi token.
- Token hết hạn.
- Token sai.

### 403 Forbidden

Hiểu đơn giản:

```text
Bạn đã đăng nhập rồi, nhưng không có quyền làm việc này.
```

Ví dụ:

- User A muốn sửa task của User B.
- Member thường gọi API chỉ admin được dùng.
- User đã login nhưng không thuộc project đó.

Nhớ nhanh:

```text
401: Chưa xác thực được bạn là ai.
403: Biết bạn là ai rồi, nhưng bạn không có quyền.
```

---

## 11. Check quyền thủ công trong method

Ngoài `permission_classes`, project có thể check quyền thủ công trong method.

Ví dụ:

```python
def update_task(self, request, task_id=None):
    task = Task.objects.filter(id=task_id).first()

    if not task:
        return self._response_status_404_not_found("Task not found")

    if task.assignee != request.user:
        return self._response_status_403_forbidden(
            "You do not have permission to update this task"
        )

    task.title = request.data.get("title")
    task.save()

    serializer = TaskSerializer(task)

    return self._response_status_200(serializer.data)
```

Flow:

```text
Tìm task
Nếu không có -> 404
Nếu task không thuộc user hiện tại -> 403
Nếu có quyền -> update task
Trả response 200
```

Đây là kiểu rất thực tế.

---

## 12. Query theo `request.user`

Khi đã có auth, API thường query data theo user hiện tại.

Ví dụ:

```python
tasks = Task.objects.filter(assignee=request.user)
```

Hoặc:

```python
projects = Project.objects.filter(members=request.user)
```

Hoặc:

```python
reports = DailyReport.objects.filter(user=request.user)
```

Ý nghĩa chung:

```text
Chỉ lấy dữ liệu liên quan đến user đang login.
```

Khi đọc code thấy `request.user`, cần tự hỏi:

- API này đang lấy data theo user nào?
- User này có role gì?
- Có đang check quyền không?

---

## 13. Permission ở cấp class và cấp method

Với ViewSet, nếu khai báo:

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [IsAuthenticated]
```

thì thường áp dụng cho toàn bộ action trong class.

Ví dụ:

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_tasks(self, request):
        ...

    def create_task(self, request):
        ...

    def update_task(self, request):
        ...
```

Nghĩa là các action này đều cần login.

Nếu project muốn mỗi method một permission khác nhau, họ có thể tách class hoặc custom lại logic. Phần này để sau, chưa cần học sâu.

---

## 14. Ví dụ API public và private

### API public: login

```python
class AuthViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [AllowAny]

    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return self._response_status_400_bad_request(serializer.errors)

        return self._response_status_200({
            "token": "abc"
        })
```

Ý nghĩa:

```text
Không cần login vẫn gọi được.
Vì đây chính là API dùng để login.
```

### API private: my tasks

```python
class TaskViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_my_tasks(self, request):
        tasks = Task.objects.filter(assignee=request.user)

        serializer = TaskSerializer(tasks, many=True)

        return self._response_status_200(serializer.data)
```

Ý nghĩa:

```text
Phải login mới gọi được.
Dữ liệu trả về phụ thuộc request.user.
```

---

## 15. Ví dụ gần với project thực tế

```python
class DailyReportViewSet(BaseHandleAPI, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_logged_tasks(self, request):
        date = request.query_params.get("date")

        tasks = TaskLog.objects.filter(
            user=request.user,
            log_date=date,
        ).select_related("task")

        serializer = TaskLogSerializer(tasks, many=True)

        return self._response_status_200(serializer.data)
```

Đọc flow:

```text
API yêu cầu login
Lấy date từ query params
Query TaskLog theo user đang login
Lấy task liên quan bằng select_related
Serialize danh sách log task
Trả response 200
```

Điểm quan trọng:

```text
request.user quyết định dữ liệu của ai được trả về.
```

---

## 16. Custom permission là gì? Basic thôi

Đôi khi project có permission tự viết.

Ví dụ:

```python
permission_classes = [IsProjectMember]
```

Hoặc:

```python
permission_classes = [IsAdminUser]
```

`IsAdminUser` là permission có sẵn trong DRF.

`IsProjectMember` có thể là custom permission của project.

Ở mức basic, bạn chỉ cần hiểu:

```text
Permission class là rule quyết định request có được vào API không.
```

Nếu thấy custom permission, hãy search class đó.

Ví dụ:

```python
class IsProjectMember(BasePermission):
    def has_permission(self, request, view):
        ...
```

Bạn chưa cần tự viết ngay, chỉ cần biết cách trace.

---

## 17. Cách đọc auth/permission khi vào dự án

Khi mở một API, đọc theo thứ tự:

1. View/ViewSet có `permission_classes` không?
2. Nếu có: `IsAuthenticated`, `AllowAny`, hay custom permission?
3. Có `authentication_classes` không?
4. Nếu không có, xem `settings.py` có `DEFAULT_AUTHENTICATION_CLASSES` không.
5. Trong method có dùng `request.user` không?
6. Query có lọc theo `request.user` không?
7. Có check quyền thủ công không?

Ví dụ check thủ công:

```python
if task.user != request.user:
    ...

if not request.user.is_staff:
    ...

if role != ...:
    ...
```

---

## 18. Chỗ dễ nhầm

### Nhầm 1: `request.user` tự nhiên mà có

Không phải tự nhiên.

Nó có sau khi authentication chạy.

Nếu request không có token/session hợp lệ, `request.user` có thể là anonymous user hoặc request bị chặn tùy config.

### Nhầm 2: `IsAuthenticated` là login API

Không phải.

`IsAuthenticated` nghĩa là API này yêu cầu user đã login.

Login API thường dùng:

```python
permission_classes = [AllowAny]
```

Vì chưa login thì mới cần gọi login.

### Nhầm 3: `401` và `403` giống nhau

Không giống.

```text
401: chưa xác thực / token sai / chưa login
403: đã xác thực nhưng không có quyền
```

### Nhầm 4: Có `permission_classes` là đủ bảo vệ mọi dữ liệu

Không hẳn.

Ví dụ:

```python
permission_classes = [IsAuthenticated]
```

chỉ đảm bảo user đã login.

Nhưng nếu API lấy task theo id:

```python
task = Task.objects.get(id=task_id)
```

mà không check task có thuộc user không, thì user A có thể lấy task của user B nếu đoán được id.

Nên nhiều API còn phải check object-level permission:

```python
if task.assignee != request.user:
    return self._response_status_403_forbidden()
```

Phần object-level permission học sâu sau. Trước mắt chỉ cần biết có rủi ro này.

---

## 19. Công thức nhớ nhanh

Authentication:

```text
Xác định request này là của user nào.
```

Permission:

```text
User đó có được phép gọi API này không.
```

`request.user`:

```text
User hiện tại sau khi authentication thành công.
```

`IsAuthenticated`:

```text
Phải login mới gọi được.
```

`AllowAny`:

```text
Ai cũng gọi được.
```

`401`:

```text
Chưa login / token sai / token hết hạn.
```

`403`:

```text
Đã login nhưng không đủ quyền.
```

---

## 20. Kết luận

Ở mức join dự án, bạn chưa cần học sâu custom authentication/JWT.

Trước mắt cần nắm chắc:

- `request.user`
- `permission_classes`
- `IsAuthenticated`
- `AllowAny`
- `authentication_classes` ở mức khái niệm
- `401` vs `403`
- query theo `request.user`
- check quyền thủ công trong method

Khi đọc một API thật, hãy nhìn:

```text
URL -> ViewSet method -> permission_classes -> request.user -> ORM query -> response
```

Bài này giúp bạn hiểu vì sao API:

- cần login hay không
- trả data theo user nào
- bị `401` hay `403`
- cần check quyền ở đâu
