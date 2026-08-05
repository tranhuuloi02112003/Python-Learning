# 1 Project Có Thể Vừa Có DRF, Vừa Có ninja-extra

> Tiếp theo bài 08-09. Bài ngắn — chỉ mô tả 1 điểm cần biết trước khi đọc code trong repo `leadplusone_api`, để không bất ngờ khi mở nhầm 1 file DRF cũ giữa lúc đang học ninja-extra.

---

## 1. Vì Sao Có Thể Trộn Lẫn 2 Framework Trong Cùng 1 Project?

```text
DRF và ninja-extra đều chỉ là "tầng viết API" nằm trên Django — cả hai đều dùng chung
model, ORM, settings, migrations của Django. Chuyển từ DRF sang ninja-extra không đụng
tới database hay business logic, chỉ đổi cách viết controller/view + routing.
```

Vì vậy, 1 project không bắt buộc phải chuyển hết cùng lúc — có thể chuyển dần từng phần (feature app), phần chưa chuyển vẫn chạy bình thường song song.

---

## 2. Ví Dụ Thật — `leadplusone_api`

Repo này đang ở trạng thái **migrate dở dang**, không phải đã chọn hẳn 1 framework:

```text
Đã chuyển sang ninja-extra:
    F26 (My Page — chứa article_writer.py), F51 (Credit), F21 (GA4),
    F16 (SEO), F27 (ChatBot), F17 (Feedback), F15 (FAQs ChatBot), F22 (GSC), F29, F94

Vẫn còn DRF thuần (chưa chuyển):
    F11 (Auth) — dùng APIView/GenericAPIView (MPF_WEB_F11_Auth/views.py)
    F14 (FAQs), F91 (Notice) — vẫn dùng serializers.Serializer
```

Root `leadplus_one/urls.py` include cả 2 kiểu app cùng lúc, và còn wire `drf_yasg` (`get_schema_view(...)`) — Swagger riêng cho phần DRF — chạy song song với các trang OpenAPI riêng của từng app ninja-extra (bài 09, mục 1).

---

## 3. Ý Nghĩa Khi Đọc Code

```text
Nếu mở MPF_WEB_F26_My_Page/controllers/article_writer.py → đây là module MỚI, viết theo ninja-extra.
Nếu mở MPF_WEB_F11_Auth/views.py                          → đây là module CŨ, vẫn là DRF thuần.
```

Không có gì sai khi thấy 2 style khác nhau trong cùng 1 repo — đơn giản là project đang chuyển dần, module nào được viết lại gần đây thì theo ninja-extra, module nào chưa động tới thì vẫn giữ nguyên DRF cũ.

---

Bài 01-10 đã đủ để đọc hiểu `article_writer.py` từ đầu tới cuối. Các bài tiếp theo (`11` trở đi) đi vào những chủ đề của Ninja/ninja-extra mà file này không dùng tới, nhưng vẫn cần biết vì có thể gặp ở feature app khác trong repo, hoặc cần dùng khi viết endpoint mới. Bắt đầu từ `11-query-va-form-data.md`.
