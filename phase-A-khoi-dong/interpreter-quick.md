# Python Runtime Cơ Bản (Interpreter, venv, pip, REPL)

## 1) 4 khái niệm cốt lõi

- Interpreter: chương trình chạy code Python.
- venv: môi trường riêng cho từng project (cách ly thư viện).
- pip: công cụ cài thư viện Python.
- REPL: chế độ gõ lệnh Python trực tiếp và thấy kết quả ngay.

## 1.1) Cách gọi đơn giản

- Interpreter: chương trình chạy code Python.
- Version: phiên bản của interpreter (ví dụ Python 3.9, 3.11).
- venv: môi trường thư viện riêng biệt cho từng project.
- pip: công cụ cài đặt thư viện Python.

Câu nhớ nhanh:

- Interpreter chạy code.
- venv tách thư viện theo project.
- pip cài thư viện vào môi trường đang dùng.

## 2) Mối quan hệ giữa 4 phần

- Interpreter là "động cơ" để chạy code.
- venv là "không gian riêng" chứa interpreter + thư viện riêng.
- pip là công cụ đưa thư viện vào đúng môi trường đang dùng.
- REPL chạy trên interpreter hiện tại (hệ thống hoặc trong venv).

Kết luận quan trọng:

- Bạn đang đứng ở môi trường nào thì `pip install` cài vào môi trường đó.
- Code chạy bằng interpreter nào thì chỉ thấy thư viện của interpreter đó.

## 3) Vì sao quan trọng?

- Tránh lỗi thiếu thư viện (`ModuleNotFoundError`).
- Tránh xung đột version giữa nhiều project.
- Đảm bảo project chạy đúng môi trường đã thiết kế.

## 4) Cách kiểm tra nhanh trong terminal

```bash
which python3
python3 -c "import sys; print(sys.executable)"
echo $VIRTUAL_ENV
```

Đọc kết quả:

- Có `venv` hoặc `.venv` trong đường dẫn -> đang dùng môi trường ảo.
- Không có -> thường đang dùng interpreter hệ thống.

## 5) Quy trình tối thiểu nên nhớ

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
python3
```

Giải thích:

- Dòng 1: tạo môi trường ảo.
- Dòng 2: bật môi trường ảo.
- Dòng 3: cài thư viện vào môi trường đó.
- Dòng 4: mở REPL để thử nhanh.

## 6) Nhớ siêu ngắn

- Interpreter = máy chạy code.
- venv = hộp riêng của project.
- pip = công cụ cài thư viện.
- REPL = nơi thử lệnh nhanh.
