# Dependency Injection Thật Của ninja-extra — Thư Viện `injector`

> Tiếp theo `13-route-context-va-settings.md`. Bài 03 gọi cách khởi tạo service trong `__init__` là "Dependency Injection thủ công" — đúng với cách `leadplusone_api` đang làm, nhưng chưa nói hết: framework có 1 cơ chế auto-DI thật, chạy phía dưới mọi controller mà không cần bạn làm gì thêm. Bài này đào sâu cơ chế đó.

---

## 1. `injector` Là Dependency Thật, Không Phải Tùy Chọn

```bash
pip show django-ninja-extra
# Requires: asgiref, contextlib2, Django, django-ninja, injector
```

`injector` (PyPI package độc lập, không phải code tự viết) là 1 thư viện DI thuần Python — cài kèm bắt buộc khi cài `django-ninja-extra`, không phải optional add-on.

---

## 2. Cơ Chế Thật: Mọi Controller Đều Đi Qua `Injector`, Kể Cả Khi Bạn Không Biết

Verify từ source, đi theo đúng thứ tự chạy thật:

**Bước 1 — Lúc Django app khởi động** (`ninja_extra/apps.py:19-24`): ninja-extra tạo 1 `Injector` instance dùng chung cho cả app:
```python
self.injector = Injector([NinjaExtraModule()])
```

**Bước 2 — Lúc bạn viết `@api_controller` lên class** (`ninja_extra/controllers/base.py:530-531`): ninja-extra tự kiểm tra `__init__` của class đó, nếu **chưa** được đánh dấu `@inject` thì tự đánh dấu:
```python
from injector import inject, is_decorated_with_inject

if not is_decorated_with_inject(cls.__init__):
    fail_silently(inject, constructor_or_class=cls)
```
Nghĩa là: **bạn không cần tự viết `@inject`** — chỉ cần dùng `@api_controller`, `__init__` của bạn tự động trở thành 1 "DI target" theo type hint của tham số.

**Bước 3 — Mỗi request tới** (`ninja_extra/controllers/route/route_functions.py:124-144`, hàm `_get_controller_instance`): controller không được tạo bằng `TaskController()` thông thường, mà qua:
```python
injector = get_injector()
controller_instance = injector.create_object(
    _api_controller.controller_class, additional_kwargs=additional_kwargs,
)
```
`injector.create_object(cls)` đọc type hint trong `__init__` của `cls`, tự resolve + tự khởi tạo từng tham số.

---

## 3. Cách Dùng Thật — Khai Type Hint Trong `__init__` Thay Vì Tự `Service()`

So sánh 2 cách viết `__init__` cho cùng 1 controller:

```python
# Cách "thủ công" — leadplusone_api đang dùng (bài 03)
class TaskController(ControllerBase):
    def __init__(self):
        self.auth_service = AuthService()
        self.task_service = TaskService()
```

```python
# Cách auto-DI thật — khai type hint, KHÔNG tự gọi Service()
class TaskController(ControllerBase):
    def __init__(self, auth_service: AuthService, task_service: TaskService):
        self.auth_service = auth_service
        self.task_service = task_service
```

Ở cách thứ 2, bạn **không** viết `self.auth_service = AuthService()` — chỉ khai tham số có type hint, `injector.create_object` tự thấy `AuthService`/`TaskService` là concrete class (không phải interface trừu tượng) nên tự `AuthService()`/`TaskService()` hộ bạn, rồi truyền vào `__init__`.

Muốn dùng cho trường hợp phức tạp hơn — VD 1 interface có nhiều implementation, cần chỉ định implementation nào — khai 1 `Module` riêng và đăng ký qua setting đã học ở bài 13 (`NINJA_EXTRA["INJECTOR_MODULES"]`):

```python
from injector import Module, provider

class TaskServiceModule(Module):
    @provider
    def provide_task_service(self) -> TaskServiceInterface:
        return TaskServiceImpl()   # chỉ định rõ implementation nào được inject
```
```python
# settings.py
NINJA_EXTRA = {"INJECTOR_MODULES": ["myapp.modules.TaskServiceModule"]}
```

Ninja-extra còn export sẵn `get_injector()` và `service_resolver(...)` (`ninja_extra/dependency_resolver.py`) để tự resolve 1 service ở nơi **không phải** `__init__` của controller (VD trong 1 function tiện ích độc lập) — không cần trace chi tiết ở đây, chỉ cần biết 2 hàm này tồn tại nếu sau này cần resolve DI ngoài controller.

---

## 4. Vì Sao Cách `leadplusone_api` Đang Làm (Tự `Service()`) Vẫn Chạy Đúng?

Vì `injector.create_object(cls)` **vẫn luôn gọi `__init__` của `cls`** — chỉ khác ở việc `__init__` đó có tham số cần resolve hay không:

```text
__init__ tự viết hết logic (self.x = X())     → injector gọi __init__(), không cần resolve gì thêm → chạy y hệt như gọi tay
__init__ có tham số type hint (x: X)          → injector tự resolve X trước, rồi gọi __init__(resolved_x)
```

Không phải 2 cơ chế tách biệt — chỉ là **cùng 1 cơ chế `injector.create_object`**, tùy `__init__` bạn viết có "để chỗ" cho nó resolve hay tự làm hết. `leadplusone_api` không sai khi viết tay — chỉ đơn giản là không tận dụng phần auto-resolve của `injector`.

> Thực tế: grep toàn `leadplusone_api/source_code/` cho `injector`/`ServiceModule`/`@injectable`/`service_resolver`/`INJECTOR_MODULES` → **0 kết quả**. Mọi controller (`article_writer.py`, `rewrite_article.py`...) đều viết `__init__` kiểu tự `Service()` — không controller nào khai type hint để tận dụng auto-resolve.

---

## 5. Khi Nào Nên Đổi Sang Auto-DI Thật?

Không có lý do bắt buộc phải đổi — cách viết tay vẫn đúng và dễ đọc cho project hiện tại (5 service cố định, không có interface/implementation thay đổi theo môi trường). Auto-DI qua `Module` thật sự có lợi khi:

- Cần đổi implementation theo môi trường (VD: `FakeEmailService` khi test, `RealEmailService` khi chạy thật) mà không sửa code controller.
- Nhiều controller dùng chung 1 service, muốn quản lý lifecycle (singleton/scoped) tập trung ở 1 chỗ (`Module`) thay vì tự `Service()` rải ở từng `__init__`.

Nếu chưa gặp nhu cầu này, viết tay vẫn là lựa chọn hợp lý, không phải "làm sai cách của framework".

---

## 6. Kết Luận

Cần chốt:

- `injector` là dependency thật, bắt buộc của `django-ninja-extra` — không phải optional.
- ninja-extra **tự động** `@inject` mọi `__init__` của class có `@api_controller`, rồi khởi tạo controller mỗi request qua `injector.create_object(...)` — auto-DI chạy ngầm dù bạn không biết.
- Cách tận dụng thật: khai type hint tham số trong `__init__` (`def __init__(self, auth_service: AuthService)`) thay vì tự `Service()` — injector tự resolve concrete class; dùng `Module` + `NINJA_EXTRA["INJECTOR_MODULES"]` khi cần chỉ định implementation cụ thể cho 1 interface.
- Cách viết tay của `leadplusone_api` vẫn đúng và chạy được — vì `create_object` luôn gọi `__init__` bình thường, chỉ là không tận dụng phần auto-resolve. Đổi sang auto-DI có lợi khi cần đổi implementation theo môi trường hoặc quản lý lifecycle tập trung — chưa cần thì không bắt buộc phải đổi.

Bài tiếp theo (`15-list-features-va-throttling-chua-dung.md`) gộp 4 tính năng cùng nhóm "có sẵn trong framework nhưng repo chưa đụng tới": pagination/ordering/searching (dành cho endpoint list) và throttling (rate limit).
