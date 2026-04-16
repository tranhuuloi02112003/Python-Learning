# Tạo venv - Bước theo bước

## Mục tiêu

Tạo môi trường ảo riêng cho project mà không sợ lầm lẫn.

## Các bước

### Bước 1: Mở terminal

Cd vào thư mục project của bạn.

```bash
cd /path/to/your/project
```

### Bước 2: Tạo venv

```bash
python3 -m venv venv
```

Giải thích:

- `python3`: chương trình Python.
- `-m venv`: module tạo virtual environment.
- `venv`: tên thư mục (có thể đặt tên khác, nhưng `venv` là phổ thông nhất).

### Bước 3: Kích hoạt venv

**Trên macOS/Linux:**

```bash
source venv/bin/activate
```

**Trên Windows:**

```bash
venv\Scripts\activate
```

Dấu hiệu venv đã hoạt động:

- Terminal sẽ hiển thị `(venv)` ở đầu dòng.
- Hoặc kiểm tra bằng: `echo $VIRTUAL_ENV`

### Bước 4: Cài thư viện

```bash
pip install requests django flask
```

Nếu làm đúng bài thực hành phase A, bạn có thể cài riêng `requests` trước:

```bash
pip install requests
python3 -c "import requests; print(requests.__version__)"
```

Giải thích:

- `pip install requests`: cài thư viện `requests` vào đúng môi trường đang activate.
- `python3 -c "import requests; print(requests.__version__)"`: in version của `requests` để kiểm tra thư viện đã cài đúng.

Hoặc từ file đã lưu trước:

```bash
pip install -r requirements.txt
```

### Bước 5: Ghi lại thư viện đã cài

```bash
pip freeze > requirements.txt
```

### Bước 6: Tắt venv khi xong

```bash
deactivate
```

### Bước 7: Xóa và tạo lại venv để luyện quy trình

```bash
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -c "import requests; print(requests.__version__)"
```

Giải thích:

- `rm -rf venv`: xóa môi trường cũ.
- `python3 -m venv venv`: tạo lại môi trường mới.
- `pip install -r requirements.txt`: cài lại thư viện từ file đã lưu.
- Lệnh `import requests; print(requests.__version__)`: xác nhận sau khi tạo lại vẫn dùng được `requests`.

## Quy trình thu gọn (nhớ nhanh)

```bash
cd project_folder
python3 -m venv venv
source venv/bin/activate
pip install requests
python3 -c "import requests; print(requests.__version__)"
pip freeze > requirements.txt
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -c "import requests; print(requests.__version__)"
```

## Các lỗi hay gặp

- `command not found: python3`: Python chưa cài hoặc không trỏ đúng.
- Venv không hoạt động: Kiểm tra lại bước kích hoạt.
- `Permission denied`: Chạy lệnh dùng `bash` hoặc kiểm tra quyền thư mục.

## Khi clone project về máy mới

```bash
cd project_folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Xong, bạn đã có đúng bộ thư viện như ban đầu.
