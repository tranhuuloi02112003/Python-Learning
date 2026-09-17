# `RouteContext` (`self.context`) và Settings Toàn Cục

> Tiếp theo `focus/12-error-handling-exception-toan-cuc.md`. 2 chủ đề trong bài này đều **chưa được dùng** trong `leadplusone_api` — viết ra để biết framework có gì, không nhầm lẫn khi gặp ở project khác hoặc khi cần dùng sau này.

---

## 1. `RouteContext` — Đối Tượng Mọi Controller Đều Có, Qua `self.context`

Ở bài 03, khi giới thiệu `ControllerBase`, đã nói lướt qua "`self.context` chứa `request` hiện tại". Giờ xem chi tiết thật.

Source `ninja_extra/context.py:19-59`:

```python
class RouteContext(RouteContextBase):
    """APIController Context which will be available to the class instance when handling request"""
    __slots__ = ["permission_classes", "request", "response", "args", "kwargs", ...]

    permission_classes: List[BasePermissionType]
    request: Union[Any, HttpRequest, None]
    response: Union[Any, HttpResponse, None]
    args: List[Any]
    kwargs: DictStrAny
```

Chứa: `request` (giống tham số `request` bạn nhận trong method, chỉ là truy cập qua đường khác), `response`, `permission_classes` đang áp dụng cho route này, và `args`/`kwargs` gốc của request.

**Ai gán giá trị vào `self.context`?** Không phải bạn — ninja-extra tự làm, mỗi request 1 lần, ngay trước khi gọi method của bạn (`ninja_extra/controllers/route/route_functions.py:175,187`):

```python
controller_instance.context = route_context   # gán trước khi gọi method
...
controller_instance.context = None             # dọn lại sau khi xong
```

Trong method, bạn truy cập qua `self.context.request`, `self.context.permission_classes`... — dùng khi cần thông tin route mà không muốn thêm tham số vào signature:

```python
async def some_method(self, request):
    print(self.context.permission_classes)   # xem permission class nào đang áp dụng cho route này
    # thường không cần — vì request đã có sẵn qua tham số, và permission thường tự áp dụng, không cần đọc lại
```

> Thực tế: **chưa dùng** trong repo. Grep `self.context` toàn `source_code/` chỉ ra 1 thứ khác hoàn toàn — `self.context.get("organization_user")` trong `MPF_WEB_F12_Account_Management/serializers.py` — đó là `context` của DRF `Serializer` (dict tự truyền tay khi gọi `MySerializer(data=..., context={...})`), **không liên quan** gì tới `RouteContext` của ninja-extra. Dễ nhầm vì tên trùng ("context") nhưng là 2 cơ chế của 2 framework khác nhau.

---

## 2. Settings Toàn Cục — 2 Cách Đọc KHÁC NHAU Giữa `ninja` Core Và `ninja-extra`

Đây là điểm dễ gõ sai nhất: `ninja` core đọc setting theo kiểu **từng key rời**, còn `ninja-extra` đọc theo kiểu **1 dict lồng**.

### `ninja` core — từng biến `NINJA_*` riêng, đặt trực tiếp trong `settings.py`

Verify `ninja/conf.py:8-36`:

```python
class Settings(BaseModel):
    PAGINATION_CLASS: str = Field("ninja.pagination.LimitOffsetPagination", alias="NINJA_PAGINATION_CLASS")
    PAGINATION_PER_PAGE: int = Field(100, alias="NINJA_PAGINATION_PER_PAGE")
    PAGINATION_MAX_PER_PAGE_SIZE: int = Field(100, alias="NINJA_MAX_PER_PAGE_SIZE")
    PAGINATION_MAX_LIMIT: int = Field(inf, alias="NINJA_PAGINATION_MAX_LIMIT")
    NUM_PROXIES: Optional[int] = Field(None, alias="NINJA_NUM_PROXIES")
    DEFAULT_THROTTLE_RATES: Dict = Field({...}, alias="NINJA_DEFAULT_THROTTLE_RATES")
    FIX_REQUEST_FILES_METHODS: Set[str] = Field({"PUT", "PATCH", "DELETE"}, alias="NINJA_FIX_REQUEST_FILES_METHODS")
```

Muốn đổi, khai thẳng trong `settings.py`:

```python
# settings.py
NINJA_PAGINATION_PER_PAGE = 20
NINJA_DEFAULT_THROTTLE_RATES = {"anon": "500/day", "user": "5000/day", "auth": "5000/day"}
```

### `ninja-extra` — 1 dict duy nhất, tên `NINJA_EXTRA`

Verify `ninja_extra/conf/package_settings.py:45-91`:

```python
NinjaEXTRA_SETTINGS_DEFAULTS = {
    "INJECTOR_MODULES": [],
    "PAGINATION_CLASS": "ninja.pagination.LimitOffsetPagination",
    "THROTTLE_CLASSES": ["ninja_extra.throttling.AnonRateThrottle", "ninja_extra.throttling.UserRateThrottle"],
    "THROTTLE_RATES": {"user": "1000/day", "anon": "100/day"},
    "ORDERING_CLASS": "ninja_extra.ordering.Ordering",
    "SEARCHING_CLASS": "ninja_extra.searching.Searching",
    "ROUTE_CONTEXT_CLASS": "ninja_extra.context.RouteContext",
}
USER_SETTINGS = getattr(django_settings, "NINJA_EXTRA", NinjaEXTRA_SETTINGS_DEFAULTS)
```

Muốn đổi, khai **1 dict duy nhất** tên `NINJA_EXTRA` (không phải từng biến `NINJA_EXTRA_PAGINATION_CLASS` rời như core):

```python
# settings.py
NINJA_EXTRA = {
    "THROTTLE_RATES": {"user": "1000/day", "anon": "100/day"},
    "PAGINATION_CLASS": "ninja_extra.pagination.PageNumberPaginationExtra",
}
```

**Bảng so sánh nhanh để không nhầm:**

| | `ninja` core | `ninja-extra` |
|:---|:---|:---|
| Cách khai trong `settings.py` | Từng biến rời, tiền tố `NINJA_` | 1 dict duy nhất, tên `NINJA_EXTRA` |
| Ví dụ | `NINJA_PAGINATION_PER_PAGE = 20` | `NINJA_EXTRA = {"PAGINATION_CLASS": "..."}` |
| Setting đổi throttle rate | `NINJA_DEFAULT_THROTTLE_RATES = {...}` | `NINJA_EXTRA = {"THROTTLE_RATES": {...}}` — **tên key khác nhau, không dùng lẫn được** |

> Thực tế: **chưa dùng** trong repo — grep `NINJA_` trong `leadplus_one/settings.py` không ra kết quả nào. Cả `ninja` core và `ninja-extra` đang chạy với **toàn bộ giá trị mặc định** (pagination 100/trang, throttle rate mặc định của thư viện, không giới hạn injector module...). Duy nhất `"ninja_extra"` xuất hiện trong `INSTALLED_APPS` (`settings.py:91`) — chỉ để đăng ký app, không cấu hình gì thêm.

---

## 3. Kết Luận

Cần chốt:

- `self.context` (`RouteContext`) chứa `request`/`response`/`permission_classes`/`args`/`kwargs` của route hiện tại — ninja-extra tự gán trước mỗi request, tự dọn sau khi xong. Chưa dùng trong repo — coi chừng nhầm với `context` của DRF Serializer (tên giống, cơ chế khác hoàn toàn).
- Settings của `ninja` core khai từng biến `NINJA_*` rời; settings của `ninja-extra` khai chung 1 dict `NINJA_EXTRA = {...}` — 2 cách khác nhau, dễ gõ nhầm tên key nếu không phân biệt rõ 2 package.
- `leadplusone_api` hiện chạy toàn bộ default, không override setting nào của cả 2 package.

Bài tiếp theo (`14-dependency-injection-thuc-su-qua-injector.md`) đào sâu phần đính chính đã thêm vào bài 03 — cơ chế auto-DI thật của ninja-extra qua thư viện `injector`.
