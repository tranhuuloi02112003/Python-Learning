# Hàm print() Trong Python

Hàm `print()` trông có vẻ đơn giản nhưng thực ra nó được trang bị rất nhiều "vũ khí ngầm" cực kỳ hữu ích. Cấu trúc khai báo đầy đủ (Signature) của hàm `print()` trong Python là:

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

Chúng ta sẽ đi mổ xẻ từng tham số một và so sánh nó với F-string.

---

## 1. `*objects` (Cơ chế gom nhóm thành Tuple)

Dấu `*` (Packing operator) mang ý nghĩa gom tất cả các tham số bạn truyền vào thành một cấu trúc **Tuple**. Nói cách khác, `*objects` trong `print` hoạt động chính xác như cơ chế `*args` ở các hàm thông thường.
Nhờ việc gom thành Tuple, `print` có thể nhận **số lượng tham số vô hạn**. Dưới "nắp capo", vòng lặp của `print` sẽ duyệt qua Tuple này, ép kiểu từng phần tử thành chuỗi (String) và in chúng ra.

```python
name = "Lợi"
age = 22
# Khi bạn truyền vào 5 tham số rải rác:
print("Tên tôi là", name, "và tôi", age, "tuổi")

# Thực chất Python đã gom chúng lại thành 1 Tuple:
# objects = ('Tên tôi là', 'Lợi', 'và tôi', 22, 'tuổi')
```

**Kỹ thuật Unpacking (Giải nén):**
Vì `print` hiểu dấu `*`, nên nếu bạn đã có sẵn một List/Tuple và muốn in rải rác các phần tử (thay vì in nguyên cái ngoặc vuông), bạn có thể dùng dấu `*` gọi là Unpacking:

```python
mang_du_lieu = [1, 2, 3, 4]

# Không có sao (*): In ra một đối tượng List duy nhất
print(mang_du_lieu)  # Kết quả: [1, 2, 3, 4]

# Có sao (*): Rã List thành 4 tham số rời rạc (tương đương print(1, 2, 3, 4))
print(*mang_du_lieu) # Kết quả: 1 2 3 4
```

## 2. `sep` (Separator - Ký tự phân cách)

Khi bạn in nhiều tham số, mặc định Python sẽ tự động chèn **một dấu cách (khoảng trắng)** vào giữa các tham số đó. Tham số `sep` giúp bạn đổi dấu cách này thành bất cứ thứ gì bạn muốn.

```python
# Mặc định: sep=' '
print("A", "B", "C")          # Kết quả: A B C

# Đổi sep thành dấu gạch nối
print("A", "B", "C", sep="-") # Kết quả: A-B-C

# Đổi sep thành xuống dòng
print("A", "B", "C", sep="\n")
# Kết quả:
# A
# B
# C
```

## 3. `end` (Ký tự kết thúc)

Mặc định, sau khi in xong mọi thứ, Python sẽ tự động chèn một ký tự **xuống dòng** `\n` vào cuối. Bạn có thể can thiệp vào tham số `end` để nối chuỗi trên cùng một dòng.

```python
# Mặc định (end='\n')
print("Hello")
print("World")
# Chạy ra 2 dòng

# Thay đổi end để nối chúng lại trên cùng 1 dòng
print("Hello", end=" ---> ")
print("World")
# Kết quả: Hello ---> World
```

_(Mẹo: Kỹ thuật `end=""` thường xuyên được dùng trong vòng lặp `for` để in thanh tiến trình tiến lên từ từ)._

## 4. `file` (In thẳng vào file thay vì ra màn hình)

Mặc định `print` đẩy chữ ra màn hình Terminal (`sys.stdout`). Bạn có thể "bẻ lái" luồng dữ liệu này để ghi thẳng vào một file Text. Dùng cách này tiện hơn `f.write()` vì nó tự động nối khoảng trắng, ép kiểu và xuống dòng.

```python
# Mở một file tên là log.txt ở chế độ 'w' (write)
with open("log.txt", "w") as f:
    print("Dòng chữ này sẽ không hiện ra màn hình!", file=f)
    print("Nó đã chui thẳng vào file log.txt", file=f)
```

## 5. `flush` (Ép đẩy dữ liệu ngay lập tức)

Máy tính thường có cơ chế **Buffer (Bộ đệm)**, nó gom đủ một lượng chữ hoặc chờ dấu `\n` rồi mới in ra một thể để tiết kiệm tài nguyên.
`flush=True` là lệnh **ÉP** máy tính bỏ qua bộ đệm, in ngay lập tức. Cực kỳ hữu ích khi làm hiệu ứng Loading.

```python
import time

for i in range(5):
    print(".", end="", flush=True)
    time.sleep(1)
# Dấu chấm sẽ hiện ra từ từ từng giây.
```

---

## 6. So sánh: Dùng print() dấu phẩy hay F-string?

Trông có vẻ ra kết quả giống nhau khi in lên màn hình, nhưng bản chất hoàn toàn khác biệt:

1. **Về Bản chất (Quan trọng nhất):**
   - `print(a, b, c)`: Chỉ thực hiện hành động **đẩy chữ ra màn hình**. Nó KHÔNG tạo ra một chuỗi (String object) hoàn chỉnh trong bộ nhớ để bạn lưu lại hay tái sử dụng.
   - `f"..."` (F-string): Là công cụ **lắp ráp chuỗi**. Nó tạo ra một đối tượng Chuỗi duy nhất. Bạn có thể in nó ra, lưu vào biến, hoặc `return` trả về từ một hàm.

   ```python
   # ĐÚNG: Trả về một chuỗi hoàn chỉnh
   def tao_loi_chao(name, age):
       return f"Xin chào {name}, bạn {age} tuổi"

   # SAI: Trả về một Tuple rời rạc, không phải là một câu hoàn chỉnh
   def tao_loi_chao(name, age):
       return "Xin chào", name, "bạn", age, "tuổi"
   ```

2. **Kiểm soát khoảng trắng:**
   `print` tự chèn khoảng trắng, đôi khi gây thừa thãi trước các dấu câu (ví dụ: `Xin chào Lợi !`). F-string cho phép ghép sát hoàn hảo (`Xin chào Lợi!`).

3. **Sức mạnh định dạng (Formatting):**
   F-string cho phép định dạng trực tiếp bên trong ngoặc nhọn `{}` cực kỳ linh hoạt mà `print` rời rạc không làm được.

   ```python
   gia_tien = 1500000
   print(f"Tổng tiền: {gia_tien:,} VNĐ") # Tổng tiền: 1,500,000 VNĐ

   pi = 3.14159265
   print(f"Số Pi là: {pi:.2f}") # Số Pi là: 3.14
   ```

**Tóm tắt:** Nếu chỉ in ra console cho vui/để debug ➡️ Dùng `print(a, b, c)`. Nếu cần lưu trữ lại thành biến để làm việc khác, return hoặc định dạng số liệu ➡️ Bắt buộc dùng **F-string**.
