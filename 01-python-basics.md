# Các kiến thức cơ bản cần biết về Python

## 1. Python là gì?

Python là một ngôn ngữ lập trình bậc cao, thông dịch (interpreted) và đa năng. Điểm đặc trưng lớn nhất là cú pháp cực kỳ ngắn gọn và dễ đọc.

- **Thông dịch (Interpreted) vs Biên dịch (Compiled):**
  - **Biên dịch:** Bước "Dịch ra file" thường làm trước khi chạy (giai đoạn Build). Khi "Run" là bạn chỉ việc kích hoạt cái file đã có sẵn đó thôi (nên nó cực nhanh).
  - **Thông dịch:** Bước "Dịch" và "Chạy" xảy ra cùng lúc ngay khi bạn nhấn Run.
  - **Tóm lại:**
    - **Thông dịch:** Là "vừa dịch vừa chạy" (Live).
    - **Biên dịch:** Là "dịch xong xuôi, đóng gói rồi mới chạy" (Pre-packaged).

- **Đa nền tảng:** Python có thể chạy được trên nhiều hệ điều hành khác nhau như Windows, Mac, Linux...
- **Cú pháp thụt lề (Indentation):** Thay vì dùng dấu ngoặc nhọn {} để phân chia khối lệnh như JavaScript, Python dùng khoảng trắng (thụt đầu dòng). Đây là quy tắc bắt buộc để code chạy đúng.
- **Dynamic Typing:** Giống như JavaScript, bạn không cần khai báo kiểu dữ liệu cho biến, nhưng Python là ngôn ngữ "Strongly Typed" (không tự động ép kiểu linh hoạt như JS).

## 2. Tại sao Python lại phổ biến?

Dựa trên sự phát triển mạnh mẽ, Python trở thành ngôn ngữ hàng đầu nhờ:

- **Cú pháp đơn giản:** Gần với ngôn ngữ tự nhiên (tiếng Anh), giúp lập trình viên dễ đọc, dễ hiểu và dễ bảo trì code.
- **Tính linh hoạt:** Ứng dụng rộng rãi trong nhiều lĩnh vực từ web, desktop, game đến AI và Machine Learning.
- **Cộng đồng lớn mạnh:** Có cộng đồng lập trình viên cực kỳ lớn, sẵn sàng hỗ trợ và chia sẻ kiến thức.
- **Kho thư viện phong phú:** Cung cấp sẵn các bộ công cụ cho hầu hết mọi nhu cầu lập trình.

## 3. Tại sao nên học Python để làm Backend?

- **Hệ sinh thái Framework mạnh mẽ:**
  - **FastAPI:** Rất hiện đại, hỗ trợ Async hoàn hảo và có Type Hints giống TypeScript.
  - **Django:** "Batteries-included" (có sẵn mọi thứ từ Auth đến Admin Panel), phù hợp cho dự án lớn.
- **Khả năng tích hợp AI/Data:** Nếu ứng dụng của bạn cần các tính năng thông minh (nhận diện hình ảnh, gợi ý sản phẩm, phân tích dữ liệu), Python là lựa chọn hàng đầu.
- **Thư viện kết nối đa dạng:** Có sẵn thư viện cho gần như mọi nhu cầu từ xử lý file, kết nối DB đến bảo mật.

## 4. Python có thể làm được những gì?

Python cực kỳ đa năng, có thể ứng dụng trong:

- **Web Development (Server-side):** Xây dựng RESTful API hoặc GraphQL với các framework như **Django, Flask, FastAPI**.
- **Xử lý dữ liệu lớn (Data Science):** Phân tích dữ liệu người dùng, báo cáo biểu đồ với **NumPy, Pandas, SciPy**.
- **Machine Learning & AI:** Huấn luyện các mô hình dự báo, thị giác máy tính với **TensorFlow, PyTorch, OpenCV**.
- **Automation & Tooling:** Viết script tự động hóa quy trình deploy, cào dữ liệu (Web Scraping).
- **Ứng dụng Desktop:** Phát triển phần mềm máy tính với **Tkinter, PyQt, Kivy**.
- **IoT và Embedded Systems:** Phát triển trên các thiết bị phần cứng nhỏ với **MicroPython, CircuitPython**.
- **Game Development:** Phát triển trò chơi với **Pygame, Panda3D**.

## 5. Các kiến thức cốt lõi cần nắm vững

### Biến (Variable) là gì?

- Biến là nơi dùng để lưu trữ dữ liệu.
- Python **không có câu lệnh để khai báo** một biến (không cần dùng `var`, `let`, `const` như JavaScript).
- Một biến sẽ được tạo ra ngay khi bạn **gán một giá trị** cho nó lần đầu tiên.

### Kiểu dữ liệu & Cấu trúc dữ liệu

- **Biến cơ bản:** `int`, `float`, `str`, `bool` (Lưu ý: Boolean trong Python viết là `True` và `False`).
- **List:** Tương đương Array trong JS.
- **Dictionary (Dict):** Tương đương Object hoặc Map trong JS.
- **Tuple:** Một dạng danh sách nhưng không thể thay đổi phần tử sau khi tạo (Immutable).

### Điều khiển luồng

- Dùng `if`, `elif`, `else` cho điều kiện.
- Dùng `for ... in ...` để duyệt mảng hoặc object.
- Định nghĩa hàm bằng từ khóa `def`.

## 6. Những câu hỏi quan trọng để hiểu sâu về Python

Để thực sự làm chủ Python ở mức độ Backend Engineer, bạn nên tìm hiểu thêm các câu hỏi sau:

- Sự khác biệt giữa **Deep Copy** và **Shallow Copy** trong Python là gì?
- **Virtual Environment** (venv/conda) là gì và tại sao nó quan trọng như `node_modules`?
- Cơ chế quản lý bộ nhớ của Python (**Garbage Collection**) hoạt động như thế nào?
- **Global Interpreter Lock (GIL)** ảnh hưởng thế nào đến hiệu năng đa luồng (multi-threading)?
- Cách sử dụng **Decorators** để tối ưu hóa code Backend (ví dụ: kiểm tra quyền truy cập API)?
- Sự khác biệt về hiệu năng và cách dùng giữa `list`, `set` và `tuple`?

## 7. Gợi ý lộ trình (Keywords)

- **Cơ bản:** Python Syntax, List Comprehension, Exception Handling.
- **Trung cấp:** OOP trong Python (Class, Inheritance), Decorators, Generators.
- **Backend chuyên sâu:** FastAPI, SQLAlchemy (ORM), Pydantic (Validation), JWT Auth.

## 8. PEP 8 - Quy chuẩn viết code "sạch" (Clean Code)

PEP 8 là bộ quy tắc giúp code Python của bạn trở nên chuyên nghiệp và dễ đọc hơn. Đây là "luật bất thành văn" mà mọi Python Developer đều nên theo.

### Các quy tắc cốt lõi cần nhớ:

1.  **Naming Convention (Quy tắc đặt tên):**
    - **Biến, Hàm, Module:** Dùng `snake_case` (vd: `user_name`, `calculate_total()`).
    - **Class (Lớp):** Dùng `PascalCase` (vd: `UserAccount`, `DatabaseConnection`).
    - **Hằng số:** Dùng `ALL_CAPS` (vd: `PI`, `DATABASE_URL`).
2.  **Indentation (Thụt lề):** Sử dụng **4 dấu cách (spaces)** cho mỗi cấp bậc code.
3.  **Whitespaces (Khoảng trắng):**
    - Đặt dấu cách quanh các toán tử gán và so sánh: `x = 5`, `if a == b:`.
    - Không đặt dấu cách ngay sát bên trong dấu ngoặc: `print(x)` (thay vì `print( x )`).
4.  **Blank Lines (Dòng trống):**
    - Dùng **2 dòng trống** để ngăn cách giữa các hàm hoặc class khác nhau.
    - Dùng **1 dòng trống** bên trong hàm để tách các đoạn logic nhỏ.
5.  **Imports:** Luôn đặt các câu lệnh `import` ở ngay đầu file.

## 9. Checklist "Code đẹp"

- [ ] Tên biến có ý nghĩa (vd: `total_price` thay vì `tp`).
- [ ] Không lạm dụng chú thích (chỉ chú thích "tại sao", đừng chú thích "cái này làm gì" nếu code đã đủ rõ).
- [ ] Hàm chỉ làm 1 việc duy nhất và không quá dài.
- [ ] Đã xóa các đoạn code thừa, code test không sử dụng.

## 10. Vòng lặp trong Python (Deep Dive)

Python cung cấp các cách lặp rất mạnh mẽ và gần gũi với ngôn ngữ tự nhiên.

### 10.1. Vòng lặp `for...in` (Foreach)

Dùng để duyệt qua từng phần tử của một danh sách (List, Tuple, String, Dictionary).

```python
fruits = ["táo", "chuối", "cam"]
for fruit in fruits:
    print(fruit)
```

### 10.2. Hàm `range()` (Lặp theo số lần)

Khi muốn lặp một số lần nhất định hoặc lặp theo chỉ số (index) kiểu `for (int i=0; i<n; i++)`.

- `range(5)`: 0, 1, 2, 3, 4
- `range(2, 6)`: 2, 3, 4, 5
- `range(1, 10, 2)`: 1, 3, 5, 7, 9 (bước nhảy là 2)

```python
for i in range(3):
    print(f"Lần lặp thứ {i}")
```

### 10.3. Hàm `enumerate()` (Lấy cả chỉ số và giá trị)

Đây là cách tối ưu nhất khi bạn cần biết phần tử đó đang ở vị trí thứ mấy.

```python
names = ["An", "Bình", "Chi"]
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")
# Kết quả: 1. An, 2. Bình, 3. Chi
```

### 10.4. Vòng lặp `while`

Dùng khi bạn không biết trước số lần lặp, vòng lặp sẽ chạy đến khi điều kiện sai.

```python
count = 0
while count < 3:
    print(count)
    count += 1
```

## 11. Cơ chế quản lý bộ nhớ (Stack & Heap)

Kiến thức này giúp bạn hiểu cách Python vận hành bên dưới "mui xe" (under the hood).

### 11.1. Stack (Ngăn xếp)

- **Lưu gì:** Tên biến, tham chiếu (địa chỉ bộ nhớ) và các lần gọi hàm.
- **Đặc trưng:** Hoạt động nhanh, tự động dọn dẹp khi hàm kết thúc (return).
- **Ví dụ:** Khi bạn khai báo `x = 10`, thì cái tên `x` nằm ở Stack.

### 11.2. Heap (Bộ nhớ đống)

- **Lưu gì:** Tất cả các đối tượng (Objects) thực sự như con số `10`, chuỗi `"Hello"`, danh sách `[1, 2, 3]`.
- **Đặc trưng:** Dung lượng lớn, tồn tại độc lập với các hàm. Trong Python, **mọi thứ đều là Object** nên mọi giá trị đều nằm trên Heap.
- **Ví dụ:** Giá trị thực của số `10` nằm ở Heap.

### 11.3. Mối liên hệ

Hãy tưởng tượng Stack là **"Danh bạ điện thoại"** còn Heap là **"Ngôi nhà thực"**:

- Stack lưu tên và địa chỉ của ngôi nhà.
- Heap chứa nội dung bên trong ngôi nhà đó.

```python
a = [1, 2, 3] # Biến 'a' (Stack) trỏ đến List (Heap)
b = a         # Biến 'b' (Stack) trỏ chung vào cùng 1 List đó (Heap)
```

### 11.4. Garbage Collection (Bộ thu gom rác)

Python tự động dọn dẹp bộ nhớ cho bạn thông qua cơ chế đếm tham chiếu (**Reference Counting**):

1.  Mỗi Object trên Heap có một bộ đếm xem có bao nhiêu biến đang trỏ vào nó.
2.  Khi bạn chạy `del a`, bộ đếm giảm đi 1.
3.  Khi bộ đếm về **0** (không còn ai dùng đến), Python sẽ tự động xóa Object đó trên Heap để giải phóng bộ nhớ.

```

```
