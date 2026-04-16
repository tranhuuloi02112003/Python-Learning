# Tổng hợp kiến thức Python cơ bản & khác biệt cốt lõi

Tài liệu này tổng hợp các kiến thức cơ bản trong Python, đặc biệt được trích dẫn và liên hệ để giúp dễ hình dung hơn (đặc biệt nếu bạn đã quen với các ngôn ngữ định kiểu tĩnh như Java, C#, C++).

---

## Phase 1: Cấu trúc & Logic đặc trưng cơ bản

Đầu tiên là những đặc trưng cốt lõi về cú pháp khiến Python thực sự khác biệt và ngắn gọn:

### 1. Indentation (Thụt lề) thay cho phân khối `{}`

Thay vì dùng dấu ngoặc nhọn `{}` để giới hạn một khối lệnh (block of code), Python bắt buộc phải sử dụng **khoảng trắng** (indentation - thường là 4 dấu cách) ở đầu dòng. Nếu bạn thụt lề sai, chương trình sẽ báo lỗi `IndentationError` và không chạy được.

```python
# Lệnh if bắt đầu khối lệnh bằng dấu hai chấm (:) và các dòng bên trong phải thụt lề
if  10 > 5:
    print("Mười lớn hơn năm")
    print("Khối lệnh này cùng một cấp thụt lề")

# Kết thúc thụt lề nghĩa là đã ra khỏi khối lệnh của if
print("Dòng này chạy độc lập")
```

### 2. Strongly nhưng Dynamically Typed

Python là ngôn ngữ kiểu động (không cần khai báo kiểu của biến lúc khởi tạo) nhưng lại mạnh về kiểu (Strongly Typed - không tự động ép kiểu lung tung để tránh lỗi ngầm).

> _(Mở rộng: Trong Java bạn phải khai báo `String name = "Gemini"`, còn Python biến sẽ tự nhận kiểu từ giá trị gắn cho nó. Tuy nhiên, Python sẽ báo lỗi nếu bạn cố tình cộng chuỗi với số mà không ép kiểu rõ ràng)._

```python
name = "Gemini"     # string
version = 1.0       # float

# Để ghép chuỗi và số, bạn bắt buộc phải ép kiểu bằng str()
# Không thể viết: "Phiên bản " + 1.0
message = "Phiên bản " + str(version)
print(message)
```

### 3. Quy tắc đặt tên kiểu Snake_case

Convention (quy chuẩn) phổ biến nhất trong Python là dùng `snake_case` (chữ thường, các từ cách nhau bởi dấu gạch dưới) cho tên biến và tên hàm.

> _(Lưu ý: Không dùng `camelCase` như `userName` hay `calculateTotal` trừ những trường hợp đặc biệt không thể tránh)._

```python
user_name = "Nguyen Van A"
total_score = 100

def get_user_info():
    # Nội dung hàm
    pass
```

### 4. `None` thay cho `Null`

Giá trị "rỗng" hoặc "không có gì cả" trong Python được viết là `None` (chữ N viết hoa).

```python
current_user = None

if current_user is None:
    print("Chưa có user nào đăng nhập")
```

### 5. Từ khóa `pass`

Python không cho phép các khối lệnh (như ruột của `if`, `while`, `def`, `class`) bị rỗng. Nếu bạn muốn định nghĩa chúng nhưng chưa biết viết gì, phải sử dụng lệnh `pass`. Nó giống như việc "để đó, tôi sẽ làm sau" và chương trình sẽ bỏ qua lệnh này.

> _(Thay vì dùng một cặp `{}` rỗng như các ngôn ngữ khác)._

```python
def feature_in_development():
    # TODO: Sẽ code chức năng này sau
    pass

### 6. Toán tử `not` & Khái niệm Truthiness (Rỗng là False)
Trong Java, bạn dùng `!` để phủ định. Trong Python, bạn dùng từ khóa `not`. Đặc biệt, Python có khái niệm **Truthiness**: coi các giá trị "rỗng" hoặc "không" là `False` khi nằm trong câu lệnh điều kiện.

*   **Falsy values (Coi là False):** `0`, `0.0`, `""` (chuỗi rỗng), `[]` (list rỗng), `{}` (dict rỗng), `None`, `False`.
*   **Truthy values (Coi là True):** Bất cứ thứ gì có giá trị (số khác 0, chuỗi có chữ, list có phần tử...).

**So sánh phong cách viết code:**

| Tình huống | Kiểu Java/C truyền thống | Kiểu Python (Pythonic) |
| :--- | :--- | :--- |
| Kiểm tra list rỗng | `if (tasks.isEmpty())` | `if not tasks:` |
| Kiểm tra biến có giá trị | `if (user != null)` | `if user:` |

---

### 7. Các kiểu vòng lặp (Loops Comparison)

| Tình huống | Cú pháp Java | Cú pháp Python |
| :--- | :--- | :--- |
| **Duyệt phần tử** | `for (String s : list) { ... }` | `for s in list:` |
| **Lặp n lần** | `for (int i=0; i<5; i++) { ... }` | `for i in range(5):` |
| **Duyệt cả Index** | `for (int i=0; i<list.size(); i++)` | `for i, s in enumerate(list):` |
| **Vòng lặp vô tận** | `while (true) { ... }` | `while True:` |

> **Tip:** Trong Python, hạn chế dùng `range(len(list))` để lấy chỉ số, thay vào đó hãy dùng `enumerate(list)` vì nó nhanh và chuyên nghiệp hơn.

---
```

---

## Phase 2: Thao tác với String & Số (Advanced)

Xử lý chuỗi trong Python cực kỳ mạnh mẽ, ngắn gọn và "clean" so với các ngôn ngữ khác:

### 1. F-strings (String Interpolation)

Được giới thiệu từ Python 3.6, `f-strings` là cách nhúng giá trị, biến số một cách ngắn gọn, nhanh chóng và dễ đọc nhất vào chuỗi (Chỉ cần thêm chữ `f` trước chuỗi và đặt biến trong cặp ngoặc nhọn `{}`).

```python
user = "Alice"
age = 25
greeting = f"Xin chào {user}, năm nay bạn {age} tuổi."
print(greeting)
# Kết quả: Xin chào Alice, năm nay bạn 25 tuổi.
```

### 2. Multi-line String (Chuỗi nhiều dòng)

Bạn có thể dùng 3 cặp dấu nháy kép `"""` (hoặc nháy đơn `'''`) để giữ nguyên được định dạng xuống dòng, dấu phẩy, khoảng trắng... của chuỗi.

```python
sql_query = """
    SELECT id, username, email
    FROM users
    WHERE is_active = True
"""
print(sql_query)
```

### 3. Slicing (Cắt chuỗi)

Cắt một phần của chuỗi dựa theo index một cách siêu ngắn ngọn theo cú pháp `[start:stop:step]`.

```python
text = "Hello World"

# Cắt từ ký tự index 0 đến trước index 5
print(text[0:5])      # Kết quả: Hello

# Cắt từ index 6 đến hết
print(text[6:])       # Kết quả: World

# Đảo ngược toàn bộ chuỗi (kỹ thuật cực nhanh)
print(text[::-1])     # Kết quả: dlroW olleH
```

### 4. Các hàm String tiện ích

```python
message = "  Python Backend   "

print(message.strip())           # Trims space: "Python Backend"
print(message.replace(" ", "_")) # "__Python_Backend___"
print(message.upper())           # Viết hoa: "  PYTHON BACKEND   "
print("A,B,C".split(","))        # Chia theo delimiter ra List: ['A', 'B', 'C']
```

### 5. Thao tác với Số

Python phân tách rõ hai loại phép chia để tuỳ trường hợp lập trình viên sử dụng.

```python
# Phép chia lấy phần nguyên (//) và chia tạo số thập phân (/)
print(10 / 3)   # 3.3333333333333335 (Trả về Float)
print(10 // 3)  # 3 (Chia lấy phần nguyên, trả về Int)

# Số mũ (không cần gọi hàm math.pow)
print(2 ** 3)   # 8
```

---

## Phase 3: Cấu trúc dữ liệu (Collections)

Đây là những linh hồn của Backend Python dùng để quản lý luồng dữ liệu:

### 1. List (Array / ArrayList)

- **Đặc điểm:** Sắp xếp có thứ tự, có thể thay đổi (`mutable`), và chứa được nhiều kiểu dữ liệu cùng lúc.
  > **Ghi chú cho Java Dev:** Python **không phân chia** giữa mảng cố định (Array) và mảng động (ArrayList). Mọi `list` trong Python đều là mảng động, tự động co giãn kích thước. Bạn có thể coi `list` chính là một `ArrayList` cực kỳ linh hoạt.

````python
items = ["Apple", "Banana", "Cherry"]
items.append("Mango")   # Thêm vào cuối
items.insert(1, "Kiwi") # Chèn "Kiwi" vào index 1
items.remove("Banana")  # Xóa phần tử giá trị Banana
last_item = items.pop() # Lấy Mango ra và xoá khỏi list
items.sort()            # Sắp xếp tại chỗ

# List Comprehension (Đặc sản siêu tốc độ của Python)
# Lọc List hiện tại và biến đổi, chỉ với 1 dòng gọn gàng

**Công thức tổng quát (Formula):**
`new_list = [ <Hành động> for <Phần tử> in <Tập hợp gốc> if <Điều kiện lọc> ]`

*   **Hành động:** Bạn muốn làm gì với phần tử đó (vd: `x*x`, `x.upper()`).
*   **Phần tử:** Biến đại diện (tương tự `for x in numbers`).
*   **Tập hợp gốc:** List hoặc mảng dữ liệu ban đầu cần xử lý.
*   **Điều kiện lọc (Optional):** Dùng để lọc lấy các phần tử thỏa mãn.

**Ví dụ:**
```python
numbers = [1, 2, 3, 4, 5]
squares = [x * x for x in numbers if x % 2 == 0]
print(squares) # Lấy bình phương của số chẵn -> [4, 16]
````

### 2. Tuple

- **Đặc điểm:** Có thứ tự, **không thể thay đổi** (immutable). Dùng để bảo vệ cố định dữ liệu.
  > _(Liên tưởng: Một Array "chỉ đọc" hoặc dùng để lưu các hằng số toạ độ)_

```python
coordinates = (10, 20)
# coordinates[0] = 15  # LỖI: Tuple không cho phép gán lại phần tử
print(coordinates[0])    # Trả về 10
```

### 3. Dictionary (Dict)

- **Đặc điểm:** Lưu dữ liệu dạng Key-Value. Truy xuất siêu tốc thông qua key.
  > _(Liên tưởng: Tương tự như `HashMap` hoặc `ObjectJSON`)_

```python
user_info = {
    "id": 101,
    "name": "Tom",
    "role": "admin"
}

# Lấy values an toàn bằng hàm .get()
# Nếu key không tồn tại, sẽ trả về tham số mặc định thay vì báo lỗi đứng chương trình
print(user_info.get("email", "Not Found")) # Not Found

print(list(user_info.keys()))   # Lấy tất cả khoá: ['id', 'name', 'role']
print(list(user_info.values())) # Lấy tất cả giá trị: [101, 'Tom', 'admin']
```

### 4. Set (Tập hợp)

- **Đặc điểm:** Không có thứ tự, **không có phần tử trùng lặp**, xử lý biểu thức logic tập hợp rất nhanh.
  > _(Liên tưởng: Bạn hay dùng nó như `HashSet`. Set dùng `{}` giống dict nhưng không có cấu trúc theo cặp Key:Value)._

```python
unique_ids = {1, 2, 2, 3, 4, 4, 5}
print(unique_ids) # Kết quả đã tự xoá trùng: {1, 2, 3, 4, 5}

unique_ids.add(6)
unique_ids.discard(1) # Bỏ số 1 đi (khác với remove là nếu không có thì ko báo lỗi)

# Toán tử tập hợp toán học
set_A = {1, 2, 3}
set_B = {3, 4, 5}
print(set_A.union(set_B))        # Hợp A và B
print(set_A.intersection(set_B)) # Giao A và B (Những phần tử chung)
```

---

## Phase 4: Hàm & Lập trình hướng đối tượng (OOP)

### 1. Hàm (Function)

Python làm cho việc định nghĩa hàm mềm dẻo hơn đáng kể.

**Default Arguments (Tham số mặc định):**

> _(Tránh viết hàm đè - Overloading rườm rà)_

```python
def connect_db(host, port=3306, user="root"):
    return f"Connecting to {user}@{host}:{port}..."

print(connect_db("localhost"))                 # Dùng giá trị mặc định
print(connect_db("localhost", port=5432))      # Ghi đè port mặc định
```

**Trả về nhiều giá trị (Multiple Returns):**

> _(Python thực chất ngầm gói gọn vào đối tượng Tuple lại cho bạn)_

```python
def get_user_status():
    return "active", 1500  # Trả về 1 trạng thái và 1 điểm số

status, points = get_user_status() # Bóc tách (unpacking) 2 biến dễ dàng
print(f"Status: {status}, Points: {points}")
```

### 2. Python Class & OOP

Đây có lẽ là sự thay đổi cách tư duy và Convention hoàn toàn.

- **Constructor (`__init__`) và `self`:** Mọi class trong Python khởi tạo dữ liệu qua method `__init__`. Tham số chuẩn đầu tiên bắt buộc phải là `self` (đám chỉ đối tượng hiện tại).
  > _(Liên tưởng: `self` giống hệt `this` trong Java/C++, nhưng nó bắt-buộc-phải-hiện-diện rõ ràng trên danh sách tham số argument của mọi class methods nhé)._
- **Access Modifier (Private/Public):** Python thực sự **chỉ có Public**. Mọi biến và hàm nào bắt đầu với gạch dưới đơn `_name` thì mọi lập trình viên tự quy ước nó là _internal/private_, không nên dùng trực tiếp từ bên ngoài.

```python
class DatabaseConnection:
    # 1. Constructor
    def __init__(self, uri):
        self.uri = uri

        # Biến internal (chỉ nên gọi trong nội bộ class này)
        self._is_connected = False

    # 2. Truyền self mặc định cho các instance methods
    def connect(self):
        self._is_connected = True
        return f"Connected to {self.uri}"

# Sử dụng
db = DatabaseConnection("mysql://...")
print(db.connect())
```

### 3. Type Hints (Optional Static Typing)

Dù là kiểu động, các dự án Backend lớn tại Python bắt buộc dùng _Type Hinting_ (có từ Python 3.5). Nó không bắt buộc trình biên dịch, nhưng các IDE và công cụ linter sẽ dùng nó để cảnh báo lỗi y như bạn viết code kiểu tĩnh.

> _(Java developer sẽ rất thích tính năng này vì nó ngăn ngừa bug ngay khi code)._

```python
# Phải khai báo biến int, và kiểu trả về là int
def calculate_discount(price: float, discount_percent: float) -> float:
    return price * (1 - discount_percent / 100)

result = calculate_discount(100.0, 10.0)
```

---

## Phase 5: Xử lý ngoại lệ & File (Backend Core)

### 1. Try / Except / Finally

Bắt lỗi và giải phóng tài nguyên.

> _(Liên tưởng: giống hệt cụm try / catch / finally)._

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Lỗi: Không được chia cho không ({e})")
except Exception as e:
    print("Một lỗi nào đó không xác định")
finally:
    print("Luôn luôn tiến hành block này, kể cả có lỗi hay không")
```

### 2. Context Manager (`with` keyword)

Cách tốt nhất của Python để quản lý tài nguyên cần _đóng/mở_ (như Đọc/Ghi file, Database Connection). Blocks `with` cam kết rằng tài nguyên sẽ tự động đóng lại khi kết thúc khối lệnh, dù cho trong quá trình chạy có bị báo lỗi văng Exception đi chăng nữa.

> _(Liên tưởng: Giống hệt `try-with-resources` trong ngôn ngữ kiểu tĩnh)._

```python
# Tự động f.close() sau khi xong hoặc có lỗi!
with open("data.txt", "r") as f:
    content = f.read()
    print(content)
```

### 3. Import & Modules System

Mọi file Python đều là một module. Folder có file `__init__.py` sẽ trở thành một package.

```python
import math # Import cả thư viện math
from datetime import datetime # Rút trích đúng cái mình cần để code ngắn gọn

now = datetime.now()
print(now)
print(math.sqrt(16))
```

---

## Phase 6: Những cú pháp dễ "Gây lú" nhất

### 1. Phân biệt `is` và `==`

- `==` có mục đích đánh giá toán học xem giá trị có bằng nhau không.
- `is` có mục đích coi xem bộ nhớ (reference) có thực sự trỏ vào chung 1 object hay không.
  > _(Dành cho Java Dev: Sự khác biệt này trái ngược 100% với Java: ở Java `==` làm nhiệm vụ so object reference, còn `.equals()` làm việc so value. Giờ trong Python nó đảo lại: `==` giống như tính năng `.equals()` cũ)._

```python
list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a

print(list_a == list_b) # True (Vì value nội dung chúng giống nhau hoàn toàn)
print(list_a is list_b) # False (Vì chúng nằm ở 2 vùng nhớ tách biệt)
print(list_a is list_c) # True (Vì đang trỏ chung 1 biến bộ nhớ)
```

### 2. Vòng lặp For...else

Trong Python, vòng lặp `for` có đi kèm được với `else`. Block `else` này CHỈ chạy khi vòng lặp vượt qua thành công, chạy hết kết thúc **mà không hề lọt vào lệnh `break`** nào trên đường.

```python
items_to_search = ["apple", "banana", "cherry"]

for fruit in items_to_search:
    if fruit == "melon":
        print("Tới công chuyện, đã tìm thấy melon!")
        break
else:
    # Đoạn này sẽ chạy vì không nào match "melon" nên không bị break giữa chừng
    print("Chúng tôi đã duyệt sạch list nhưng chẳng tìm thấy 'melon'!")
```
