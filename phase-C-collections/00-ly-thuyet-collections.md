# TỔNG HỢP KIẾN THỨC CẤU TRÚC DỮ LIỆU (PHASE C)

Tài liệu này tổng hợp toàn bộ các kiến thức cốt lõi liên quan đến cách tổ chức, lưu trữ Cấu trúc dữ liệu, Phân tách Module và Xử lý Đọc/Ghi File trong Python.

---

## 1. Data Structures (Thao tác List & Comprehension)

### List Operations (Các lệnh thao tác mảng)
List là mảng động thay đổi được độ dài và chứa được nhiều kiểu dữ liệu cùng lúc.
- Thêm phần tử: `list.append(item)` (vào cuối), `list.insert(index, item)` (chèn vào giữa).
- Xóa phần tử: `list.remove(value)` (xóa theo giá trị), `list.pop()` (lấy và xóa phần tử cuối cùng).
- Sắp xếp: `list.sort()` (xếp tại chỗ).

### Slicing (Cắt mảng)
Áp dụng tương tự như chuỗi String với công thức `[start:stop:step]`. Rất hữu ích khi cần lấy top đầu hoặc top cuối mảng.
- `list[:5]` (Lấy 5 phần tử đầu tiên).
- `list[-3:]` (Lấy 3 phần tử cuối cùng).

### List Comprehension (Đặc sản cốt lõi của Python)
Cú pháp cực nhanh để tạo ra một List mới thay vì dùng vòng lặp `for` và `.append()` nhiều dòng.
- **Công thức:** `[ <Hành động>  for <Phần tử> in <Tập hợp>  if <Điều kiện> ]`
- **Ví dụ lọc số chẵn:**
  ```python
  numbers = [1, 2, 3, 4, 5]
  squares = [x * x for x in numbers if x % 2 == 0] # Trả về [4, 16]
  ```

---

## 2. Dict, Set, Tuple (Lý thuyết và Ứng dụng)

### 2.1. Tuple (Mảng tĩnh)
- **Đặc điểm:** Có thứ tự, **không thể thay đổi** (immutable). Dùng để bảo vệ cố định dữ liệu.
  > _(Liên tưởng: Một Array "chỉ đọc" hoặc dùng để lưu các hằng số toạ độ)_

```python
coordinates = (10, 20)
# coordinates[0] = 15  # LỖI: Tuple không cho phép gán lại phần tử
print(coordinates[0])    # Trả về 10
```

### 2.2. Dictionary (Dict)
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

#### Kỹ thuật đếm tần suất bằng Dict
Dictionary xuất sắc nhất trong việc rà soát và đếm tần suất (Ví dụ: đếm Word Count).
```python
word_counts = {}
for word in words:
    word_counts[word] = word_counts.get(word, 0) + 1
```

### 2.3. Set (Tập hợp)
- **Đặc điểm:** Không có thứ tự, **không có phần tử trùng lặp**, xử lý biểu thức logic tập hợp rất nhanh. Khai báo Set bằng cặp ngoặc nhọn `{}` giống Dict nhưng không có cấu trúc theo cặp Key:Value.
  > _(Liên tưởng: Giống `HashSet` trong Java)._

```python
unique_ids = {1, 2, 2, 3, 4, 4, 5} # Khi khai báo không có dạng key:value thì đây là Set
print(unique_ids) # Kết quả tự xoá trùng: {1, 2, 3, 4, 5}

unique_ids.add(6)
unique_ids.discard(1) # Bỏ số 1 đi (khác với remove là nếu không có thì ko báo lỗi)

# Toán tử tập hợp toán học
set_A = {1, 2, 3}
set_B = {3, 4, 5}
print(set_A.union(set_B))        # Hợp A và B
print(set_A.intersection(set_B)) # Giao A và B (Những phần tử chung)
```

### 2.4. Tổng kết: So sánh và Lựa chọn cấu trúc an toàn

Bảng dưới đây tóm tắt sự khác biệt cốt lõi để bạn biết chính xác khi nào nên móc loại nào ra dùng:

| Cấu trúc | Cú pháp | Thay đổi (Mutable)? | Có thứ tự? | Trùng lặp? | Khi nào dùng? |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **List** | `[1, 2, "A"]` | ✅ Có | ✅ Có | ✅ Có | **Mảng đa năng.** Dùng khi cần một danh sách chung chung (D/s học sinh, Lịch sử thao tác). |
| **Tuple** | `(1, 2, "A")` | ❌ Không (Immutable) | ✅ Có | ✅ Có | **Mảng chỉ đọc.** Dùng khi dữ liệu cố định (Tọa độ, cấu hình) hoặc gom biến trả về (`return a, b`). |
| **Set** | `{1, 2, "A"}` | ✅ Có | ❌ Không | ❌ Không | **Bộ lọc duy nhất.** Dùng để lọc trùng lặp từ List, hoặc làm phép toán tập hợp (tìm điểm chung). |
| **Dict** | `{"id": 1}` | ✅ Có | ✅ Có* | ❌ Không (Key) | **Cuốn từ điển.** Lưu theo cặp `Key: Value`. Dùng giống JSON hoặc để đếm tần suất xuất hiện. |

*(Ghi chú: Dict bắt đầu giữ nguyên được thứ tự thêm vào từ phiên bản Python 3.7+)*

---

## 3. Kỹ thuật Giải nén (Unpacking & Destructuring)

Bản chất của dấu `*` (với List/Tuple) và `**` (với Dict) là công cụ giải nén ở cấp độ ngôn ngữ. Nó không bị giới hạn trong khai báo hàm hay `print()` mà có thể dùng ở khắp nơi để xử lý cấu trúc dữ liệu cực nhanh:

### Truyền tham số mảng vào hàm
Khi hàm yêu cầu tham số rời rạc nhưng dữ liệu đang nằm trong List:
```python
def tinh_the_tich(dai, rong, cao): 
    return dai * rong * cao

kich_thuoc = [5, 4, 3] 
# Dùng * để rã mảng thành 3 tham số rời truyền vào hàm:
ket_qua = tinh_the_tich(*kich_thuoc) # Tương đương tinh_the_tich(5, 4, 3)
```

### Gộp (Merge) nhiều cấu trúc dữ liệu
```python
list_A = [1, 2]
list_B = [3, 4]
list_tong = [0, *list_A, *list_B, 5] # Rã ra nhét chung: [0, 1, 2, 3, 4, 5]

dict_A = {"a": 1}
dict_B = {"b": 2}
dict_tong = {**dict_A, **dict_B} # Rã 2 dict nhỏ gộp thành 1 dict lớn
```

### Tách biến thông minh (Destructuring Assignment)
Rất hữu ích khi cần lấy phần tử đầu/cuối của một mảng dài và gom phần còn lại.
```python
diem_thi = [10, 5, 6, 7, 8, 9]

# Biến có dấu * sẽ "hút" tất cả các giá trị dư ra thành 1 list mới
diem_cao_nhat, *phan_giua, diem_thap_nhat = diem_thi
# diem_cao_nhat = 10 
# phan_giua = [5, 6, 7, 8]
# diem_thap_nhat = 9
```

---

## 4. Modules (Tổ chức và Phân rã mã nguồn)

Khi file `main.py` quá dài, việc tách logic là bắt buộc.
- **Tách file:** Di chuyển hàm tính toán rườm rà ra một file `utils.py`.
- **Cú pháp Import:** 
  - Gọi toàn bộ thư viện: `import utils` (Lúc dùng phải gọi `utils.calculate()`).
  - Gọi đích danh để code gọn hơn: `from utils import calculate`.
- **Hàm phân tích `dir()`:** Lệnh `dir(math)` hoặc `dir(tên_module)` giúp liệt kê toàn bộ các biến/hàm đang tồn tại ngầm bên trong một module để xem thư viện đó có gì dùng được không.

---

## 5. File I/O Cơ bản (Đọc & Ghi file)

Bắt buộc phải áp dụng **Context Manager (`with open`)** để file luôn tự động đóng lại (giải phóng Memory) kể cả khi chương trình bị crash giữa chừng.

### Xử lý với văn bản Text (Log, Txt)
- Chế độ mở: `"r"` (Đọc), `"w"` (Ghi đè mới hoàn toàn), `"a"` (Ghi tiếp nối vào cuối đuôi).
- **Đọc file khôn ngoan:** Không dùng `file.read()` nếu file nặng 10GB vì sẽ tràn RAM. Tối ưu nhất là dùng vòng lặp cho từng dòng:
  ```python
  with open("app.log", "r") as f:
      for line in f:
          print(line.strip()) # Xử lý lần lượt từng dòng
  ```

---

## 6. CSV Cơ bản

Dữ liệu thực tế thường chạy qua file đuôi CSV. Python có sẵn module `csv`.
- Dùng `csv.reader(f)` để bóc tách từng dòng file CSV và chuyển nó về thành danh sách (List).
- Tính năng mạnh hơn: Dùng `csv.DictReader(f)` để nó ngầm biến dòng tiêu đề (header) của cột biến tự động thành Key trong Dict, lấy đúng giá trị theo cột rất khỏe.

---

## 7. Bài tập thực hành & Dự án (Mini Projects)

### Mini Projects Tích hợp (Mức Trung Bình)
1. **Contact Book CLI:** CRUD lưu trữ thông tin (thêm, sửa, xóa, tìm) vào một List các Dict và lưu dữ liệu thực ra file dạng TXT hoặc CSV.
2. **Log Analyzer:** Đọc trích xuất một file `.log` máy chủ, filter dòng theo mức độ ERROR, đếm tần suất lỗi bằng Dict, in ra báo cáo tổng kết cuối cùng.
3. **Quiz Engine:** Đọc câu đố bằng tập hợp `List[Dict]`. Mix xáo trộn thứ tự tự nhiên (random), bắt user nhập đáp án và tổng kết điểm.

### Bạn sẽ ĐẠT Năng lực Giai đoạn C nếu:
- [ ] Phân biệt và ứng dụng quyết đoán được khi gặp đề bài thì nên móc List, Dict, Set hay Tuple ra xài.
- [ ] Đọc được một cục dữ liệu file văn bản chết, mổ xẻ lọc chữ và biến nó thành một File kết quả báo cáo mới.
- [ ] Có Project chia tách ngầm thành 2 file `main.py` và `utils.py` chạy trơn tru mà không lỗi `ModuleNotFoundError`.
- [ ] Xong được dự án nhỏ: Lọc Unique Emails bằng Set và đếm ký tự Top 10 phổ biến nhất bằng Dict.
