# `async`/`await` và `sync_to_async` — Học Từ Ví Dụ Đơn Giản

> Bài này KHÔNG dựa vào `article_writer.py` (trừ 1 đoạn nhỏ ở cuối để đối chiếu). Toàn bộ ví dụ ở đây là code tự tạo, đơn giản, không thuộc project nào — mục tiêu là hiểu khái niệm `async`/`await` trước, sau đó mới áp dụng vào code thật.

---

## 1. Vấn Đề Cần Giải Quyết Là Gì?

Tưởng tượng 1 function phải "chờ" — gọi API bên ngoài, đọc file, hoặc query database. Trong lúc chờ, CPU không làm gì cả, chỉ đứng đợi.

```python
import time

def get_weather():
    time.sleep(3)          # giả lập chờ API trả lời — mất 3 giây
    return "Sunny"
```

Nếu server có 2 request cùng lúc, request thứ 2 phải **xếp hàng** chờ request thứ 1 chạy xong hàm `get_weather()`, dù bản thân nó chẳng liên quan gì đến thời tiết.

`async`/`await` giải quyết đúng vấn đề này: cho phép chương trình **tranh thủ làm việc khác** trong lúc 1 tác vụ đang chờ I/O (network, disk, database).

---

## 2. `async def` Là Gì? — Coroutine

Khi thêm `async` trước `def`, function đó không còn là function bình thường — nó thành **coroutine function**. Gọi nó không chạy code bên trong ngay lập tức:

```python
async def get_weather():
    return "Sunny"

result = get_weather()
print(result)
# <coroutine object get_weather at 0x...>   ← KHÔNG PHẢI "Sunny"!
```

Muốn nó thực sự chạy và lấy được kết quả thật, phải dùng `await`:

```python
result = await get_weather()
print(result)
# "Sunny"   ← giờ mới đúng
```

Ghi nhớ:

```text
async def   → khai báo "hàm này CÓ THỂ tạm dừng giữa chừng để nhường CPU cho việc khác"
await       → "chạy nó thật sự, và nếu nó cần chờ I/O thì nhường CPU trong lúc chờ"
```

---

## 3. So Sánh Có/Không Có Async — Bằng Số Liệu Cụ Thể

Giả sử có 2 việc: lấy thời tiết (mất 3 giây, phải chờ mạng) và cộng 2 số (gần như tức thì).

**Không async (code sync bình thường):**

```python
def get_weather():
    time.sleep(3)
    return "Sunny"

def add(a, b):
    return a + b

get_weather()   # chạy 3s, CHIẾM CPU/thread suốt lúc đó
add(1, 2)       # phải đợi get_weather() xong mới tới lượt, dù chỉ cần vài micro-giây
```

```text
Tổng thời gian: ~3 giây (add phải chờ dù bản thân nó siêu nhanh)
```

**Có async:**

```python
import asyncio

async def get_weather():
    await asyncio.sleep(3)   # "chờ 3s" nhưng NHƯỜNG CPU trong lúc chờ
    return "Sunny"

async def add(a, b):
    return a + b

async def main():
    task1 = asyncio.create_task(get_weather())   # bắt đầu chạy, không block
    task2 = asyncio.create_task(add(1, 2))       # chạy NGAY trong lúc task1 đang "chờ mạng"
    print(await task2)   # "3" — xong gần như ngay lập tức
    print(await task1)   # "Sunny" — xong sau 3 giây
```

```text
task2 (add) không phải xếp hàng sau task1 (get_weather) — nó chạy xong trước, dù được tạo sau.
Đây chính là lợi ích của async: việc nhanh không bị việc chậm chặn đường.
```

---

## 4. Quên `await` Thì Sao? — Lỗi Âm Thầm, Không Crash

Đây là lỗi dễ mắc nhất khi mới học async, vì Python **không báo lỗi ngay**:

```python
async def check_stock(item_id):
    await asyncio.sleep(1)     # giả lập gọi API kiểm tra tồn kho
    return False                # hết hàng

# SAI — quên await
result = check_stock(101)
if result:
    print("Còn hàng, tiến hành đặt")
# result lúc này là <coroutine object check_stock ...>, KHÔNG PHẢI False
# object nào cũng "truthy" (khác None/False/0/[]) → if result: LUÔN True
# → in ra "Còn hàng, tiến hành đặt" dù hàng đã HẾT — API còn chưa từng được gọi!
```

```python
# ĐÚNG
result = await check_stock(101)
if result:
    print("Còn hàng, tiến hành đặt")
# result = False thật → không in gì, đúng logic
```

Quy tắc: **mọi lời gọi tới 1 async function đều phải có `await` đứng trước**, nếu không sẽ có bug im lặng, rất khó phát hiện vì không có traceback nào báo lỗi.

---

## 5. Vì Sao Hàm Gọi Hàm Async Cũng Phải Là Async? (Async Lan Truyền Ngược)

```python
async def call_external_api():
    await asyncio.sleep(2)
    return {"status": "ok"}

# Muốn viết 1 hàm "bọc" lại call_external_api để dùng ở nhiều nơi:
def wrapper():                       # SAI — def thường
    return await call_external_api()  # SyntaxError! await chỉ hợp lệ trong async def

async def wrapper():                 # ĐÚNG
    return await call_external_api()
```

Quy tắc cứng của Python: **`await` chỉ hợp lệ bên trong `async def`**. Nếu hàm A cần `await` một hàm async B, thì A cũng buộc phải là `async def` — dù bản thân A không "chậm" gì cả, chỉ đơn giản là chuyển tiếp lệnh gọi.

---

## 6. `sync_to_async` — Cầu Nối Khi Cần Gọi Code Sync Từ Trong Async

Vấn đề: nhiều thư viện/code cũ (đặc biệt là Django ORM truyền thống) viết theo kiểu sync — không phải `async def`. Ví dụ:

```python
def get_user_from_db(user_id):        # hàm sync bình thường, không async
    # giả lập query database
    return {"id": user_id, "name": "Alice"}
```

Không thể `await` trực tiếp 1 hàm sync:

```python
async def handler(user_id):
    user = await get_user_from_db(user_id)   # SAI — TypeError: object dict can't be used in 'await'
```

`sync_to_async` (từ thư viện `asgiref`) bọc hàm sync đó lại thành 1 coroutine giả — nó chạy hàm sync thật trong 1 thread pool riêng (không chiếm event loop chính), rồi trả kết quả về qua `await`:

```python
from asgiref.sync import sync_to_async

async def handler(user_id):
    user = await sync_to_async(get_user_from_db)(user_id)   # ĐÚNG
    return user
```

Đọc cú pháp: `sync_to_async(get_user_from_db)` tạo ra 1 "bản async" của `get_user_from_db`, rồi gọi nó với `(user_id)` như bình thường, rồi `await` để lấy kết quả thật.

---

## 7. `sync_to_async` KHÔNG Làm Request Này Nhanh Hơn — Nó Bảo Vệ Request KHÁC

Đây là chỗ dễ hiểu nhầm nhất. Nhìn lại dòng cuối mục 6:

```python
user = await sync_to_async(get_user_from_db)(user_id)
```

**Điều không đổi:** đã dùng `await`, dòng code NGAY SAU nó vẫn phải chờ tới khi có kết quả mới chạy tiếp — y hệt gọi sync bình thường, request này không hề nhanh hơn.

**Câu hỏi đúng cần đặt ra không phải** "request này có phải chờ không" (chắc chắn có) — mà là **"trong lúc request này chờ, những request KHÁC (của user khác) có bị ảnh hưởng không"**.

### Mô hình: Nhiều user dùng CHUNG 1 "luồng chính", không phải mỗi user 1 luồng riêng

```text
Model CŨ (Django sync truyền thống) — mỗi request 1 thread riêng:
User A → thread riêng của A
User B → thread riêng của B      ← A chiếm thread của A không ảnh hưởng B, vì thread khác nhau
User C → thread riêng của C

Model ĐANG DÙNG (async, ninja-extra) — nhiều user CHUNG 1 "luồng chính" (event loop):
User A ─┐
User B ─┼─→  1 EVENT LOOP DUY NHẤT xử lý xen kẽ cả 3 request
User C ─┘    ← A, B, C dùng CHUNG 1 luồng — nếu luồng này bị 1 người "chiếm cứng", 2 người còn lại bị kẹt theo
```

Đây là lý do async "nguy hiểm" hơn sync ở đúng điểm này: sync mỗi user có thread riêng, ai chiếm thread của mình cũng không ảnh hưởng người khác; async thì nhiều user hoàn toàn không liên quan tới nhau lại đang dùng chung 1 event loop.

### So sánh có/không có `sync_to_async` — timeline 2 request của 2 user khác nhau

Giả sử `get_weather()` (mục 1, mất 3 giây vì chờ DB/network) là request của **user A**, và `add(1, 2)` (gần như tức thì) là request của **user B** — 2 user không liên quan gì tới nhau, chỉ tình cờ request tới gần cùng lúc.

**Nếu gọi hàm sync (giả sử `time.sleep(3)`) trực tiếp trên event loop, không qua `sync_to_async`:**

```text
t=0s   Request A tới, event loop bắt đầu chạy time.sleep(3) TRỰC TIẾP trên event loop
       → event loop bị "kẹt cứng" 3 giây, không làm được gì khác trong lúc này
t=0s   Request B tới — nhưng event loop đang bị A CHIẾM → B phải XẾP HÀNG, chưa chạy được
t=3s   A xong, event loop RẢNH, mới bắt đầu chạy B
t=3s+ε B xong
```

→ B bị trễ gần 3 giây, dù bản thân B chỉ cần vài micro-giây — vì event loop (duy nhất) bị A giữ chặt suốt lúc chờ.

**Với `await sync_to_async(...)()` (cách đúng):**

```text
t=0s   Request A tới, gặp await sync_to_async(slow_func)()
       → sync_to_async KHÔNG tự chạy slow_func trên event loop chính
       → nó giao việc đó cho 1 THREAD PHỤ (lấy từ thread pool riêng)
       → event loop chính, sau khi giao việc xong, LẬP TỨC RẢNH — không đứng chờ tại đó
       → request A được "gác lại" (tạm dừng), event loop rảnh tay làm việc khác
t=0s   Request B tới — event loop đang RẢNH (không bị A chiếm) → chạy B ngay
t=0s+ε B xong — KHÔNG bị ảnh hưởng gì bởi việc A vẫn còn đang chờ
t=3s   Thread phụ chạy xong slow_func, báo lại cho event loop
t=3s   Event loop quay lại tiếp tục request A, đúng ngay sau dòng await
```

→ B xong gần như ngay lập tức, không phải chờ A — vì việc chờ (3 giây) được đẩy sang 1 thread khác, không chiếm event loop chính.

### Tóm gọn — phân biệt 2 điều khác nhau

| | Request A (chính nó) có phải chờ? | Request B (user khác) có bị kẹt theo? |
|:---|:---|:---|
| Gọi sync trực tiếp trên event loop | Có, 3s | **Có** — B bị kẹt theo, vì event loop duy nhất bị A giữ |
| `await sync_to_async(...)()` | Có, vẫn 3s — A không nhanh hơn | **Không** — B chạy bình thường, vì việc chờ nằm ở thread phụ |

`await` = "dòng code sau nó, trong request này, phải chờ" — không đổi, luôn đúng. "Không chặn event loop" = "request khác không bị bắt chờ theo" — đây là lợi ích thật của `sync_to_async`, khác hẳn ý "request này chờ hay không".

> Lưu ý: server thật thường chạy nhiều **worker** (process) song song, mỗi worker có 1 event loop riêng. Nếu A rơi vào worker 1 và chiếm event loop đó, chỉ request khác cũng rơi vào **đúng worker 1** cùng lúc mới bị ảnh hưởng — request rơi vào worker 2/3/4 hoàn toàn bình thường, không biết gì về việc worker 1 đang bị kẹt. Không phải "1 user 1 luồng riêng" (đó là model sync cũ), cũng không phải "toàn bộ hệ thống, mọi user" bị ảnh hưởng — mà là mọi request đang cùng rơi vào đúng 1 worker đó, tại đúng thời điểm đó.

---

## 8. Có Bắt Buộc Phải Làm Vậy Không? — Django Tự Chặn, Không Chỉ "Nên"

Câu trả lời: **bắt buộc — nhưng chỉ bắt buộc bên trong `async def`**, không phải "cả hệ thống".

### Django tự raise lỗi, không phải tự giác làm cho tốt

Từ bản Django 3.1+, nếu code trong `async def` gọi thẳng 1 thao tác sync-blocking (VD: ORM query kiểu cũ) mà không bọc `sync_to_async`, Django **tự raise `SynchronousOnlyOperation`** — chặn hẳn không cho chạy, không phải warning hay chạy chậm mà crash ngay:

```python
async def suggest_titles(self, request, payload):
    persona = PersonaSetting.objects.get(id=payload.persona_id)   # ❌ SynchronousOnlyOperation
```

Cơ chế bảo vệ này có thể tắt qua biến môi trường `DJANGO_ALLOW_ASYNC_UNSAFE` — nhưng đây là "cửa thoát khẩn cấp" cho dev console/script chạy 1 lần, không phải cách dùng cho code chạy thật.

### Phạm vi: chỉ trong `async def`, không phải toàn bộ codebase

Nếu 1 project trộn cả code cũ (`def` thường) và code mới (`async def`) — như đã học ở bài 10 (1 project có thể vừa có DRF, vừa có ninja-extra):

```text
Code trong async def   → BẮT BUỘC bọc sync_to_async (hoặc dùng ORM async gốc) khi đụng I/O sync
Code trong def thường  → KHÔNG cần gì cả, gọi ORM/API sync trực tiếp như trước — không lỗi, không cần đổi
```

Lý do: `def` thường không chạy trên event loop async — mỗi request của nó được cấp riêng 1 thread (Django tự lo phần bridge này). Không phải "chuyển hết code cũ sang async" — chỉ áp dụng cho code mới viết trong `async def`.

### 2 cách xử lý (đã học ở mục 6), không chỉ 1 cách

```python
# Cách 1 — bọc sync_to_async (dùng cho code sync có sẵn từ trước, tiện hơn viết lại từ đầu)
result = await sync_to_async(some_sync_function)()

# Cách 2 — dùng thẳng API async gốc, nếu viết mới hoàn toàn (không phải gọi lại code cũ)
obj = await Model.objects.aget(id=...)   # .aget()/.acreate()/.afirst()... có sẵn, không cần bọc gì
```

### Không chỉ ORM/DB — áp dụng cho MỌI thao tác blocking khác

Quy tắc này không riêng cho database — **bất kỳ thao tác nào chờ I/O theo kiểu sync** (đọc file, gọi HTTP bằng thư viện sync, gọi 1 SDK sync) đặt trong `async def` đều gặp đúng vấn đề y hệt, cần xử lý y hệt (bọc `sync_to_async`, hoặc dùng bản async của thư viện đó nếu có).

> Thực tế: 1 service AI trong `leadplusone_api` dùng `AsyncOpenAI` (bản async của SDK OpenAI) chứ không dùng `OpenAI` (bản sync) — cùng lý do: gọi API AI cũng là I/O cần async-safe khi code đang nằm trong `async def`, không riêng gì database.

---

## 9. `async def` Là Lựa Chọn, Không Phải Ninja-extra Ép Buộc

Điểm cần đính chính ngay: **ninja-extra cho phép trộn cả `def` (sync) và `async def` trong cùng 1 Controller** — không bắt buộc mọi method phải async. Đã verify source `ninja/operation.py` (dòng 434-435): Ninja tự kiểm tra `is_async(view_func)` cho từng method riêng lẻ, xử lý khác nhau tùy kết quả — không phải "cả Controller phải đồng nhất 1 kiểu".

```python
@api_controller("/tasks")
class TaskController(ControllerBase):
    def list_tasks(self, request):                             # sync — HỢP LỆ trong ninja-extra
        return {"tasks": list(Task.objects.all().values())}    # gọi ORM trực tiếp, không lỗi gì

    async def create_task(self, request, payload: TaskCreateSchema):   # async — cũng hợp lệ
        ...
```

### Vậy vì sao 1 controller thật lại viết TOÀN BỘ method là `async def`?

Không phải do ninja-extra ép — mà là **lựa chọn** của người viết, vì các method đó (VD: gợi ý tiêu đề bằng AI) đều phải chờ 1 service ngoài trả lời (có thể mất vài giây) — đây là công việc "chờ I/O lâu, CPU không làm gì cả", đúng kiểu việc `async` giải quyết tốt nhất.

Chuỗi nhân quả đúng:

```text
Project CHỌN viết async def (vì cần await gọi service chậm, VD gọi AI)
        ↓ hệ quả bắt buộc, không phải do ninja-extra ép
Trong async def, đụng DB phải qua sync_to_async / ORM async (quy tắc cứng của Python, mục 6)
```

KHÔNG phải: "ninja-extra ép mọi method phải async def".

> Thực tế: mọi method trong `article_writer.py` (project `leadplusone_api`) đều là `async def` — không phải vì framework ép, mà vì mọi method đó ít nhiều đều dẫn tới việc gọi AI (chậm), nên người viết chọn nhất quán 1 kiểu cho cả file.

### Vì sao code sync (DRF) không gặp vấn đề "chặn luồng chính"?

Không phải vì DRF "có cơ chế bảo vệ khác" — mà vì **Django tự động lo việc này ở tầng dispatch, cho MỌI view sync**, không riêng gì DRF. Đã verify trực tiếp source Django (`django/core/handlers/base.py`, method `_get_response_async`):

```python
wrapped_callback = self.make_view_atomic(callback)
# If it is a synchronous view, run it in a subthread   ← comment gốc của Django
if not iscoroutinefunction(wrapped_callback):
    wrapped_callback = sync_to_async(wrapped_callback, thread_sensitive=True)
```

Django tự kiểm tra: view/method là `def` thường → tự bọc `sync_to_async(...)` cho toàn bộ hàm đó, tự đẩy request này chạy trên 1 thread riêng (mượn từ thread pool) — **y hệt model "mỗi user 1 thread riêng"** đã học ở mục 7. Không cần tự làm gì cả — Django làm hộ, ở tầng nhận request, trước khi gọi tới view.

Vậy 2 kiểu chạy song song thật trong cùng 1 server:

```text
Endpoint async def   → chạy trên event loop chính, CHIA SẺ với các request async khác
Endpoint def thường  → Django tự bọc, chạy trên 1 thread RIÊNG (mượn từ pool) — không đụng event loop chính
```

### Khi nào nên dùng `async def`, khi nào `def` thường vẫn ổn

| Nên dùng `async def` khi | `def` thường vẫn ổn khi |
|:---|:---|
| Endpoint chủ yếu chờ I/O (gọi AI, gọi API ngoài, query chậm) | Endpoint chủ yếu tính toán CPU — không có gì để "chờ", async không giúp gì |
| Cần chịu tải nhiều request cùng lúc, mỗi request chờ lâu | Endpoint đơn giản, nhanh, ít người gọi cùng lúc |
| Đang viết code mới, thoải mái dùng `sync_to_async`/ORM async | Chỉ có SDK/lib bản sync (không có bản async) — dùng async vẫn phải bọc thêm, phức tạp hơn mà lợi ích không rõ nếu ít người dùng cùng lúc |

**Lưu ý quan trọng: async không làm 1 request chạy nhanh hơn** — bản thân việc chờ AI 3 giây vẫn là 3 giây, không rút ngắn được. Async chỉ giúp server chịu được nhiều request cùng lúc hơn (không cần 1 thread riêng cho mỗi request đang chờ), không giúp từng request riêng lẻ nhanh hơn.

### Flow nghiệp vụ có khác gì không?

**Không.** Các bước nghiệp vụ (check đăng nhập → check quyền/hạn mức → gọi service ngoài → cập nhật DB → trả kết quả) giống hệt nhau dù viết `def` hay `async def` — thứ tự, điều kiện, dữ liệu không đổi gì cả. Khác duy nhất nằm ở tầng hạ tầng bên dưới: request chạy "trên event loop chính, chia sẻ với người khác" hay "trên 1 thread riêng, không chia sẻ ai" — điều này vô hình với người đọc code nghiệp vụ, chỉ ảnh hưởng hiệu năng/khả năng chịu tải của server.

---

## 10. Chi Phí Thật — Sync Tốn 1 Thread OS Nguyên Hàm, Async Chỉ Tốn "Chỗ Ngồi Ảo" Lúc Chờ

Mục 3 đã nói async giúp "chịu tải nhiều request hơn" — mục này trả lời cụ thể: **tốn tài nguyên gì**, và **endpoint không async thì sao** (câu hỏi trực tiếp của bạn).

### 1 Server Chạy Nhiều "Luồng Chính" Độc Lập, Không Phải 1

1 server thật không chỉ có 1 event loop duy nhất — nó thường chạy nhiều **worker process** song song (mỗi worker = 1 process riêng của hệ điều hành), và mỗi worker có 1 event loop độc lập của riêng nó:

```text
Giả sử server chạy 4 worker process song song
→ 4 "luồng chính" (event loop) độc lập, cùng chạy đồng thời, không chia sẻ với nhau
→ 100 user gửi request cùng lúc → chia đều vào 4 worker đó (~25 user/worker)
→ Mỗi worker không nhận "1 user 1 chỗ" — nhận cả chục request CÙNG LÚC,
  xử lý xen kẽ nhau, vì đa số thời gian là CHỜ (I/O), không tốn CPU thật lúc chờ
```

Số lượng worker cụ thể là quyết định vận hành/hạ tầng (không thuộc phạm vi bài này) — điều cần nhớ chỉ là: **có nhiều event loop độc lập chạy song song, mỗi request rơi vào đúng 1 trong số đó**, không phải toàn bộ hệ thống chỉ có 1 luồng chính duy nhất.

### Endpoint `async def` — chỉ nhường event loop lúc CHỜ, không cần thread riêng

```text
Chạy trên event loop chính SUỐT quá trình — chỉ NHƯỜNG event loop đúng lúc đang
await I/O (gọi AI, query DB...). Lúc tính toán bình thường vẫn dùng event loop,
nhường lại NGAY khi xong đoạn chờ. Không cần thread OS riêng chỉ để "đứng chờ".
```

### Endpoint `def` thường — Django tự bọc, nhưng tốn 1 thread OS THẬT, suốt cả hàm

Đã verify tiếp source Django (`django/core/handlers/asgi.py:161`):

```python
async with ThreadSensitiveContext():
    await self.handle(scope, receive, send)
```

Dòng này chạy 1 lần cho **mỗi request mới tới** — mỗi request được cấp 1 `ThreadSensitiveContext` riêng, và bên trong là 1 thread OS thật riêng. Ghép với điều đã học ở mục 8 (Django tự `sync_to_async(callback)` nếu callback là `def` thường): với endpoint sync, **toàn bộ hàm từ đầu tới cuối** (không chỉ đoạn đụng DB) chạy trên 1 thread OS thật, riêng cho request đó, tách hẳn khỏi event loop chính:

```text
Request tới → Django LẬP TỨC giao nguyên hàm cho 1 thread OS riêng
            → thread đó CHIẾM GIỮ suốt từ đầu tới cuối hàm (không nhường gì cả,
              vì code sync không biết gì về async/await)
            → event loop chính rảnh ngay từ đầu, nhưng phải có ĐỦ thread OS
              để cấp cho từng request đang chạy
```

### So sánh trực tiếp — 100 request cùng lúc, trong 1 worker process

```text
100 request → endpoint ASYNC:
    Chia sẻ 1 event loop, việc "chờ" gần như miễn phí (không tốn thread OS)
    → xử lý xen kẽ ổn, không cần 100 thread thật.

100 request → endpoint SYNC (giả sử):
    Request 1 → Django cấp thread OS #1, chiếm giữ suốt thời gian chạy
    Request 2 → Django cấp thread OS #2, chiếm giữ suốt thời gian chạy
    ...
    Request 100 → Django cấp thread OS #100
    → Cần THẬT 100 thread OS cùng lúc, chỉ trong 1 worker process đó.
```

Thread OS thật (khác coroutine ảo của async) tốn RAM + có giới hạn hệ điều hành — không "rẻ" như 1 coroutine đang chờ. Nếu request thứ 101 tới đúng lúc máy đang chật vật tạo thread mới (giới hạn RAM/OS) → đây mới là chỗ có thể thật sự nghẽn, khác hẳn cơ chế "chia sẻ event loop" của async.

### Trả lời trực tiếp: endpoint không async thì sao?

**Vẫn chạy đúng, ra kết quả đúng** — Django tự lo hết, không cần tự viết `sync_to_async` gì bên trong hàm sync đó. Khác biệt chỉ nằm ở **khả năng chịu tải đồng thời**: sync tốn 1 thread OS thật/request, chiếm giữ suốt cả quá trình xử lý; async chỉ tốn "1 chỗ ngồi ảo" trên event loop, rẻ hơn rất nhiều khi có nhiều request cùng chờ I/O lâu — đúng lý do các endpoint gọi AI (chờ lâu) nên chọn `async def`: nếu viết sync, sẽ tốn rất nhiều thread OS thật chỉ để... đứng chờ.

---

## 11. Đối Chiếu Nhanh Với File Thật (`article_writer.py`)

Chỉ để thấy các khái niệm trên trông thế nào trong 1 project thật — không cần hiểu toàn bộ file, chỉ nhìn 2 dòng:

```python
# article_writer.py, dòng 199
ai_response, meta = await self._execute_ai(user_id, payload, ...)
```

```text
self._execute_ai(...)  → là 1 async def (mục 5: vì bên trong nó có await gọi tiếp 1 async khác)
await ở trước           → bắt buộc, nếu thiếu thì ai_response sẽ là coroutine object (mục 4),
                          không phải kết quả AI thật
```

Và 1 dòng khác dùng `sync_to_async` (mục 6) để gọi 1 class có sẵn, viết sync từ trước:

```python
organization_id, error = await sync_to_async(guard.pre_check)()
```

`guard.pre_check` là method sync bình thường (không phải `async def`), nên phải bọc `sync_to_async(...)` giống hệt ví dụ `get_user_from_db` ở mục 6.

---

## 12. Kết Luận

Cần chốt:

- `async def` tạo ra coroutine — gọi không chạy ngay, phải có `await` mới thực sự chạy và lấy được kết quả thật.
- Lợi ích: trong lúc 1 tác vụ đang chờ I/O (network, DB...), chương trình tranh thủ chạy việc khác thay vì đứng đợi.
- Quên `await` là bug im lặng: biến nhận về là coroutine object (luôn truthy), không phải giá trị thật — code chạy tiếp với data sai mà không có lỗi nào báo.
- Hàm A gọi `await` hàm async B thì A cũng buộc phải là `async def` (async lan truyền ngược lên trên).
- `sync_to_async(sync_func)` là cầu nối để gọi 1 hàm sync (thư viện cũ, ORM sync...) từ trong 1 hàm async, mà không chặn toàn bộ chương trình.
- **`sync_to_async` không làm request hiện tại nhanh hơn** (nó vẫn chờ đúng số thời gian) — cái nó bảo vệ là **request của user khác đang dùng chung 1 event loop** (cùng 1 worker), không bị kéo theo chờ. Đây là khác biệt giữa "request này tự chờ" và "request khác bị kẹt theo" — 2 câu hỏi khác nhau, dễ nhầm làm 1 (mục 7).
- **Không phải "nên" mà là Django bắt buộc**: gọi thao tác sync-blocking trực tiếp trong `async def` (không bọc `sync_to_async`/không dùng API async gốc) khiến Django tự raise `SynchronousOnlyOperation`, chặn hẳn không cho chạy — nhưng chỉ bắt buộc bên trong `async def`, code `def` thường (kiểu cũ) không bị ảnh hưởng, không cần đổi gì. Áp dụng cho mọi I/O sync-blocking, không riêng ORM/DB (mục 8).
- **`async def` là lựa chọn, không phải ninja-extra ép buộc** — 1 Controller được trộn cả `def` và `async def` (đã verify source). Chọn `async def` khi endpoint chủ yếu chờ I/O lâu (gọi AI, API ngoài); `def` thường vẫn ổn cho endpoint nhanh/tính toán CPU. DRF (sync) không gặp vấn đề "chặn luồng chính" không phải vì có cơ chế riêng — Django tự bọc `sync_to_async(thread_sensitive=True)` cho MỌI view sync ở tầng dispatch, tự cấp 1 thread riêng cho mỗi request đó (đã verify source Django). Async không làm 1 request nhanh hơn, chỉ giúp server chịu tải nhiều request hơn — và flow nghiệp vụ hoàn toàn không đổi giữa `def`/`async def`, chỉ khác tầng hạ tầng vô hình với code đọc được (mục 9).
- **Chi phí thật, cụ thể là tốn gì**: server thường chạy nhiều worker process song song, mỗi worker = 1 event loop riêng, mỗi request rơi vào đúng 1 worker. Endpoint `async def` chỉ nhường event loop lúc chờ I/O — không tốn thread OS để "đứng chờ". Endpoint `def` thường được Django tự bọc, nhưng **toàn bộ hàm** (không riêng đoạn đụng DB) chạy trên 1 thread OS thật, chiếm giữ suốt cả quá trình — 100 request sync cùng lúc cần thật 100 thread OS (tốn RAM, có giới hạn OS), còn 100 request async chia sẻ rẻ trên 1 event loop. Endpoint không async vẫn chạy đúng, không cần sửa gì — khác biệt chỉ ở khả năng chịu tải (mục 10).
