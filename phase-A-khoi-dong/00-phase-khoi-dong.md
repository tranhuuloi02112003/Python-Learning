# Phase Khởi Động - Tóm Tắt Nhanh

Tài liệu này gom các ý quan trọng nhất của phase Khởi động để bạn dễ ôn lại trước khi học Django và backend Python.

## 1. Mục tiêu của phase này

Sau phase này, bạn cần làm được 4 việc:

- Kiểm tra được Python đang cài trên máy.
- Dùng được REPL để thử lệnh nhanh.
- Tạo và dùng được `venv` để tách môi trường theo từng project.
- Cài package bằng `pip`, tạo `Hello World`, và chạy được file Python đầu tiên.

## 2. Python environment là gì?

Đây là bộ công cụ để bạn chạy Python trên máy:

- Python interpreter: chương trình thực thi code Python.
- `pip`: trình cài thư viện.
- `venv`: môi trường ảo cho từng project.

### Lệnh kiểm tra nhanh trên macOS

```bash
python3 --version
which python3
which pip
```

Nếu máy báo ra đường dẫn kiểu `/Users/user/venv/bin/python3` hoặc `/Users/user/venv/bin/pip` thì bạn đang dùng đúng môi trường ảo.

## 3. REPL là gì?

REPL là chế độ gõ lệnh Python trực tiếp vào terminal và nhận kết quả ngay lập tức.

### Cách mở REPL

```bash
python3
```

### Cách thoát REPL

```python
exit()
```

### Những lệnh nên thử trong REPL

```python
2 + 3
10 - 4
6 * 7
8 / 2
8 // 2
9 % 2
2 ** 3
"Hello" + " World"
str(123)
input("Tên bạn là gì? ")
```

### Ý nghĩa cần nhớ

- `+`, `-`, `*`, `/`: toán tử cơ bản.
- `//`: chia lấy phần nguyên.
- `%`: chia lấy dư.
- `**`: lũy thừa.
- `str(...)`: ép sang chuỗi.
- `input(...)`: nhận dữ liệu từ bàn phím, kết quả luôn là chuỗi.

## 4. `venv` là gì?

`venv` là môi trường ảo của Python. Nó giúp mỗi project có bộ thư viện riêng, không bị xung đột với project khác.

### Vì sao cần `venv`?

- Project A có thể cần Django phiên bản này.
- Project B có thể cần Django phiên bản khác.
- Nếu cài chung toàn máy, thư viện rất dễ đụng nhau.

### Tạo `venv`

```bash
python3 -m venv venv
```

### Kích hoạt `venv` trên macOS

```bash
source venv/bin/activate
```

### Cách kiểm tra `venv` đã hoạt động chưa

```bash
echo $VIRTUAL_ENV
which python3
which pip
```

Kết quả đúng thường sẽ có đường dẫn chứa thư mục `venv`.

### Cách tắt `venv`

```bash
deactivate
```

### Dấu hiệu dễ nhận biết

- Terminal thường hiện tên môi trường ở đầu dòng.
- `which python3` trỏ vào thư mục `venv`.
- `pip install ...` sẽ cài vào project hiện tại, không cài toàn máy.

## 5. `pip` là gì?

`pip` là trình quản lý thư viện của Python. Dùng để cài, ghi lại, và khôi phục dependencies.

### Lệnh cơ bản nhất

```bash
pip install requests
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Ý nghĩa

- `pip install requests`: cài package `requests`.
- `pip freeze > requirements.txt`: ghi toàn bộ thư viện đang cài ra file.
- `pip install -r requirements.txt`: cài lại tất cả thư viện từ file đã lưu.

### Lưu ý quan trọng

- Chỉ nên chạy `pip install` sau khi đã activate `venv`.
- Khi clone project mới về, bước đầu tiên thường là activate `venv` rồi cài dependencies từ `requirements.txt`.

## 6. Hello World là gì?

Đây là file Python đầu tiên dùng để xác nhận mọi thứ chạy được.

### Tạo file `hello.py`

```python
print("Hello World")
```

### Chạy file

```bash
python3 hello.py
```

Nếu terminal in ra `Hello World` thì bạn đã chạy Python file thành công.

## 7. File `calc.py` nhỏ để luyện input và ép kiểu

```python
a = float(input("Nhập số a: "))
b = float(input("Nhập số b: "))

print("Tổng:", a + b)
print("Hiệu:", a - b)
print("Tích:", a * b)
print("Thương:", a / b)
```

### Bài học ở đây

- `input()` luôn trả về chuỗi.
- Muốn tính toán thì phải ép kiểu sang `int` hoặc `float`.
- `print()` là cách đơn giản nhất để xem kết quả.

## 8. Checklist hoàn thành phase

- [ ] Chạy được `python3 --version`.
- [ ] Vào được REPL bằng `python3`.
- [ ] Thử được các phép toán cơ bản trong REPL.
- [ ] Tạo được `venv` bằng `python3 -m venv venv`.
- [ ] Kích hoạt được `venv` bằng `source venv/bin/activate`.
- [ ] Cài được `requests` bằng `pip install requests`.
- [ ] Lưu được thư viện ra `requirements.txt`.
- [ ] Chạy được `hello.py`.
- [ ] Chạy được `calc.py`.

## 9. Trình tự học đề xuất

1. Kiểm tra môi trường Python.
2. Làm quen với REPL.
3. Tạo và kích hoạt `venv`.
4. Cài package bằng `pip`.
5. Tạo `Hello World`.
6. Làm `calc.py`.
7. Ôn lại checklist một lần nữa.

## 10. Câu nhớ nhanh

- REPL = thử lệnh nhanh.
- `venv` = môi trường riêng cho project.
- `pip` = cài thư viện.
- `requirements.txt` = danh sách thư viện để cài lại.
- `Hello World` = kiểm tra file Python chạy được.
