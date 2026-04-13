# Tổng quan về GSD (Get-Shit-Done)

## 1. GSD là gì?
GSD không phải là một thư viện code, mà là một "Hệ điều hành quy trình" chạy trên nền các AI Agent (như Antigravity, Claude Code).
- **Mục tiêu**: Chống lại sự "lú lẫn" của AI khi dự án quá lớn (Context Rot).
- **Cơ chế**: Chia dự án thành các phần nhỏ, ép AI làm việc theo trình tự nghiêm ngặt thay vì để nó tự code theo cảm hứng.

## 2. Các lệnh GSD cốt lõi và Thời điểm sử dụng

| Nhóm lệnh | Lệnh cụ thể | Sử dụng khi nào? |
| :--- | :--- | :--- |
| **KHỞI TẠO** | `/gsd-new-project` | Khi bắt đầu một dự án mới hoàn toàn (Greenfield). |
| | `/gsd-map-codebase` | **Quan trọng nhất**: Khi làm việc trên dự án có sẵn của công ty (Brownfield). |
| **QUY TRÌNH** | `/gsd-discuss-phase [n]` | Bắt đầu một tính năng mới (Phase n). Dùng để chốt yêu cầu/giao diện. |
| | `/gsd-plan-phase [n]` | Sau khi thảo luận. AI sẽ liệt kê các bước code cụ thể (file nào, sửa gì). |
| | `/gsd-execute-phase [n]` | Khi bạn đã duyệt Plan. AI bắt đầu viết code và tự động Git Commit. |
| | `/gsd-verify-work [n]` | Khi code xong. Dùng để kiểm tra lỗi, chạy thử và hoàn thiện. |
| **TIỆN ÍCH** | `/gsd-next` | Lệnh "lười": Tự động nhảy sang bước tiếp theo trong quy trình. |
| | `/gsd-quick [nội dung]` | Cần sửa nhanh lỗi nhỏ, typo, màu sắc (bỏ qua các bước Discuss/Plan). |
| | `/gsd-note [ý tưởng]` | Đang làm mà nảy ra ý tưởng mới nhưng chưa muốn làm ngay. |

## 3. Luồng phát triển 1 tính năng mới (Ví dụ: Level Assessment)
Đây là quy trình từ A đến Z bạn nên áp dụng trong Antigravity để tận dụng tối đa GSD:

**Giai đoạn 1: Đồng bộ ngữ cảnh**
- **Mở branch mới**: Luôn tạo một branch git mới cho tính năng này.
- **Quét dự án**: Gõ `/gsd-map-codebase` để AI hiểu cấu trúc React/Vite/Tailwind hiện tại của team Liftsoft.

**Giai đoạn 2: Phân tích & Chia Phase (`/gsd-discuss`)**
- **Cung cấp tài liệu**: Bạn gửi file mô tả tính năng hoặc ảnh chụp thiết kế Chart.
- **Kích hoạt**: Gõ `/gsd-discuss-phase 1` (Ví dụ: Dựng khung và Biểu đồ).
- **Thảo luận**: Bạn và AI chốt xem dùng thư viện Highcharts bản nào, data format ra sao, component tách như thế nào.

**Giai đoạn 3: Lập kế hoạch thực thi (`/gsd-plan`)**
- **Lệnh**: `/gsd-plan-phase 1`.
- **Kiểm tra**: AI sẽ liệt kê các task:
  - Task 1: Tạo `LevelAssessmentChart.tsx`.
  - Task 2: Viết custom hook `useSkillData.ts`.
  - Task 3: Cấu hình Radar Chart options.
- **Duyệt**: Nếu bạn thấy Plan ổn (đã tách logic ra khỏi UI theo Clean Code), hãy chuyển sang bước tiếp theo.

**Giai đoạn 4: Code & Commit tự động (`/gsd-execute`)**
- **Lệnh**: `/gsd-execute-phase 1`.
- **Theo dõi**: AI bắt đầu viết code. Xong Task 1, nó sẽ tự tạo commit: `feat(assessment): create radar chart component`.
- **Kiểm soát**: Bạn nhìn trực tiếp code trên màn hình Antigravity, nếu thấy nó viết sai, bạn có thể ngắt lệnh và bảo nó sửa lại ngay.

**Giai đoạn 5: Kiểm tra & Nghiệm thu (`/gsd-verify`)**
- **Lệnh**: `/gsd-verify-work 1`.
- **Test**: Bạn mở trình duyệt check xem Highcharts có hiển thị đúng không.
- **Sửa lỗi**: Nếu có lỗi, AI sẽ sửa và tạo commit fix cho đến khi bạn hài lòng.

**Giai đoạn 6: Kết thúc**
- **Lệnh**: `/gsd-next` để chuyển sang Phase tiếp theo (ví dụ: Phase 2 kết nối API thật).

## 4. Tại sao bạn (Frontend Intern) nên dùng GSD?
- **Lên trình quản lý**: Bạn học được cách chia task bài bản như một Senior thay vì cắm đầu vào code ngay.
- **Lịch sử Git sạch đẹp**: Khi Leader xem code, họ sẽ thấy các commit cực kỳ chuyên nghiệp và dễ hiểu.
- **Hạn chế lỗi**: AI sẽ không vô tình sửa/xóa nhầm code cũ vì nó luôn bám sát file `STATE.md` và `PLAN.md` nội bộ.

## 5. Các lệnh GSD Mở rộng (Nâng cao)
Phần này bổ sung thêm các nhóm lệnh giúp bạn làm chủ quy trình và xử lý các tình huống phát sinh:

**Nhóm 1: Chuyên gia Debug & Review Code (Cực hay cho Intern)**
- `/gsd-code-review`: Làm xong một Phase, thay vì tự push code lên chờ Sếp chửi, gõ lệnh này. AI sẽ đóng vai một Senior Developer khó tính soi từng dòng code bạn (hoặc AI) vừa viết xem có lỗi bảo mật, chậm logic, bị lặp code hay không.
- `/gsd-code-review-fix`: Đi cặp với lệnh trên. Sau khi liệt kê một đống lỗi trong file `REVIEW.md`, gõ tiếp lệnh này, AI sẽ tự động nhảy vào sửa (fix code) cho đạt chuẩn Clean Code.
- `/gsd-debug`: Khi gặp một cái bug "trời ơi đất hỡi". GSD sẽ tạm dừng việc build tính năng mới, tạo một quy trình "khám nghiệm tử thi" siêu logic để truy vết lỗi trên toàn bộ hệ thống thay vì để bạn đoán mò.

**Nhóm 2: "Quay xe" và Đổi Lộ trình (Phase Management)**
*Tình huống: Đang làm bài ngon ơ thì sếp bảo "Ê em, làm thêm cho anh cái giao diện này trước đi". Cấu trúc roadmap bị phá vỡ!*
- `/gsd-insert-phase`: Đây là lệnh "cứu mạng", cho phép bạn chèn khẩn cấp một tính năng (Ví dụ Phase 1.5) vào giữa lịch trình mà không làm rối file `ROADMAP.md` cũ.
- `/gsd-add-phase`: Bổ sung thêm Phase vào đuôi của lộ trình dự án hiện tại.
- `/gsd-undo`: Rollback (Cỗ máy thời gian). Đang làm `/gsd-execute-phase` mà thấy AI viết code đi vào ngõ cụt, chạy lệnh này để nó sạch sẽ Git Revert lại toàn bộ thay đổi vừa diễn ra, khôi phục source code y như cũ không rớt một nhịp.

**Nhóm 3: Dành riêng cho dân Frontend (UI/UX)**
- `/gsd-ui-phase`: Sinh ra một file `UI-SPEC.md`. Cực kì lợi hại khi bạn đang code React/Tailwind. Trước khi code, lệnh này ép AI làm rõ: "Màu primary là mã hex gì? Spacing margin dùng mấy pixel? Shadows đổ bóng ra sao để thống nhất toàn bộ trang web?".
- `/gsd-ui-review`: Sau khi code xong giao diện, lệnh này giúp đánh giá lại code frontend dựa trên 6 nguyên tắc tiêu chuẩn (vd: kiểm tra xem nút bấm có đồng bộ không, có chỗ nào chèn ép padding sai không...).

**Nhóm 4: Quản lý Quỹ thời gian / Việc lặt vặt rảnh tay**
- `/gsd-add-todo` & `/gsd-check-todos`: Không to tát như Phase, chỉ là cái Todo list. Gặp việc nhỏ nhẹ như "Chỉnh font tí", "Đổi tên biến user thành account", ném vào Todo, sau đó bảo AI list ra và bốc từng cái làm dần.
- `/gsd-pause-work` & `/gsd-resume-work`: Tới giờ về đi chơi / đi ngủ. Lệnh pause giúp AI gom gọn lại state đang làm tới đâu (Context Handoff). Hôm sau bật máy lên gõ resume, AI sẽ tự biết: "Hôm qua tôi đang dở tay code cái Radar Chart, để tôi làm tiếp cho sếp". Trí nhớ không bị đứt đoạn!

💡 **Mẹo dọn dẹp**: Hôm nào rảnh rỗi dọn rác dự án dư âm, gõ `/gsd-cleanup`, AI sẽ đi dọn dẹp lại các thư mục nháp hay file log không cần thiết. Đừng ngần ngại khám phá các lệnh mồi này, nó sẽ luyện cho bạn kỹ năng dùng Tool cực bén!

> **Lời khuyên cuối**: Hãy bắt đầu bằng lệnh `/gsd-help` ngay trong Antigravity để AI của bạn hiển thị danh sách lệnh và xác nhận nó đã sẵn sàng đồng hành cùng bạn theo quy trình này!
