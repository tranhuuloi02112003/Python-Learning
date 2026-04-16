# Traceback Cơ Bản - Đọc và Hiểu Lỗi Python

## 1. Traceback là gì?

**Traceback không phải lệnh**, mà là **thông báo lỗi chi tiết** mà Python in ra khi code bị lỗi.

Nó giúp bạn biết:

- Lỗi xảy ra ở file nào?
- Lỗi ở dòng số mấy?
- Lỗi là gì?

## 2. Cấu trúc của một Traceback

```
Traceback (most recent call last):
  File "test.py", line 3, in <module>
    result = age + 5
TypeError: can only concatenate str (not "int") to str
```

**Giải thích từng phần:**

- `Traceback (most recent call last)` = đây là một lỗi
- `File "test.py", line 3` = lỗi ở file `test.py`, dòng 3
- `result = age + 5` = dòng code bị lỗi (Python copy lại dòng này)
- `in <module>` = lỗi ở mức độ chương trình chính
- `TypeError: ...` = loại lỗi và chi tiết lỗi

## 3. Các Loại Lỗi Phổ Biến

| Loại Lỗi              | Khi nào xảy ra                                                 | Ví dụ                              |
| --------------------- | -------------------------------------------------------------- | ---------------------------------- |
| **TypeError**         | Kiểu dữ liệu sai (cộng chuỗi + số, gọi function trên số, v.v.) | `age + 5` (age là chuỗi)           |
| **ValueError**        | Giá trị sai (ép kiểu không thành công)                         | `int("abc")`                       |
| **NameError**         | Tên biến không tồn tại                                         | `print(naem)` (typo)               |
| **IndexError**        | Chỉ số vượt quá danh sách                                      | `list[10]` (list chỉ có 5 phần tử) |
| **KeyError**          | Khóa không tồn tại trong dictionary                            | `dict["key_không_có"]`             |
| **FileNotFoundError** | File không tồn tại                                             | `open("file_k_có.txt")`            |
| **ZeroDivisionError** | Chia cho 0                                                     | `10 / 0`                           |
| **AttributeError**    | Attribute không tồn tại                                        | `"hello".xyz()`                    |

## 4. Ví Dụ Chi Tiết

### Ví dụ 1: TypeError

```python
# Code bị lỗi
age = "20"  # Đây là chuỗi
result = age + 5
```

**Traceback:**

```
TypeError: can only concatenate str (not "int") to str
```

**Fix:** Ép kiểu sang số

```python
age = "20"
result = int(age) + 5  # ✓ Đúng
```

### Ví dụ 2: ValueError

```python
# Code bị lỗi
age = input("Tuổi: ")  # User nhập "abc"
age_int = int(age)
```

**Traceback:**

```
ValueError: invalid literal for int() with base 10: 'abc'
```

**Fix:** Kiểm tra input trước

```python
age = input("Tuổi: ")
if age.isdigit():
    age_int = int(age)
else:
    print("Vui lòng nhập số!")
```

### Ví dụ 3: NameError

```python
# Code bị lỗi
print(naem)  # Typo: "naem" thay vì "name"
```

**Traceback:**

```
NameError: name 'naem' is not defined
```

**Fix:** Kiểm tra chính tả

```python
name = "Hoa"
print(name)  # ✓ Đúng
```

### Ví dụ 4: IndexError

```python
# Code bị lỗi
my_list = [1, 2, 3]
print(my_list[10])  # Index 10 không tồn tại
```

**Traceback:**

```
IndexError: list index out of range
```

**Fix:** Kiểm tra độ dài list hoặc dùng index đúng

```python
my_list = [1, 2, 3]
print(my_list[0])  # ✓ Đúng (phần tử đầu tiên)
```

## 5. Cách Đọc Traceback Để Debug

**Bước 1:** Đọc dòng lỗi cuối cùng

- Nó báo loại lỗi là gì

**Bước 2:** Nhìn vào `File` và `line`

- Biết chính xác code nào bị lỗi

**Bước 3:** Đọc message chi tiết

- Nó thường gợi ý cách fix

**Ví dụ:**

```
TypeError: unsupported operand type(s) for +: 'str' and 'int'
```

Này nó báo: không cộng chuỗi với số → cần ép kiểu.

## 6. Cách Tránh Lỗi

- **Kiểm tra kiểu dữ liệu** trước khi dùng
- **Kiểm tra input** từ `input()` trước khi ép kiểu
- **Kiểm tra độ dài** trước khi truy cập index
- **Dùng `try/except`** khi không chắc chắn

### Ví dụ an toàn với `try/except`:

```python
try:
    age = int(input("Nhập tuổi: "))
    print(f"Năm sinh: {2025 - age}")
except ValueError:
    print("Lỗi: Vui lòng nhập số!")
except ZeroDivisionError:
    print("Lỗi: Không chia cho 0!")
```

## 7. Nhớ

- Traceback không phải lệnh, là **thông báo lỗi**
- Luôn **đọc dòng cuối cùng** trước (loại lỗi)
- Luôn **chú ý dòng số** (line number)
- Dùng **`try/except`** để xử lý lỗi an toàn
