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

## 7. Đối Chiếu Nhanh Với File Thật (`article_writer.py`)

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

## 8. Kết Luận

Cần chốt:

- `async def` tạo ra coroutine — gọi không chạy ngay, phải có `await` mới thực sự chạy và lấy được kết quả thật.
- Lợi ích: trong lúc 1 tác vụ đang chờ I/O (network, DB...), chương trình tranh thủ chạy việc khác thay vì đứng đợi.
- Quên `await` là bug im lặng: biến nhận về là coroutine object (luôn truthy), không phải giá trị thật — code chạy tiếp với data sai mà không có lỗi nào báo.
- Hàm A gọi `await` hàm async B thì A cũng buộc phải là `async def` (async lan truyền ngược lên trên).
- `sync_to_async(sync_func)` là cầu nối để gọi 1 hàm sync (thư viện cũ, ORM sync...) từ trong 1 hàm async, mà không chặn toàn bộ chương trình.
