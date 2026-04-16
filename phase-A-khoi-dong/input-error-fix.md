# Sửa lỗi do Input Sai - Hướng dẫn thực hành

## Lỗi thường gặp

Khi dùng `input()` mà user nhập sai kiểu dữ liệu.

## Ví dụ 1: Lỗi ValueError

```python
age = input("Nhập tuổi: ")
age_int = int(age)  # Nếu user nhập "abc" sẽ lỗi
print(f"Năm sau bạn {age_int + 1} tuổi")
```

**Lỗi xuất hiện:**
```
ValueError: invalid literal for int() with base 10: 'abc'
```

**Cách sửa: Kiểm tra input trước khi ép kiểu**

```python
age = input("Nhập tuổi: ")

if age.isdigit():
    age_int = int(age)
    print(f"Năm sau bạn {age_int + 1} tuổi")
else:
    print("Lỗi: Vui lòng nhập một số!")
```

## Ví dụ 2: Dùng try/except (An toàn hơn)

```python
try:
    age = input("Nhập tuổi: ")
    age_int = int(age)
    print(f"Năm sau bạn {age_int + 1} tuổi")
except ValueError:
    print("Lỗi: Vui lòng nhập một số hợp lệ!")
```

Cách này bắt mọi lỗi `ValueError` và xử lý mà không crash.

## Ví dụ 3: Lặp cho tới khi hợp lệ

```python
while True:
    age = input("Nhập tuổi: ")
    if age.isdigit():
        age_int = int(age)
        print(f"Năm sau bạn {age_int + 1} tuổi")
        break
    else:
        print("Lỗi: Vui lòng nhập một số!")
```

Khi user nhập sai, chương trình sẽ hỏi lại cho tới khi nhập đúng.

## Ví dụ 4: Kết hợp nhiều kiểm tra

```python
try:
    name = input("Tên: ")
    age = input("Tuổi: ")
    
    if not name.strip():
        print("Lỗi: Tên không được để trống!")
    elif not age.isdigit():
        print("Lỗi: Tuổi phải là số!")
    else:
        age_int = int(age)
        print(f"Xin chào {name}, năm sau bạn {age_int + 1} tuổi")
except Exception as e:
    print(f"Lỗi không xác định: {e}")
```

## Tóm tắt cách xử lý

1. **Kiểm tra trước**: Dùng `.isdigit()`, `.isalpha()`, `.strip()`.
2. **Try/except**: Bắt lỗi nếu không chắc chắn.
3. **While loop**: Lặp cho tới khi user nhập đúng.

## Bảng các hàm kiểm tra input thường dùng

| Hàm | Dùng để | Ví dụ |
|---|---|---|
| `.isdigit()` | Kiểm tra có phải số không | `"123".isdigit()` → True |
| `.isalpha()` | Kiểm tra có phải chữ không | `"abc".isalpha()` → True |
| `.isalnum()` | Kiểm tra có phải chữ+số không | `"abc123".isalnum()` → True |
| `.strip()` | Xóa khoảng trắng 2 đầu | `" hello ".strip()` → "hello" |
| `.lower()` | Chuyển thành chữ thường | `"HELLO".lower()` → "hello" |

## Điều cần nhớ

- Luôn kiểm tra input trước khi ép kiểu.
- Dùng `try/except` cho các thao tác có rủi ro.
- Dùng `while` loop để lặp cho tới khi hợp lệ.
