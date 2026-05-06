# Chi tiết về Lập trình Hướng đối tượng (OOP) trong Python

Lập trình hướng đối tượng (OOP) là một mô hình lập trình dựa trên khái niệm về "đối tượng", có thể chứa dữ liệu dưới dạng các trường (thường được gọi là thuộc tính) và mã dưới dạng các thủ tục (thường được gọi là phương thức).

Dưới đây là chi tiết về 6 khái niệm cốt lõi của OOP trong Python:

## 1. Lớp (Class) và Đối tượng (Object)

- **Lớp (Class):** Là một bản thiết kế (blueprint) hoặc khuôn mẫu để tạo ra các đối tượng. Nó định nghĩa các thuộc tính (properties/attributes) và phương thức (methods) mà các đối tượng tạo ra từ lớp đó sẽ có.
- **Đối tượng (Object/Instance):** Là một thực thể cụ thể được tạo ra từ một lớp. Mỗi đối tượng có dữ liệu (trạng thái) riêng biệt độc lập với các đối tượng khác cùng lớp.

> **Lưu ý cho người dùng Java:** Python là ngôn ngữ _kiểu động (Dynamically typed)_. Bạn không cần phải khai báo các thuộc tính (fields) ở đầu class giống Java. Thuộc tính thường được định nghĩa và khởi tạo trực tiếp ngay bên trong hàm `__init__`. Thêm nữa, ở Python mọi thứ đều là object, kể cả bản thân "Class" cũng là một object.

```python
# Định nghĩa Lớp
class Car:
    # Phương thức khởi tạo (Constructor) - Được gọi tự động khi tạo đối tượng mới
    def __init__(self, brand, color):
        self.brand = brand  # Thuộc tính
        self.color = color  # Thuộc tính

    # Phương thức (Method)
    def start_engine(self):
        print(f"Xe {self.color} {self.brand} đang khởi động động cơ...")

# Tạo các Đối tượng (Objects) từ lớp Car
car1 = Car("Toyota", "Đỏ")
car2 = Car("Ford", "Đen")

# Truy cập thuộc tính và gọi phương thức
print(car1.brand)          # Output: Toyota
car1.start_engine()        # Output: Xe Đỏ Toyota đang khởi động động cơ...
car2.start_engine()        # Output: Xe Đen Ford đang khởi động động cơ...
```

## 2. Tính Đóng gói (Encapsulation) & Access Modifiers

Tính đóng gói giúp bảo vệ tính toàn vẹn của dữ liệu bằng cách hạn chế quyền truy cập trực tiếp vào các thành phần bên trong của đối tượng.

### 2.1. Ba cấp độ truy cập trong Python

Khác với Java dùng từ khóa (`public`, `private`,...), Python sử dụng **quy ước đặt tên** để xác định quyền truy cập:

| Cấp độ        | Cách đặt tên | Ý nghĩa                                                                                    |
| :------------ | :----------- | :----------------------------------------------------------------------------------------- |
| **Public**    | `name`       | Truy cập tự do từ mọi nơi.                                                                 |
| **Protected** | `_name`      | **Quy ước:** Chỉ nên dùng trong nội bộ lớp và các lớp con kế thừa.                         |
| **Private**   | `__name`     | **Kỹ thuật:** Python sẽ kích hoạt cơ chế _Name Mangling_ để hạn chế truy cập từ bên ngoài. |

> **Lưu ý cho người dùng Java:** Khác với Java dùng từ khóa để "khóa cửa" (compiler báo lỗi), Python dùng quy ước tên gọi và Name Mangling để tạo rào cản. Triết lý của Python là "Consenting Adults" - tin tưởng lập trình viên tự chịu trách nhiệm thay vì ngăn cấm tuyệt đối.

---

### 2.2. Cơ chế Name Mangling (Đổi tên biến) là gì?

Khi bạn đặt tên biến có 2 dấu gạch dưới ở đầu (ví dụ `__balance`) trong lớp `BankAccount`, Python sẽ tự động đổi tên biến này theo công thức:
`_ClassName__variableName`

**Ví dụ cụ thể:**

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance # Private attribute

account = BankAccount(1000)

# 1. Cố gắng truy cập trực tiếp sẽ bị lỗi:
# print(account.__balance)
# --> AttributeError: 'BankAccount' object has no attribute '__balance'

# 2. Nhưng thực tế, Python đã đổi tên nó thành:
print(account._BankAccount__balance)
# --> Output: 1000 (Truy cập thành công qua tên đã biến đổi)
```

**Tại sao lại cần Name Mangling?**

1.  **Tránh xung đột tên (Name Clashes):** Khi lớp con kế thừa từ lớp cha, nếu cả hai đều có thuộc tính `__update`, Name Mangling giúp chúng không bị ghi đè lẫn nhau (vì tên thật sẽ là `_Parent__update` và `_Child__update`).
2.  **Ngăn chặn truy cập vô ý:** Nó buộc lập trình viên phải "hiểu mình đang làm gì" nếu muốn truy cập vào dữ liệu private, vì họ phải dùng cái tên đã bị biến đổi phức tạp kia.

```python
# Ví dụ tổng hợp lại phần Đóng gói
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner          # Public
        self._currency = "VND"      # Protected (Quy ước)
        self.__balance = balance    # Private (Sẽ bị Name Mangling)

    def get_balance(self):
        return f"{self.__balance} {self._currency}"

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Nạp {amount} thành công.")

account = BankAccount("Lợi", 1000)
print(account.get_balance()) # Cách chính thống: 1000 VND
```

## 3. Tính Kế thừa (Inheritance)

Tính kế thừa cho phép một lớp mới (Lớp con - Child Class/Subclass) kế thừa các thuộc tính và phương thức của một lớp đã có (Lớp cha - Parent Class/Superclass). Giúp tái sử dụng code và thiết lập mối quan hệ phân cấp.

> **Lưu ý cho người dùng Java:**
>
> - Java dùng từ khóa `extends`, Python truyền tên lớp cha vào trong ngoặc đơn: `class Child(Parent):`.
> - Khác biệt lớn nhất: Java chỉ hỗ trợ Đơn kế thừa (một lớp con chỉ có 1 lớp cha). **Python hỗ trợ Đa kế thừa (Multiple Inheritance)**, một lớp con có thể kế thừa từ nhiều lớp cha cùng lúc: `class Child(Father, Mother):`.

```python
# Lớp Cha
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} đang ăn.")

    def sleep(self):
        print(f"{self.name} đang ngủ.")

# Lớp Con kế thừa từ Lớp Cha (Animal)
class Dog(Animal):
    def __init__(self, name, breed):
        # Dùng super() để gọi hàm __init__ của lớp cha
        super().__init__(name)
        self.breed = breed  # Thuộc tính riêng của lớp con

    def bark(self):
        print(f"{self.name} sủa: Gâu gâu!")

# Sử dụng
my_dog = Dog("Milu", "Corgi")

# Kế thừa phương thức từ lớp cha
my_dog.eat()    # Output: Milu đang ăn.
my_dog.sleep()  # Output: Milu đang ngủ.

# Dùng phương thức riêng của lớp con
my_dog.bark()   # Output: Milu sủa: Gâu gâu!
```

### 3.1. Method Overriding – Ghi đè Phương thức (Chi tiết)

Khi lớp con kế thừa từ lớp cha, đôi khi hành vi của phương thức trong lớp cha không còn phù hợp với lớp con nữa. **Method Overriding** cho phép lớp con **định nghĩa lại** phương thức đó với cùng tên.

> **Quy tắc để ghi đè:** Chỉ cần định nghĩa lại hàm trong lớp con với **đúng tên** và **đúng signature**. Python sẽ tự biết ưu tiên dùng phiên bản của lớp con.

**Có 3 chiến lược ghi đè:**

#### Chiến lược 1: Viết mới hoàn toàn (Replace)
Bỏ qua hoàn toàn logic của cha, viết logic mới từ đầu.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_info(self):
        return f"NV: {self.name} - Lương: {self.salary}"

class Developer(Employee):
    def __init__(self, name, salary, language):
        super().__init__(name, salary)  # Gọi cha để xử lý name, salary
        self.language = language

    # Ghi đè hoàn toàn - không dùng gì của cha nữa
    def get_info(self):
        return f"NV: {self.name} - Lương: {self.salary} - Ngôn ngữ: {self.language}"

dev = Developer("An", 1000, "Python")
print(dev.get_info())  # Output: NV: An - Lương: 1000 - Ngôn ngữ: Python
```

#### Chiến lược 2: Mở rộng (Extend) – Tận dụng lại lớp cha bằng `super()`
Đây là cách viết **thông minh và chuyên nghiệp hơn**. Thay vì viết lại toàn bộ, ta dùng `super()` để lấy kết quả của cha rồi cộng thêm vào.

```python
class Developer(Employee):
    def __init__(self, name, salary, language):
        super().__init__(name, salary)
        self.language = language

    # Tận dụng kết quả của cha rồi mở rộng thêm
    def get_info(self):
        parent_info = super().get_info()        # Lấy chuỗi "NV: An - Lương: 1000"
        return f"{parent_info} - Ngôn ngữ: {self.language}"  # Ghép thêm vào

dev = Developer("An", 1000, "Python")
print(dev.get_info())  # Output: NV: An - Lương: 1000 - Ngôn ngữ: Python
```

> **💡 Khi nào dùng `super()` trong Override?**
> - Khi logic của cha vẫn còn giá trị và bạn chỉ muốn **bổ sung thêm**, hãy dùng `super()`.
> - Khi logic của cha **hoàn toàn không phù hợp**, hãy viết mới hoàn toàn (Chiến lược 1).
> - Trong `__init__`, **hầu như luôn luôn** phải gọi `super().__init__(...)` để đảm bảo các thuộc tính từ cha được khởi tạo đúng.

#### Chiến lược 3: Kết hợp với vòng lặp đa hình (Polymorphism in action)
Đây là ứng dụng thực tế nhất: nhiều lớp con có cùng tên hàm nhưng hành vi khác nhau, và ta có thể gọi chúng theo cách thống nhất.

```python
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_info(self):
        parent_info = super().get_info()
        return f"{parent_info} - Quản lý: {self.team_size} người"

# Danh sách nhân viên các loại khác nhau
employees = [
    Employee("Bình", 800),
    Developer("An", 1000, "Python"),
    Manager("Chi", 2000, 5),
]

# Gọi chung một lệnh, mỗi đối tượng tự biết phản hồi theo cách của mình
for emp in employees:
    print(emp.get_info())

# Output:
# NV: Bình - Lương: 800
# NV: An - Lương: 1000 - Ngôn ngữ: Python
# NV: Chi - Lương: 2000 - Quản lý: 5 người
```

---

## 4. Tính Đa hình (Polymorphism)

Đa hình là "một giao diện, nhiều cách thực hiện". Nó cho phép các đối tượng thuộc các lớp khác nhau có thể phản hồi lại cùng một lời gọi phương thức theo cách riêng của chúng.

Có 2 cách thể hiện chính ở Python:

1.  **Method Overriding (Ghi đè phương thức):** Lớp con định nghĩa lại một phương thức đã có ở lớp cha.
2.  **Duck Typing:** "Nếu nó đi giống vịt và kêu giống vịt, thì nó là vịt". Python không quan tâm đối tượng thuộc class nào, chỉ quan tâm nó có phương thức cần gọi hay không.

> **Lưu ý cho người dùng Java:**
>
> - Java có tính chặt chẽ cao, đối tượng muốn có tính đa hình phải cùng kế thừa từ một `Interface` hoặc `Class` cha. Python với `Duck Typing` linh hoạt hơn nhiều: chỉ cần các đối tượng có **tên hàm giống nhau** là gọi chung được, không cần phải có quan hệ họ hàng gì cả.
> - Python **không có Method Overloading** (tạo nhiều hàm trùng tên nhưng khác tham số) như Java. Hàm nào định nghĩa sau cùng sẽ ghi đè đè lên hàm trước đó.

**Ví dụ chi tiết về Duck Typing (Khác biệt lớn với Java):**

```python
class CreditCard:
    def pay(self, amount):
        print(f"Thanh toán {amount} qua Thẻ tín dụng.")

class CryptoWallet:
    def pay(self, amount):
        print(f"Thanh toán {amount} bằng Bitcoin.")

# Hàm này không quan tâm đối tượng truyền vào là gì, miễn là nó có hàm .pay()
def process_payment(payment_obj, amount):
    payment_obj.pay(amount)

# Hai lớp CreditCard và CryptoWallet không hề kế thừa chung một lớp nào cả
visa = CreditCard()
btc = CryptoWallet()

process_payment(visa, 100) # Output: Thanh toán 100 qua Thẻ tín dụng.
process_payment(btc, 200)  # Output: Thanh toán 200 bằng Bitcoin.
```

_Giải thích:_ Trong Java, bạn sẽ phải tạo `interface Payment` rồi cho cả 2 lớp trên `implements Payment`. Trong Python, chỉ cần chúng "biết kêu cạp cạp" (có hàm `pay`) là chúng "là vịt" (dùng chung được).

```python
# Ví dụ Method Overriding và Đa hình
class Bird:
    def speak(self):
        return "Chim kêu ríu rít"

class Duck(Bird):
    # Ghi đè phương thức speak của lớp cha
    def speak(self):
        return "Vịt kêu: Cạp cạp"

class Parrot(Bird):
    # Ghi đè phương thức speak của lớp cha
    def speak(self):
        return "Vẹt nói: Xin chào"

# Một hàm chung có thể nhận bất kỳ đối tượng nào
def make_animal_speak(animal):
    # Cùng gọi hàm speak(), nhưng mỗi con vật sẽ phản hồi khác nhau
    print(animal.speak())

bird = Bird()
duck = Duck()
parrot = Parrot()

make_animal_speak(bird)   # Output: Chim kêu ríu rít
make_animal_speak(duck)   # Output: Vịt kêu: Cạp cạp
make_animal_speak(parrot) # Output: Vẹt nói: Xin chào
```

## 5. Tính Trừu tượng (Abstraction)

Tính trừu tượng giúp ẩn đi các chi tiết thực thi phức tạp và chỉ hiển thị ra các tính năng thiết yếu của đối tượng. Trong Python, ta sử dụng module `abc` (Abstract Base Classes) để tạo các Lớp trừu tượng.

- **Lớp trừu tượng:** Không thể tạo đối tượng (instance) trực tiếp từ nó. Nó thường đóng vai trò như một "hợp đồng" (contract) bắt buộc các lớp con phải tuân thủ.
- **Phương thức trừu tượng:** Là phương thức được khai báo nhưng không có nội dung thực thi ở lớp cha. Lớp con **bắt buộc** phải ghi đè (override) nó.

> **Lưu ý cho người dùng Java:** Python **không có** từ khóa `interface` hay `abstract` tích hợp sẵn trong cú pháp lõi. Để làm việc với tính Trừu tượng, bạn bắt buộc phải import module `abc` (Abstract Base Classes) từ thư viện chuẩn. Nó giống như một thư viện gắn thêm thay vì là tính năng bản địa ăn sâu vào ngôn ngữ như Java.

```python
from abc import ABC, abstractmethod

# Kế thừa từ ABC để tạo Lớp trừu tượng
class Shape(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def calculate_area(self):
        pass # Phương thức rỗng, bắt buộc lớp con phải triển khai

    # Lớp trừu tượng vẫn có thể có phương thức bình thường
    def describe(self):
        print(f"Tôi là một hình màu {self.color}")

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height

    # BẮT BUỘC phải triển khai phương thức tính diện tích
    def calculate_area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    # BẮT BUỘC phải triển khai phương thức tính diện tích
    def calculate_area(self):
        return 3.14 * (self.radius ** 2)

# shape = Shape("Đỏ") # LỖI: Không thể khởi tạo đối tượng từ Abstract Class

rect = Rectangle("Xanh", 5, 10)
circle = Circle("Vàng", 3)

rect.describe()                         # Output: Tôi là một hình màu Xanh
print(f"Diện tích: {rect.calculate_area()}") # Output: Diện tích: 50

print(f"Diện tích hình tròn: {circle.calculate_area()}") # Output: Diện tích hình tròn: 28.26
```

## 6. Magic Methods (Dunder Methods)

Đây là các phương thức đặc biệt trong Python được bao quanh bởi hai dấu gạch dưới (Double UNDERscore = Dunder). Chúng cho phép định nghĩa các hành vi "ma thuật" (như phép toán `+`, `-`, cách in đối tượng,...).

> **Lưu ý cho người dùng Java:**
>
> - Hàm `__str__` trong Python chính xác là tương đương với việc bạn `override` hàm `toString()` trong Java.
> - Tuy nhiên Python tiến xa hơn Java ở chỗ nó hỗ trợ **Operator Overloading (Ghi đè toán tử)**. Java không cho phép bạn định nghĩa phép cộng `+` hay trừ `-` cho 2 object tự tạo (trừ String). Còn ở Python, bạn chỉ việc định nghĩa lại các hàm có sẵn như `__add__` (cho dấu `+`), `__sub__` (cho dấu `-`), `__eq__` (cho dấu `==`)... thì Python sẽ tự hiểu cách thao tác với object của bạn.

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    # __str__: Định nghĩa chuỗi hiển thị khi dùng print() (Dành cho người dùng)
    def __str__(self):
        return f"Cuốn sách '{self.title}' có {self.pages} trang."

    # __len__: Định nghĩa hành vi khi dùng hàm len()
    def __len__(self):
        return self.pages

    # __add__: Định nghĩa hành vi khi dùng toán tử '+' cho 2 đối tượng
    def __add__(self, other):
        return self.pages + other.pages

book1 = Book("Harry Potter", 400)
book2 = Book("Đắc Nhân Tâm", 300)

print(book1)             # Output: Cuốn sách 'Harry Potter' có 400 trang. (Nhờ hàm __str__)
print(len(book1))        # Output: 400 (Nhờ hàm __len__)
print(book1 + book2)     # Output: 700 (Nhờ hàm __add__)
```

## 7. Các đặc trưng nâng cao & "Pythonic" trong OOP

Để code OOP của bạn thực sự mang phong cách Python (Pythonic) và không bị "lai tạp" tư duy từ ngôn ngữ khác, bạn cần nắm thêm 3 khái niệm cực kỳ quan trọng sau:

### 7.1. Decorator `@property` (Thay thế Getter/Setter)

Ở phần Đóng gói, người dùng Java thường có thói quen tạo hàm `get_balance()` để lấy giá trị biến private. 
Nhưng ở Python, dùng hàm `get_...()` bị coi là code "thiếu tự nhiên". Giải pháp là dùng `@property`.

`@property` biến một **hàm** (phương thức) thành một **thuộc tính ảo**. Nghĩa là bạn viết logic tính toán/lấy dữ liệu bên trong hàm, nhưng khi người dùng gọi, họ không cần thêm cặp ngoặc tròn `()`.

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    # Cách kiểu Java (Không nên dùng):
    def get_fahrenheit(self):
        return (self._celsius * 9/5) + 32

    # Cách chuẩn Python (Dùng @property):
    @property 
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32

temp = Temperature(25)

# Nếu dùng cách Java, bạn phải gọi: temp.get_fahrenheit()
# Nhờ @property, bạn có thể gọi nó như một biến bình thường:
print(temp.fahrenheit) # Output: 77.0 (Lưu ý: Không có ngoặc () ở cuối)
```

### 7.2. Class Variable vs Instance Variable

- **Instance Variable (Thuộc tính đối tượng):** Khai báo trong `__init__` với `self`. Mỗi đối tượng có một bản sao lưu trữ riêng.
- **Class Variable (Thuộc tính lớp):** Khai báo ngay dưới tên class, nằm ngoài mọi hàm. Dùng chung cho TẤT CẢ các đối tượng. (Khá giống `static variable` trong Java).

```python
class Dog:
    species = "Canis familiaris" # Class Variable (Dùng chung cho mọi con chó)

    def __init__(self, name):
        self.name = name         # Instance Variable (Tên riêng của từng con)

dog1 = Dog("Milu")
dog2 = Dog("Corgi")
print(dog1.species) # Output: Canis familiaris
print(Dog.species)  # Nên gọi trực tiếp từ tên Lớp thay vì đối tượng
```

### 7.3. Các loại Phương thức (Method Types)

Trong Java, phương thức chỉ chia làm 2 loại (thường và `static`). Python chia làm 3 loại rõ rệt. Dưới đây là giải thích và ví dụ cụ thể cho 2 loại đặc biệt:

1.  **Instance Method (Hàm của đối tượng):** Nhận tham số đầu tiên là `self` (trỏ đến đối tượng). Được dùng nhiều nhất.
2.  **Class Method (`@classmethod`):** Nhận tham số đầu tiên là `cls` (trỏ đến chính cái Lớp đó). 
    *   **Tác dụng:** Dùng để thay đổi biến tập thể (Class Variable) hoặc để làm "Factory Method" (hàm tự tạo ra một đối tượng theo một cách đặc biệt, ví dụ khởi tạo từ một chuỗi ngày tháng thay vì truyền từng tham số).
3.  **Static Method (`@staticmethod`):** Không nhận `self` hay `cls`. 
    *   **Tác dụng:** Chẳng khác gì một hàm tiện ích bình thường bạn viết ngoài file. Nhưng vì logic của nó liên quan chặt chẽ đến Class này (ví dụ hàm kiểm tra định dạng ngày tháng hợp lệ trước khi tạo user) nên ta "nhét" nó vào class cho gọn gàng và dễ quản lý.

**Ví dụ minh họa `@classmethod` và `@staticmethod`:**

```python
class Employee:
    # Class variable
    raise_amount = 1.05 

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary # Instance variable

    # 1. INSTANCE METHOD (Dùng self)
    def apply_raise(self):
        self.salary = int(self.salary * self.raise_amount)

    # 2. CLASS METHOD (Dùng cls)
    @classmethod
    def set_raise_amount(cls, amount):
        # cls ở đây chính là Lớp Employee. 
        # Hàm này đổi mức tăng lương cho TOÀN BỘ nhân viên
        cls.raise_amount = amount

    # 3. STATIC METHOD (Không dùng self hay cls)
    @staticmethod
    def is_workday(day):
        # Hàm này chỉ làm 1 việc duy nhất là check ngày hợp lệ hay không.
        # Nó không cần dùng bất kỳ biến self.salary hay cls.raise_amount nào cả.
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

# --- CÁCH SỬ DỤNG ---

# Đổi mức tăng lương chung cho toàn bộ nhân viên (Dùng Class Method)
Employee.set_raise_amount(1.10) 

# Kiểm tra ngày (Dùng Static Method)
import datetime
my_date = datetime.date(2023, 10, 15)
print(Employee.is_workday(my_date)) # Output: False (Ngày Chủ nhật)
```

> **Lưu ý cuối cùng:** Ở Python, `self` và `cls` không phải là từ khóa bắt buộc của hệ thống (như `this` trong Java), chúng chỉ là **quy ước đặt tên** cộng đồng. Bạn có thể dùng tên khác (ví dụ `def apply_raise(toi):`), nhưng điều đó là cấm kỵ vì sẽ khiến cộng đồng Python khó đọc code của bạn.
