# Kiến trúc Thực thi của Python (Python Execution Flow)

Tài liệu này giải thích cách Python thực sự hoạt động "dưới nắp capo" (Under the hood) từ lúc nhấn nút "Run" cho đến khi xuất ra kết quả. Hiểu rõ luồng này giúp bạn viết code tối ưu hơn và xử lý triệt để các lỗi về Scope (như `UnboundLocalError`).

---

## Phần 1: Giải thích theo thuật ngữ chuyên môn (Technical)

Khi chạy một file `.py`, Python (cụ thể là trình thông dịch CPython) sẽ đi qua 2 giai đoạn chính: **Giai đoạn Biên dịch (Compilation)** và **Giai đoạn Thực thi (Execution)**.

### 1. Giai đoạn Biên dịch (Compilation - Frontend)
Python không thực thi trực tiếp mã nguồn của bạn. Đầu tiên, nó phân tích và dịch mã nguồn thành một dạng mã trung gian.
- **Lexing & Parsing:** Chia nhỏ mã nguồn thành các "từ vựng" (Token) và xây dựng Cây cú pháp trừu tượng (**AST - Abstract Syntax Tree**).
- **Static Analysis (Xây dựng Symbol Table):** Đây là bước cực kỳ quan trọng. Python quét AST để xác định **Scope tĩnh (Static Scope)** của tất cả các biến. Nếu thấy một biến được gán giá trị (`=`) ở trong một hàm, nó lập tức lưu tên biến đó vào Bảng ký hiệu (**Symbol Table**) với định danh là **Biến cục bộ (Local Variable)**. Việc khoanh vùng này được chốt cứng ngay từ lúc biên dịch.
- **Bytecode Generation:** AST được dịch thành **Bytecode** (thường có dạng file `.pyc`). Bytecode là tập hợp các chỉ thị mã máy ảo nguyên thủy, tối giản (ví dụ: `LOAD_FAST`, `STORE_FAST`, `BINARY_ADD`).

### 2. Giai đoạn Thực thi (Execution - Backend / PVM)
Bytecode được chuyển vào **Máy ảo Python (PVM - Python Virtual Machine)**. PVM là một cỗ máy hoạt động dựa trên cơ cấu ngăn xếp (Stack-based Virtual Machine).
- **Code Object:** Chứa bytecode đã được dịch ra, các hằng số và danh sách tên biến. Đây là "bản thiết kế" bất biến của chương trình.
- **Frame Object (Call Stack):** Mỗi khi một hàm được gọi, PVM tạo ra một **Frame Object** (Khung thực thi). Frame này cấp phát vùng nhớ cho biến cục bộ (Local Variables) dựa trên dữ liệu từ Symbol Table, đồng thời quản lý một ngăn xếp giá trị (Value Stack) để làm khu vực tính toán trung gian.
- **Evaluation Loop:** PVM chạy một vòng lặp vĩnh cửu, đọc lệnh Bytecode nối tiếp nhau và thao tác đẩy/rút dữ liệu (push/pop) vào Stack để thi hành logic.

---

## Phần 2: Giải thích theo góc nhìn thực tiễn (Quét -> Thực thi)

Nếu để giải thích cho một người mới hoặc báo cáo ngắn gọn, luồng thực thi của Python có thể tóm lược qua hình ảnh: **Quét (Scan)** và **Thực thi (Execute)**.

### 1. Bước 1: Quét (Scanning)
Hãy tưởng tượng trình thông dịch Python như một người **Kiến Trúc Sư**. Khi nhận bản vẽ (code của bạn), ông ấy không bắt tay xây nhà ngay mà đi quét mắt một lượt từ trên xuống dưới.

**Mục đích của việc Quét là để làm gì?**
1.  **Kiểm tra cú pháp (Syntax Check):** Quét xem có thiếu dấu ngoặc, gõ sai từ khóa hay thụt lề sai lệch không. Bắt lỗi ngay vòng gửi xe.
2.  **Định danh "hộ khẩu" (Xác định Scope):** Kiến trúc sư đi "dán nhãn" sở hữu cho các biến. Nếu thấy trong một căn phòng (Hàm) có lệnh gán (`x = 20`), ông ấy ghi chú ngay vào sổ tay: *"Từ giờ trở đi, x là đồ dùng riêng (Local) của phòng này"*. Bước này giúp Python xác định cấu trúc bộ nhớ trước, không bị "mù đường" hay phải đi dò tìm biến lúc chạy thật.
3.  **Tạo "Bản hướng dẫn lắp ráp" (Bytecode):** Cắt nghĩa những dòng code phức tạp của con người thành một danh sách các hành động siêu vi mô. Bản hướng dẫn này chỉ bao gồm các chỉ thị hạt nhân như: *Lấy ra (LOAD) -> Cất vào (STORE) -> Cộng (ADD)*.

### 2. Bước 2: Thực thi (Execution)
Sau khi Kiến trúc sư dán nhãn xong và giao cuốn Sổ tay hướng dẫn, một **Người Thợ Xây (Máy ảo PVM)** xuất hiện để thi công.
- Người thợ xây này không hiểu ngôn ngữ Python, anh ta chỉ biết nhắm mắt làm đúng thứ tự từng dòng lệnh trong Sổ tay lắp ráp (chạy Bytecode).
- Anh ta làm việc trong môi trường (Frame) đã được Kiến trúc sư đánh dấu sẵn đâu là ngăn tủ Local, đâu là tủ Global để nhấc/cất dữ liệu chính xác.

---

## 3. Ứng dụng thực tế: Giải mã lỗi `UnboundLocalError`

Hiểu được 2 bước Quét và Chạy trên sẽ giúp bạn giải thích triệt để nguyên nhân của cái bẫy kinh điển sau:

```python
x = 10
def thu_nghiem():
    print(x) # Lỗi: UnboundLocalError
    x = 20
```

**Bản chất vấn đề:**
1.  Ở **Bước Quét**, Kiến trúc sư thấy dòng `x = 20`, ông ta lập tức chốt cứng vào sổ: *"Trong hàm `thu_nghiem`, biến `x` thuộc sở hữu Local"*.
2.  Khi tiến vào **Bước Thực thi**, Người thợ chạy dòng `print(x)` trước. Anh ta đọc sổ thấy `x` là Local, nên mở ngăn tủ Local ra lấy... nhưng **ngăn tủ đang trống rỗng** (vì anh ta chưa làm tới bước gán giá trị).
3.  Anh thợ lâm vào tình thế khó xử: Đồ riêng thì chưa có giá trị, mà lại bị cấm không được chạy ra ngoài (Global) mượn biến `x = 10` vì Kiến trúc sư đã dặn `x` là của riêng phòng này rồi. Hệ quả là anh ta đình công và báo lỗi `UnboundLocalError`.
