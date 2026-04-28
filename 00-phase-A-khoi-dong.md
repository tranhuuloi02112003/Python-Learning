# TỔNG HỢP KIẾN THỨC KHỞI ĐỘNG (PHASE A)

Tài liệu này tổng hợp toàn bộ các kiến thức cốt lõi liên quan đến việc làm quen và thiết lập môi trường Python ban đầu.

---

## 1. Khái Niệm Python Cơ Bản

### Python là gì?
- Python là một ngôn ngữ lập trình bậc cao, **thông dịch (interpreted)** và đa năng. Điểm đặc trưng lớn nhất là cú pháp cực kỳ ngắn gọn và dễ đọc.
- **Thông dịch (Interpreted) vs Biên dịch (Compiled):**
  - **Biên dịch (Compiled):** Bước "Dịch ra file" thường làm trước khi chạy (giai đoạn Build). Khi "Run" là hệ thống chỉ việc kích hoạt cái file đã có sẵn đó thôi (nên tốc độ khởi chạy cực nhanh). Ví dụ: C, C++, Java.
  - **Thông dịch (Interpreted):** Bước "Dịch" và "Chạy" xảy ra cùng lúc ngay khi bạn nhấn Run. Trình thông dịch (Interpreter) sẽ vừa đọc từng dòng code vừa thực thi lập tức (Live). Ví dụ: Python, JavaScript.
  - **Tóm lại:** Biên dịch là "dịch xong xuôi trọn vẹn, đóng gói rồi mới chạy" (Pre-packaged). Còn Thông dịch là "vừa dịch vừa chạy".
- **Cú pháp thụt lề (Indentation):** Thay vì dùng dấu ngoặc `{}` như Java hay JavaScript, Python dùng khoảng trắng (thụt đầu dòng) để phân chia các khối code.
- **Dynamic Typing:** Bạn không cần khai báo kiểu dữ liệu cho biến, nhưng Python là ngôn ngữ "Strongly Typed" (không tự động ép kiểu linh hoạt nếu sai logic như cộng chuỗi và số).

### Định hướng ứng dụng
- Python đặc biệt mạnh ở mảng Backend (Django, FastAPI), Data Science (Numpy, Pandas), Trí tuệ nhận tạo (AI/Machine Learning) và Automation tool.

### Các phiên bản Python cần biết
- Lệnh kiểm tra phiên bản trên terminal: `python3 --version`
- **Thông tin phiên bản (2026):**
  - **Phiên bản ổn định trong giới doanh nghiệp hiện tại:** `Python 3.12` (rất nhiều công ty đang dùng vì độ ổn định cao và tài liệu đầy đủ).
  - **Phiên bản mới nhất:** `Python 3.14.4` (phát hành tháng 04/2026). Các bản `Python 3.15` cũng đang trong quá trình preview và thử nghiệm.

---

## 2. Môi trường Runtime

Bốn khái niệm sống còn khi lập trình dự án Python: **Interpreter, venv, pip, REPL**.

### Các thuật ngữ cốt lõi
- **Interpreter (Trình thông dịch):** Chương trình dùng để dịch và chạy code Python.
- **venv (Virtual Environment):** Môi trường ảo, cách ly thư viện riêng cho từng dự án. Đảm bảo project A và project B không bị xung đột phiên bản thư viện.
- **pip:** Công cụ quản lý và cài đặt gói thư viện (như `npm` của Node.js hay `mvn` của Java).
- **REPL:** Chế độ gõ lệnh Python trực tiếp trên terminal và thấy kết quả ngay (thường gọi ra bằng cách gõ `python3` nhấn Enter).

### Mối quan hệ giữa các thành phần
- Khi tạo dự án, bạn tạo `venv` để tạo ra một "không gian riêng".
- Bên trong `venv` đó sẽ có `Interpreter` và `pip` độc lập với hệ thống.
- Khi cài thư viện qua `pip install`, thư viện sẽ tải đúng vào môi trường bạn đang kích hoạt.

### Quy trình Setup (venv) thông dụng
```bash
# 1. Tạo môi trường ảo (đặt tên thư mục là 'venv')
python3 -m venv venv

# 2. Kích hoạt môi trường (trên macOS/Linux)
source venv/bin/activate
# (Nếu hiển thị (venv) ở đầu dòng lệnh terminal là đã thành công)

# Lệnh phụ: Kiểm tra xem đang dùng Python của máy hay của venv thiết lập
which python3 

# 3. Cài đặt thư viện mới thông qua pip
pip install requests django

# 3.1. HOẶC cài lại toàn bộ thư viện khi bắt đầu dự án được clone về máy
pip install -r requirements.txt

# 4. Lưu cấu hình các thư viện hiện tại ra file để dùng chia sẻ
pip freeze > requirements.txt

# 5. Thoát và tắt môi trường ảo
deactivate
```

---

## 3. Khắc Phục Sự Cố - Đọc hiểu Traceback

### Traceback là gì?
- **Traceback** là toàn bộ đoạn thông báo lỗi chi tiết mà Python in ra trên màn hình khi đoạn code chạy bị hỏng.
- Nó chỉ dẫn để bạn gỡ rối (Debug) dựa trên: Lỗi nằm ở file nào, tại dòng thứ mấy và loại lỗi cụ thể là gì.

### Các nhóm lỗi phổ biến kinh điển
- **TypeError:** Lỗi sai kiểu dữ liệu (Ví dụ: `age = "20" + 5` - Không thể cộng chuỗi và số nguyên chung với nhau).
- **ValueError:** Lỗi giá trị quy chiếu (Ví dụ: `int("abc")` - Cố bắt biến chữ thành số nguyên là vô lý).
- **NameError:** Tên biến chưa được định nghĩa (Ví dụ: `print(anbc)` - Gõ sai chính tả tên biến).
- **IndexError:** Truy xuất mảng vượt giới hạn (Ví dụ: mảng có 3 phần tử mà gọi `list[10]`).

### Kỹ năng đọc Traceback chuyên nghiệp
1. **Lướt xuống dòng cuối cùng:** Python luôn ghi Tên loại lỗi chính và mô tả nguyên nhân rất rõ ở phần cuối cùng của khối báo lỗi (`TypeError: can only concatenate str (not "int") to str`).
2. **Tìm chữ thư mục "File" ở trên nó:** Tiếp tục nhìn lên trên một dòng, nó sẽ báo vị trí sập dòng Code xảy ra (`File "test.py", line 3`) giúp bạn tìm đến chính xác dòng 3 để sửa đổi.
3. **Phòng ngừa:** Luôn bọc cấu trúc `try/except` để kiểm soát các vùng mã rủi ro nếu có yếu tố dữ liệu mập mờ (đặc biệt là giá trị `input()` từ người dùng nhập bậy vào).
```python
try:
    age = int(input("Nhập tuổi: "))
    print(f"Năm sinh: {2026 - age}")
except ValueError:
    print("Lỗi: Tuổi phải là số nguyên!")
```
