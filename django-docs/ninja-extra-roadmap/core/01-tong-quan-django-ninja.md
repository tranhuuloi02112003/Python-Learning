# Tổng Quan Django Ninja

> Note: Bài này giả định bạn đã biết Django core (model, urls, view) và DRF (đã học ở `drf-roadmap/`). Ở đây chỉ tập trung giải thích khái niệm **riêng** của Django Ninja — chưa so sánh với DRF, phần so sánh để ở bài cuối cùng của folder này.

---

## 1. Django Ninja Là Gì?

Django Ninja là một **thư viện viết API cho Django**, giống DRF ở mục đích (nhận request, trả JSON), nhưng khác cách viết:

```text
DRF:          tự viết Serializer (CharField, IntegerField...) để validate
Django Ninja: dùng Pydantic (type hint: str, int, Optional[str]...) để validate
```

Điểm khác biệt lớn nhất: Django Ninja viết theo kiểu **function-based**, không bắt buộc dùng class.

---

## 2. Flow Cơ Bản Nhất

```text
Request → router.post("/path")(function) → Ninja tự parse JSON body
        → ép vào Pydantic Schema → function(request, payload: Schema)
        → function return dict/object → Ninja tự serialize theo response={...}
```

Ví dụ tối thiểu:

```python
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class HelloSchema(Schema):
    name: str

@api.post("/hello")
def hello(request, payload: HelloSchema):
    return {"message": f"Hello {payload.name}"}
```

So với DRF, những thứ bạn quen thuộc vẫn còn nguyên vẹn:

| Vẫn giống DRF | Khác DRF |
|:---|:---|
| `request` object vẫn là Django request | Không có `urls.py` riêng — route khai ngay tại `@api.post(...)` |
| Vẫn trả JSON, vẫn có status code | Không viết class Serializer — dùng Pydantic `Schema` |
| Vẫn chạy trên Django, vẫn dùng ORM bình thường | Không bắt buộc viết class View — mỗi endpoint là 1 function |

---

## 3. Router — Nơi Khai Route

`router` trong Ninja đóng vai trò gần giống `urls.py`, nhưng khai ngay tại chỗ định nghĩa function:

```python
from ninja import Router

router = Router()

@router.get("/list")
def list_items(request):
    return {"items": []}

@router.post("/create")
def create_item(request, payload: ItemSchema):
    ...
```

Rồi gắn router vào app chính:

```python
# main api instance
api.add_router("/items", router)
```

Cần nhớ:

```text
router.get/post/put/patch/delete("/path")  → khai HTTP method + path cùng lúc
Không có file urls.py riêng cho phần này — route "dính liền" với function xử lý.
```

---

## 4. Path Operation — Function Độc Lập

Mỗi endpoint trong Ninja thuần là **1 function độc lập**, không có class bao quanh:

```python
@router.get("/persona/{persona_id}/detail")
def persona_detail(request, persona_id: int):
    ...
```

So sánh tư duy:

```text
DRF:    class TaskViewSet(ViewSet):  → nhiều method (get/post/put) sống chung 1 class
Ninja:  def task_list(request): ...  → mỗi function là 1 endpoint riêng biệt, không chung class
```

Vì không có class, nếu nhiều endpoint cần dùng chung logic (VD: cùng gọi `AuthService`, `TaskService`...), bạn phải tự khởi tạo lại service đó ở **từng function** — đây chính là hạn chế mà `ninja-extra` (bài 03 trong folder này) giải quyết.

---

## 5. Kết Luận

Cần chốt trước khi qua bài tiếp theo:

- Django Ninja vẫn chạy trên Django, vẫn nhận `request`, vẫn trả JSON + status code — không có gì "mới hoàn toàn".
- Khác biệt cốt lõi: dùng Pydantic `Schema` (type hint) thay cho DRF `Serializer`, và route khai ngay tại `router.post(...)` thay vì tách riêng `urls.py`.
- Ninja thuần là function-based — mỗi endpoint 1 function, không có class chứa nhiều endpoint liên quan.

Bài tiếp theo (`02-pydantic-schema-va-response.md`) đi sâu vào cách Pydantic Schema validate input và cách Ninja serialize output.
