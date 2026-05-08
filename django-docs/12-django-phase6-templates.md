# Phase 6: Công xưởng Giao diện (Template Engine)

Đây là mảnh ghép cuối cùng trong mô hình MVT. Template Engine của Django là nơi biến những dữ liệu khô khan từ Database thành những trang web lung linh mà người dùng nhìn thấy.

---

## 1. Context: Chiếc cầu nối từ View sang HTML

Hãy nhớ lại hàm View:
```python
return render(request, 'list.html', {'tasks': tasks, 'name': 'Lợi'})
```
Cái từ điển `{'tasks': tasks, 'name': 'Lợi'}` được gọi là **Context**. 
*   Django sẽ cầm cái "túi" Context này đi vào file HTML. 
*   Cứ chỗ nào bạn viết `{{ name }}`, Django sẽ thò tay vào túi, lấy chữ "Lợi" và dán đè lên chỗ đó.

---

## 2. Ngôn ngữ Template của Django (DTL)

DTL không phải là Python, nó là một ngôn ngữ riêng cực kỳ đơn giản với 3 cú pháp chính:

### A. Variables (Biến): `{{ ... }}`
Dùng để in giá trị ra màn hình.
*   `{{ task.title }}`: In tiêu đề task.
*   `{{ request.user.username }}`: In tên người đang đăng nhập.

### B. Tags (Thẻ điều hướng): `{% ... %}`
Dùng để xử lý logic (vòng lặp, điều kiện).
*   `{% for task in tasks %}` ... `{% endfor %}`: Lặp qua danh sách.
*   `{% if task.completed %}` ... `{% else %}` ... `{% endif %}`: Kiểm tra điều kiện.
*   `{% url 'home' %}`: Sinh ra đường link dựa trên tên đã đặt ở `urls.py`.

### C. Filters (Bộ lọc): `{{ var|filter }}`
Dùng để "trang điểm" cho dữ liệu trước khi hiện ra.
*   `{{ task.created_at|date:"d/m/Y" }}`: Biến ngày giờ loằng ngoằng thành định dạng "04/05/2026".
*   `{{ task.title|lower }}`: Chuyển hết thành chữ thường.
*   `{{ task.title|truncatechars:10 }}`: Nếu tên quá dài, nó tự cắt và thêm dấu `...` ở sau.

---

## 3. Kế thừa Template (Sức mạnh thực sự)

Trong một trang web thực tế, các trang thường có chung Header (Thanh menu) và Footer (Thông tin cuối trang). 
👉 **Vấn đề:** Nếu bạn có 100 trang, chẳng lẽ bạn phải copy code Header/Footer vào 100 file? Nếu cần đổi màu Header, bạn phải sửa 100 file?

**Giải pháp của Django: `extends` và `block`**

### Bước 1: Tạo file gốc `base.html` (Khung xương)
Bạn định nghĩa những thứ chung nhất ở đây, và để lại những "khoảng trống" (block) cho các trang con điền vào.

```html
<!-- base.html -->
<html>
<head><title>My App</title></head>
<body>
    <nav>Đây là Thanh Menu Chung</nav>

    <div class="content">
        {% block content %}
        <!-- Trang con sẽ ném nội dung vào đây -->
        {% endblock %}
    </div>

    <footer>Đây là Footer Chung</footer>
</body>
</html>
```

### Bước 2: Các trang con "Kế thừa" từ trang gốc
Trang con không cần viết lại thẻ `<html>`, `<body>` hay `nav` nữa. Nó chỉ cần tập trung vào nội dung riêng của nó.

```html
<!-- list.html -->
{% extends 'base.html' %} <!-- Nói với Django: Hãy lấy khung của base.html -->

{% block content %}
    <h1>Danh sách công việc của tôi</h1>
    <!-- Code của trang List nằm ở đây -->
{% endblock %}
```

**Lợi ích:** Bạn chỉ cần sửa Header ở đúng 1 file `base.html`, toàn bộ 100 trang con sẽ thay đổi theo ngay lập tức!

---

## 4. Ghép nối Template (Template Partials với `include`)

Bên cạnh `extends`, Django cung cấp một công cụ mạnh mẽ khác là `{% include %}`. Nếu `extends` là việc **"Xây từ dưới lên"** (Tạo khung xương, trang con điền nội dung vào), thì `include` là **"Lắp ghép từ trên xuống"** (Chia nhỏ các bộ phận và nhúng vào một file lớn).

### Khi nào dùng `extends`? Khi nào dùng `include`?

*   **Dùng `{% extends %}`:** Khi bạn muốn tạo ra một cái **Layout tổng thể** (Master Layout) dùng chung cho nhiều trang (ví dụ: `base.html`). Bất cứ trang nào (`home.html`, `detail.html`) cũng bắt buộc phải tuân theo cái khung này.
    *   *Tư duy:* Trang con xin ké vào trang cha.
*   **Dùng `{% include %}`:** Khi bạn có một đoạn code HTML lặp đi lặp lại hoặc quá dài, bạn cắt nó ra thành một file nhỏ (Component) để **nhúng vào nhiều nơi** hoặc giúp file chính ngắn gọn, dễ đọc.
    *   *Tư duy:* Trang cha chủ động hút các mảnh Lego con vào để lắp ráp.

### Cách sử dụng `{% include %}`

Bạn gọi đường dẫn của file con. Django sẽ lấy nội dung file đó chèn vào đúng vị trí này:

```html
<!-- base_pro.html (File gốc) -->
<body>
    <!-- Nhúng Header vào đây -->
    {% include 'components/header.html' %}
    
    <div class="content">
        <!-- Nhúng Sidebar vào đây -->
        {% include 'components/sidebar.html' %}
    </div>
</body>
```

---

## 5. Static Files (File tĩnh)

Để nhúng CSS, JavaScript hay Hình ảnh vào Template, Django cung cấp thẻ `{% load static %}`.

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

---

**Chúc mừng bạn!** Bạn đã hoàn thành 6 Phase đào sâu về bản chất của Django. 
1.  **Request/Response Cycle:** Luồng đi của gói tin.
2.  **URLs:** Lễ tân điều phối.
3.  **Views:** Bộ não xử lý.
4.  **Models & ORM:** Trái tim dữ liệu.
5.  **Forms:** Người gác cổng an ninh.
6.  **Templates:** Công xưởng giao diện.

Giờ đây, bạn đã không còn là người "copy code tutorial" nữa, mà đã hiểu thực sự những gì đang diễn ra dưới gầm máy. Bạn đã sẵn sàng để quay lại và nâng cấp Todo App lên một tầm cao mới chưa?
