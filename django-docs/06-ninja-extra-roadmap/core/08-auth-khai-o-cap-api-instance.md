# Auth — Khai Ở Cấp API Instance, Không Phải Từng View

> Tiếp theo bài 01-07. Bài này so sánh **vị trí khai báo auth** giữa DRF và ninja-extra. Toàn bộ ví dụ là code minh họa tự viết, không cần project nào để đối chiếu.

---

## 1. DRF — Auth Khai Theo Từng View/ViewSet

```python
class MyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
```

Mỗi View/ViewSet tự khai `authentication_classes` + `permission_classes` riêng — muốn đổi auth cho 1 view thì sửa đúng view đó, không ảnh hưởng view khác. Nếu có 20 view, không dùng base class chung thì phải lặp lại 2 dòng này 20 lần.

---

## 2. ninja-extra — Khai 1 Lần Ở Cấp `NinjaExtraAPI`

`ninja-extra` cho phép khai `auth=` ngay khi tạo instance `NinjaExtraAPI` — áp dụng cho **toàn bộ** controller đăng ký vào instance đó, không cần khai lại ở từng method:

```python
from ninja_extra import NinjaExtraAPI, api_controller, http_get, ControllerBase
from ninja.security import HttpBearer

class SimpleTokenAuth(HttpBearer):
    def authenticate(self, request, token):
        # token lấy từ header "Authorization: Bearer <token>"
        if token == "valid-token":
            return token   # return khác None -> coi là auth thành công
        return None          # return None -> Ninja tự trả 401

api = NinjaExtraAPI(auth=SimpleTokenAuth())   # khai auth 1 LẦN DUY NHẤT ở đây

@api_controller("/tasks")
class TaskController(ControllerBase):
    @http_get("/list")                        # method này TỰ ĐỘNG được bảo vệ bởi SimpleTokenAuth
    def list_tasks(self, request):
        return {"tasks": []}

    @http_get("/detail/{task_id}")             # method này CŨNG tự động được bảo vệ, không cần khai lại
    def task_detail(self, request, task_id: int):
        return {"id": task_id}

api.register_controllers(TaskController)
```

Ninja cũng cho phép khai `auth=` ở cấp thấp hơn nếu cần khác biệt — `@api_controller("/tasks", auth=...)` (riêng cho 1 controller) hoặc `@http_get("/path", auth=...)` (riêng cho 1 method) — nhưng nếu không khai gì thêm, mọi endpoint sẽ dùng đúng `auth=` đã khai ở `NinjaExtraAPI(...)`.

So sánh:

| | DRF | ninja-extra |
|:---|:---|:---|
| Nơi khai auth mặc định | Từng View/ViewSet | 1 lần ở `NinjaExtraAPI(auth=...)`, áp dụng cho cả app |
| Muốn override cho 1 controller/method riêng | Sửa `authentication_classes` của đúng view đó | Khai thêm `auth=` ở `@api_controller(...)` hoặc `@http_get(...)` — override cái đã khai ở cấp API instance |
| Số chỗ phải khai khi có 20 endpoint dùng chung 1 auth | 20 lần (hoặc dùng base class chung) | 1 lần |

---

## 3. 2 Cách Viết Class Auth — `APIKeyHeader` vs `HttpBearer`

Ninja cung cấp sẵn vài class cha để kế thừa, tùy vào **credential nằm ở đâu** trong request:

### `HttpBearer` — đọc theo chuẩn `Authorization: Bearer <token>`

```python
from ninja.security import HttpBearer

class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        user = find_user_by_token(token)   # tự viết hàm này
        if user:
            request.user = user
            return user
        return None
```

### `APIKeyHeader` — đọc theo 1 header/cookie tự đặt tên

```python
from ninja.security import APIKeyHeader

class CookieAuth(APIKeyHeader):
    param_name = "auth_token"   # tên cookie sẽ đọc, VD: request.COOKIES["auth_token"]

    def authenticate(self, request, key):
        user = find_user_by_cookie_value(key)   # tự viết hàm này
        if user:
            request.user = user
            return user
        return None
```

```text
HttpBearer     → dùng khi client gửi token qua header "Authorization: Bearer <token>"
                 (phổ biến cho API-to-API, mobile app, Postman...)
APIKeyHeader   → dùng khi credential nằm ở 1 cookie hoặc header tự đặt tên
                 (phổ biến cho web app dùng cookie session-like)
```

Cả 2 đều implement method `authenticate(self, request, token_hoac_key)` — `return` khác `None` (thường là user object) nghĩa là auth thành công, Ninja tự set kết quả đó vào chỗ bạn cần (thường gán vào `request.user` trong thân hàm), `return None` nghĩa là auth thất bại, Ninja tự trả `401`.

---

## 4. Permission Class — Cách Dùng Nếu Có, Và Cách Thay Thế Nếu Không Dùng

`ninja-extra` có hỗ trợ permission class tương tự DRF, đặt tên field là `permissions` (không phải `permission_classes` như DRF):

```python
from ninja_extra import api_controller, http_get, ControllerBase
from ninja_extra.permissions import BasePermission, IsAuthenticated

class IsOwner(BasePermission):
    def has_permission(self, request, controller) -> bool:
        task_id = request.resolver_match.kwargs.get("task_id")
        return Task.objects.filter(id=task_id, owner=request.user).exists()

@api_controller("/tasks", permissions=[IsAuthenticated])   # áp dụng cho cả controller
class TaskController(ControllerBase):

    @http_get("/detail/{task_id}", permissions=[IsOwner])   # thêm riêng cho method này
    def task_detail(self, request, task_id: int):
        return {"id": task_id}
```

```text
IsAuthenticated  → class có sẵn từ ninja_extra.permissions, giống hệt DRF
IsOwner          → tự viết, kế thừa BasePermission, override has_permission()
permissions=[...] → khai ở @api_controller (áp dụng cả class) hoặc @http_get (áp dụng riêng method)
```

Nếu 1 project **không dùng** cơ chế `permissions=[...]` này (dù framework có hỗ trợ), cách thay thế phổ biến là check quyền **thủ công ngay trong thân hàm**, thường lồng luôn vào điều kiện query thay vì tách class riêng:

```python
@http_get("/detail/{task_id}")
def task_detail(self, request, task_id: int):
    task = Task.objects.filter(id=task_id, owner=request.user).first()   # lồng luôn "chỉ owner mới thấy" vào query
    if not task:
        return 404, {"code": "not_found", "detail": "Task not found"}
    return {"id": task.id}
```

Khác biệt: cách dùng `permissions=[IsOwner]` tách rõ "ai được phép gọi" ra khỏi logic nghiệp vụ, tái dùng được ở nhiều endpoint; cách check thủ công gọn hơn cho 1 endpoint đơn lẻ nhưng phải viết lại điều kiện tương tự ở mỗi nơi cần.

---

## 5. Kết Luận

Cần chốt:

- DRF khai auth/permission theo từng View — ninja-extra cho phép khai **1 lần duy nhất** ở cấp `NinjaExtraAPI(auth=...)`, áp dụng cho toàn bộ controller, và vẫn override được ở cấp thấp hơn (`@api_controller`, `@http_get`) khi cần khác biệt.
- 2 class cha phổ biến để viết auth: `HttpBearer` (đọc `Authorization: Bearer <token>`) và `APIKeyHeader` (đọc 1 cookie/header tự đặt tên) — cả 2 đều implement `authenticate(request, token)`, trả khác `None` là thành công.
- `permissions=[...]` (từ `ninja_extra.permissions`) là cơ chế permission class có sẵn, dùng được ở cấp controller hoặc method — nếu không dùng, cách thay thế phổ biến là check quyền thủ công, thường lồng thẳng vào điều kiện query (`filter(id=..., owner=request.user)`).
