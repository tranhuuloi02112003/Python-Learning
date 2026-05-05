# TỔNG HỢP KIẾN THỨC NỀN TẢNG CÚ PHÁP (PHASE B)

Tài liệu này tổng hợp toàn bộ các kiến thức cốt lõi liên quan đến cú pháp nền tảng của Python.

---

## 1. Python Basics (Biến, Số, Chuỗi, Input/Output, Format)

### Biến và kiểu dữ liệu

- Python là ngôn ngữ kiểu động (Dynamic Typing), không cần từ khóa như `var`, `let`, `const`. Biến được khởi tạo ngay khi gán giá trị.
- Python kiểm soát kiểu chặt chẽ (Strongly Typed), không tự động ép kiểu sai logic (ví dụ cộng chuỗi với số sẽ sinh lỗi).
- Các kiểu dữ liệu cơ bản: `int` (số nguyên), `float` (số thực), `str` (chuỗi), `bool` (`True`/`False`).

### Toán tử số học

- Cơ bản: `+` (cộng), `-` (trừ), `*` (nhân).
- Các phép chia:
  - Chia lấy số thập phân: `/` (ví dụ `10 / 3 = 3.333`)
  - Chia lấy phần nguyên: `//` (ví dụ `10 // 3 = 3`)
  - Chia lấy phần dư: `%` (ví dụ `10 % 3 = 1`)
- Lũy thừa: `**` (ví dụ `2 ** 3 = 8`)

### Input/Output & Ép kiểu

- Nhập dữ liệu: `input("Prompt")`. Hàm này **luôn luôn trả về dạng chuỗi (`str`)**.
- Muốn tính toán số học, bắt buộc phải ép kiểu bằng `int()` hoặc `float()`. Ví dụ: `int(input("Nhập tuổi: "))`.
- Xuất dữ liệu: Hàm `print()`.

### Mutable và Immutable (Tính có thể thay đổi)

**Triết lý lõi:** Trong Python KHÔNG CÓ "kiểu nguyên thủy" (primitive types) như Java hay C++. **Mọi thứ đều là Object (Đối tượng)**. Kể cả một con số như `5` hay chữ `A` cũng là một Object hoàn chỉnh chiếm giữ một địa chỉ trên RAM. Chính vì vậy, Python phân loại các Object này thành 2 nhóm để quản lý sự an toàn bộ nhớ:

- **Immutable (Bất biến / Không thể thay đổi):** `tuple`, `int`, `float`, `bool`, `str`. 
  Vì số `5` là một Object, để tránh việc có code nào đó lỡ tay "sửa đổi" trực tiếp bản thể số `5` thành số `6` (làm sập logic toàn bộ chương trình), Python khóa chết chúng lại. Khi bạn thay đổi giá trị (VD: `x = 5; x = x + 1`), thực chất Python tạo ra một Object số `6` mới hoàn toàn và dán lại cái nhãn `x` sang đó. Object số `5` cũ vẫn an toàn không bị sứt mẻ.
- **Mutable (Khả biến / Có thể thay đổi):** `list`, `dict`, `set`. 
  Giống như một cái thùng chứa, bạn có thể thay đổi, thêm, bớt phần tử bên trong thùng mà không làm thay đổi địa chỉ bộ nhớ ban đầu của cái thùng đó. (⚠️ Cực kỳ cẩn thận với lỗi lây lan tham chiếu khi gán `a = b` vì cả 2 nhãn sẽ cùng trỏ vào chung 1 thùng).

#### 2 "Bảo bối" để soi thấu Object: `type()` và `id()`
Để chứng minh và kiểm tra các khái niệm trên, Python cung cấp 2 hàm built-in cực mạnh:
1. **`type(biến)`**: Trả về Class (kiểu dữ liệu) tạo ra object đó. Dùng khi bạn không chắc biến đang chứa cái gì (VD: `type(5)` trả về `<class 'int'>`).
2. **`id(biến)`**: Trả về **địa chỉ vùng nhớ (Memory Address)** của object trên thanh RAM. Số này giống như "số nhà" của đối tượng. Nhờ `id()`, ta có thể bắt bài lỗi tham chiếu:

```python
# CHỨNG MINH IMMUTABLE (Đổi giá trị -> Đổi nhà)
x = 5
print(id(x)) # VD: 1000
x = x + 1 
print(id(x)) # Sẽ ra số MỚI (VD: 1032) -> x đã dọn sang nhà mới!

# CHỨNG MINH MUTABLE (Sửa bên trong -> Nhà vẫn y nguyên)
mang = [1, 2]
print(id(mang)) # VD: 5500
mang.append(3)
print(id(mang)) # VẪN LÀ 5500 -> Không hề mua nhà mới!
```

### Xử lý Chuỗi (String) nâng cao

- **F-string:** Cách gọi biến lồng vào chuỗi nhanh gọn và đẹp nhất:
  ```python
  age = 20
  print(f"Năm nay bạn {age} tuổi")
  ```
- **Slicing:** Cắt chuỗi với cú pháp `[start:stop:step]`. Đặc biệt `[::-1]` dùng để đảo ngược chuỗi.
- **Multi-line:** Dùng ngoặc kép 3 lần `"""` để bọc các chuỗi dài xuống dòng tùy ý.

---

## 2. Control Flow (Điều khiển luồng - if, elif, else)

### Cú pháp thụt lề (Indentation)

- Chặn các khối lệnh bằng cách lùi vào 4 khoảng trắng, không dùng ngoặc nhọn `{}`. Kết thúc khối lệnh khi không còn lùi lề nữa.

### Truthy và Falsy Values

- Khác với nhiều ngôn ngữ khác, Python tự động coi các giá trị rỗng/không là `False` (Falsy) khi nằm trong lệnh điều kiện: `0`, `0.0`, `""` (chuỗi rỗng), `[]` (danh sách rỗng), `{}`, `None`.
- Dùng từ khóa `not` để phủ định (thay vì `!`). Ví dụ: `if not task_list:` (nếu mảng task_list bị rỗng).

### Phân biệt `=`, `==` và `is`

- `=`: Là toán tử **GÁN** giá trị sang một biến. (VD: `a = 5`).
- `==`: Là toán tử **SO SÁNH GIÁ TRỊ** toán học. (VD: `a == 5`).
- `is`: Là toán tử **SO SÁNH BỘ NHỚ**, kiểm tra xem 2 biến có trỏ chung vào cùng một vùng lưu trữ đối tượng hay không.

---

## 3. Loops (Vòng lặp)

### Khi nào dùng Vòng lặp nào?

- **Vòng lặp `for`**: Dùng khi **đã biết trước số lần lặp** hoặc lặp trên một danh sách/chuỗi cho sẵn.
- **Vòng lặp `while`**: Dùng khi **không biết trước số lần lặp**, vòng lặp giữ trạng thái mở cho đến khi một điều kiện sai đi (Ví dụ bắt user gõ password tới khi đúng).

### Chi tiết hàm `range()`

Dùng để tạo dãy số tự động, rất hay đi chung với lệnh `for`:

- `range(stop)`: `range(5)` tạo ra `0, 1, 2, 3, 4`.
- `range(start, stop)`: `range(2, 6)` tạo ra `2, 3, 4, 5` (lấy số bắt đầu, bỏ phiên bản số kết thúc).
- `range(start, stop, step)`: `range(1, 10, 2)` tạo ra dãy `1, 3, 5, 7, 9` (bước nhảy là 2).

### Hàm `enumerate()`

Khi cần lấy cả "giá trị" lẫn "chỉ số" (index):

```python
names = ["An", "Bình", "Chi"]
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}") # 1. An, 2. Bình, 3. Chi
```

### Điều hướng lặp (`break`, `continue`, `else`)

- `break`: Đập vỡ và thoát hẳn ra khỏi cấu trúc vòng lặp.
- `continue`: Bỏ qua các lệnh còn lại ở dưới trong vòng này, tua trở về đầu để chạy qua vòng lặp tiếp theo.
- **Cấu trúc `for...else`**: Lệnh `else` kích hoạt nếu vòng lặp `for` đã duyệt qua tất thảy mọi thứ thành công và **về đích tự nhiên mà không bị vướng phải `break`**.

---

## 4. Functions (Hàm)

Hàm được dùng để cô lập một mảnh logic/tính toán cố định vào gọi lại tại bất cứ đâu. Giúp mã nguồn gọn gàng.

### Định nghĩa và Return

- Cấu trúc sử dụng từ khóa `def`.
- Trả về biểu thức (Return).
- Nếu không có `return`, Python ngầm coi là `return None`.

### Tham số mặc định (Default arguments)

```python
def xinchao(name, age=18):
    return f"Xin chào {name}, bạn {age} tuổi"
```

Hàm này nếu gọi `xinchao("Hải")` thì `age` tự nhận số `18`.

### Trả về nhiều giá trị

Python ngầm gói các biến trả về thành đối tượng dạng Tuple.

```python
def get_user():
    return "Loi", 22
name, age = get_user() # Tự nhận giá trị gỡ ra cho hai biến cùng lúc
```

### Docstring

Dùng cặp dấu `""" """` ngay bên dưới mục `def` đầu tiên để mô tả nhanh tác dụng của cấu trúc hàm. Mọi file IDE thông minh sẽ hiện thông báo này khi bạn gọi tên hàm ở file khác.

### Tham số linh hoạt (\*args và \*\*kwargs)

- `*args` (**Splat operator** - Iterable Unpacking Operator): Nhận vào một số lượng tuỳ ý các tham số không tên (positional arguments), gói chúng thành một **Tuple**.
- `**kwargs` (**Double splat** - Dictionary Unpacking Operator): Nhận vào một số lượng tuỳ ý các tham số có tên (keyword arguments), gói chúng thành một **Dictionary**.

```python
def thong_tin(*args, **kwargs):
    print("Args:", args)     # (1, 2)
    print("Kwargs:", kwargs) # {'name': 'Loi', 'age': 22}

thong_tin(1, 2, name="Loi", age=22)
```

### Scope biến (Phạm vi truy cập - Quy tắc LEGB)

Khi một biến được gọi, Python sẽ tìm kiếm theo thứ tự ưu tiên (từ trong ra ngoài) theo nguyên tắc **LEGB**:

1. **L - Local (Cục bộ):** Biến được khai báo bên trong hàm hiện tại.
2. **E - Enclosing (Bao bọc):** Biến ở hàm bọc bên ngoài (khi dùng hàm lồng nhau closure).
3. **G - Global (Toàn cục):** Biến được khai báo ở ngoài cùng của file, ngang hàng với các hàm.
4. **B - Built-in (Tích hợp):** Các từ khóa, hàm xây dựng sẵn của Python (như `print`, `len`).

**Từ khoá `global` và `nonlocal`:**

- Biến trong hàm có thể **đọc** được biến global, nhưng không thể **ghi đè/gán lại** giá trị mới cho nó. Nếu muốn thay đổi hoàn toàn biến global từ trong hàm, bắt buộc phải dùng từ khoá `global`.
- Tương tự, dùng `nonlocal` để gán lại biến của hàm bọc bên ngoài (Enclosing).

```python
count = 0 # Biến Global

def tang_bien():
    global count
    count += 1 # Nếu không khai báo 'global count', lệnh này sẽ báo lỗi UnboundLocalError
```

_(Lưu ý: Nếu biến Global là kiểu Mutable như List hay Dict, bạn vẫn có thể `.append()` hoặc sửa phần tử bên trong từ trong hàm mà không cần từ khóa `global`)_.

**Sự khác biệt cực lớn: Python KHÔNG có Block Scope (Phạm vi khối lệnh)**

- Khác với C++, Java hay JavaScript (khi dùng `let`/`const`), các biến được sinh ra bên trong các cấu trúc rẽ nhánh hoặc vòng lặp như `if`, `for`, `while`, `try...except` **không bị giới hạn** trong không gian lùi lề đó.
- Các cấu trúc này **không tạo ra Scope mới**. Biến được tạo ra trong chúng sẽ "rò rỉ" (leak) ra ngoài và thuộc về Scope đang chứa cấu trúc đó (Global hoặc Local của hàm).

```python
items = ["A", "B", "C"]
for item in items:
    pass

# Biến 'item' KHÔNG bị tiêu hủy. Nó vẫn tồn tại ở ngoài và mang giá trị cuối cùng.
print("Phần tử cuối cùng là:", item) # In ra: "C"

# ⚠️ LƯU Ý BẪY (Gotcha):
# Nếu mảng 'items' bị rỗng ([]), vòng lặp không chạy vòng nào.
# Khi đó, câu lệnh gán nội bộ 'item = ...' không xảy ra, biến 'item' chưa từng được sinh ra.
# Gọi 'print(item)' ở ngoài sẽ bị Crash (NameError: name 'item' is not defined).
```

### Hàm ẩn danh (Lambda Function)

Hàm ngắn gọn viết trên 1 dòng, không dùng từ khóa `def`, không có return rườm rà. Thường dùng làm tham số gọi callback cho các hàm như `map()`, `filter()`, `sort()`.

```python
# Cú pháp: lambda arguments: expression
tinh_tong = lambda a, b: a + b
print(tinh_tong(3, 5)) # 8

# Thường dùng để sắp xếp List các Dictionary
users = [{"name": "An", "age": 20}, {"name": "Bình", "age": 18}]
users.sort(key=lambda u: u["age"]) # Khai báo hàm lấy tuổi để so sánh
```

### Cơ chế truyền tham số (Pass by Object Reference)

Python không dùng Pass by Value (Truyền giá trị) hay Pass by Reference (Truyền tham chiếu) kiểu như C++, mà sử dụng **Pass by Object Reference**:

- Nếu truyền vào tham số là đối tượng **Immutable** (số, chuỗi, tuple), hàm không thể tác động thay đổi đối tượng gốc ở bên ngoài.
- Nếu truyền vào tham số là đối tượng **Mutable** (list, dict), hàm có thể tác động, chỉnh sửa trực tiếp lên các phần tử của đối tượng gốc đó.

---

## 5. Style cơ bản (PEP 8 Cơ bản)

Luật viết mã của toàn bộ Pythonista:

- **Tên biến, Tên hàm:** Phải viết dạng `snake_case` (thường, cách nhau bởi gạch dưới `_`). Ví dụ: `user_name`, `calculate_sum()`.
- **Tên Lớp (Class):** Bắt buộc `PascalCase` (in hoa từng chữ). Ví dụ: `BankTransaction`.
- **Tên Hằng số:** Nào bao giờ cũng `ALL_CAPS`. Ví dụ: `DATABASE_URL`.
- **Dấu cách (Indentation):** Sử dụng 4 khoảng trắng.
- **Khúc trắng (Spacing):** Dùng 1 dấu cách bao quanh các toán tử `=`/`+`/`-` (`x = 5`). Không để dấu cách trong các lệnh có ngoặc đơn `print(val)`.
- **Cách khối (Lines):** Cần 2 dòng trắng cách giữa để phân định 2 hàm Function độc lập nhau. Mọi lệnh `import` đều quy tụ lên dòng cao nhất đầu tiên của file.

---

## 6. Debug / Traceback cơ bản

Traceback là một "Bản đồ báo lỗi", không phải hệ điều hành bắt lỗi.

- Đọc **từ dòng cuối cùng** lên để xác định chủng loại nguyên nhân:
  - `TypeError`: Bạn đang thao tác chéo (nhân chuỗi với một đối tượng bất hợp lý...).
  - `ValueError`: Tính toán trên dữ liệu rỗng nát (bắt biến chữ thành số nguyên).
  - `NameError`: Typo gọi lầm tên biến do viết sai trính tả biến ban đầu.
  - `IndexError`: Truy xuất chỉ số vượt khung array thực (mảng độ dài 3 mà đòi gọi phần tử index 10).
- Sau đó lội lên dòng chữ **File... line...** để định hình dòng nào chứa lệnh phơi diễn lỗi trên môi trường code (Editor) để bay về sửa lỗi.

---

## 7. Bài tập thực hành & Dự án (Mini Projects)

Gợi ý các yêu cầu thực hành cho Phase:

1. Thiết kế **Number Guessing Game**: Luyện logic toán `while` (lặp tới khi User đúng), if (to/nhỏ), và biến count (tính số lần đếm nháp).
2. Xây dựng **Text Menu CLI**: Giao diện chọn 1/2/3 và thoát, mỗi tính năng cấu hình vào 1 hàm `def`.
3. Bài tập ứng dụng **Mini Calculator + History**:
   - Dùng vòng lặp kiểm soát các thao tác cộng, trừ. Không rối code trong lệnh `if/else`.
   - Dùng List `[]` để gọi lệnh `.append()` nhồi lịch sử thao tác của mỗi vòng lặp lưu giấu vết.
   - Cắt lẻ logic toán vào một file cấu hình `utils.py` rồi `import` xử lý.
4. Làm thử hàm viết chức năng trả về năm nhuận `is_leap_year(year)`.
5. In ra màn hình **Bảng cửu chương 2-9** bằng vòng lặp `for` lồng nhau.
