# Google Cloud cơ bản

## 1. Google Cloud Console là gì?

Google Cloud Console là nơi quản lý hạ tầng của dự án trên Google Cloud.

Trong một project thực tế, Google Cloud có thể chứa nhiều thành phần như:

- BE server
- FE app
- Database
- Logs
- Error Reporting
- Job / Migration
- Cronjob / Scheduler
- Monitoring
- Storage file
- Permission / IAM

Với developer mới vào dự án, không cần học toàn bộ Google Cloud. Chỉ cần nắm các phần mà dự án đang dùng và phục vụ cho việc debug, kiểm tra deploy, kiểm tra database, log và cronjob.

---

## 2. Project và Environment

Trong Google Cloud, mỗi hệ thống thường được chia theo project hoặc service tương ứng với môi trường.

Ví dụ:

- Staging: môi trường test / QA / nội bộ
- Live / Production: môi trường thật người dùng đang sử dụng

Khi debug, bước đầu tiên luôn là xác định mình đang kiểm tra môi trường nào:

```text
STG hay LIVE?
```

Sau đó mới xác định tiếp service, database, log hoặc cronjob tương ứng.

---

## 3. Cloud Run là gì?

Cloud Run là nơi chạy các service của hệ thống.

Trong dự án, có thể thấy các service như:

```text
wky-api-staging
wky-api-live
wky-app-staging
wky-app-live
lift-drive-api
lift-drive-app
lift-drive-api-migrate
```

Cách hiểu:

```text
wky-api-staging = BE staging
wky-api-live    = BE live/production
wky-app-staging = FE staging
wky-app-live    = FE live/production
xxx-migrate     = job/migration hoặc task chạy một lần
```

Kết luận quan trọng:

```text
BE/FE của dự án đang chạy bằng Cloud Run Service.
```

---

## 4. Cloud Run Logs dùng để làm gì?

Cloud Run Logs dùng để xem log của một service cụ thể.

Ví dụ muốn xem log BE staging:

```text
Cloud Run
→ wky-api-staging
→ Observability
→ Logs
```

Dùng khi:

- API bị lỗi 500
- Tester báo lỗi trên STG
- Cần xem exception/traceback
- Cần kiểm tra request có chạy vào BE không
- Cần xem log sau khi deploy

Một số keyword thường search trong log:

```text
Traceback
Exception
ERROR
OperationalError
Unknown column
Migration
NodeNotFoundError
```

Cách nhớ:

```text
Biết service nào lỗi
→ vào Cloud Run Logs của service đó
```

---

## 5. Error Reporting là gì?

Error Reporting là nơi gom nhóm các lỗi exception/crash của app.

Nó giúp xem nhanh:

- App đang lỗi gì
- Lỗi xảy ra ở service nào
- Lỗi xảy ra lúc nào
- Stack trace chính là gì
- Lỗi này lặp lại bao nhiêu lần

Khác với Cloud Run Logs, Error Reporting không bắt đầu bằng việc chọn service trước. Nó là màn cấp project.

Flow:

```text
Chọn đúng project STG/LIVE
→ vào Error Reporting
→ filter service/time range nếu cần
```

Ví dụ lỗi từng gặp:

```text
NodeNotFoundError
Migration 0032_backfill_month_of_work
dependencies reference nonexistent parent node 0029...
```

và:

```text
Unknown column 'employee.last_experience_incremented_date'
```

Khi ghép lại có thể hiểu:

```text
Code đã dùng field mới
nhưng DB chưa có column mới
vì migration bị fail hoặc thiếu dependency
```

---

## 6. Logs Explorer là gì?

Logs Explorer là nơi search/filter log toàn project.

So sánh nhanh:

```text
Cloud Run Logs
→ xem nhanh log của 1 service cụ thể

Logs Explorer
→ search log toàn project, filter mạnh hơn

Error Reporting
→ xem lỗi exception đã được gom nhóm
```

Cách dùng thực tế:

```text
Biết service nào lỗi
→ Cloud Run Logs

Chưa biết lỗi nằm ở service nào
→ Logs Explorer

Muốn xem lỗi chính/stack trace dễ đọc
→ Error Reporting
```

Với level cơ bản, chỉ cần biết Logs Explorer dùng để search rộng khi chưa biết lỗi nằm ở đâu.

---

## 7. Cloud SQL là gì?

Cloud SQL là nơi quản lý database của dự án.

Ví dụ trong project có instance:

```text
wky-api-db-live
```

Cách hiểu:

```text
Cloud SQL Instance = DB server
Database = database thật nằm bên trong instance
```

Ví dụ:

```text
wky-api-db-live
→ Cloud SQL instance

Bên trong có database app
→ chứa các table như employee, task, project...
```

Cách vào từ Home:

```text
Home
→ Menu trái
→ Cloud SQL
→ Instances
```

Hoặc:

```text
View all products
→ Databases
→ Cloud SQL
```

Các tab cần biết:

```text
Overview
→ xem thông tin DB server, version, CPU, memory, connection info

Databases
→ xem database bên trong instance

Backups
→ xem backup

Cloud SQL Studio
→ nơi login DB và gõ SQL để xem data
```

---

## 8. Cloud SQL Studio dùng để làm gì?

Cloud SQL Studio là nơi có thể login vào database và chạy SQL trực tiếp trên Google Cloud.

Dùng để xem data hoặc kiểm tra schema.

Một số câu query an toàn:

```sql
SHOW DATABASES;
```

```sql
SHOW TABLES;
```

```sql
DESCRIBE employee;
```

```sql
SHOW COLUMNS FROM employee;
```

```sql
SELECT *
FROM employee
LIMIT 10;
```

Kiểm tra column có tồn tại không:

```sql
SHOW COLUMNS FROM employee LIKE 'last_experience_incremented_date';
```

Nguyên tắc quan trọng:

```text
STG: có thể SELECT để kiểm tra nếu được phép
LIVE: chỉ SELECT khi được confirm
Không UPDATE / DELETE / INSERT / ALTER / DROP nếu chưa được phép
```

Không tự ý thao tác:

```text
Restart DB
Stop DB
Delete DB
Edit connection
Change user/password
Import/Export
Create backup
```

---

## 9. Cloud Run Revisions là gì?

Cloud Run Revision là version deploy của một Cloud Run Service.

Cách hiểu:

```text
Cloud Run Service = app đang chạy
Revision = một version deploy của app
```

Ví dụ:

```text
wky-api-staging
→ service BE staging

wky-api-staging-00495-bzv
→ revision/version deploy
```

Mỗi lần deploy code mới lên Cloud Run, thường sẽ tạo revision mới.

Trong tab Revisions cần xem:

```text
Revision name
Traffic
Deployed
Image
Status
```

Ý nghĩa:

```text
Traffic 100%
→ revision đang nhận toàn bộ request hiện tại

Deployed
→ thời điểm deploy

Image
→ container image đang chạy

Status / tick xanh
→ revision đang ready hay lỗi
```

Cách đọc quan trọng nhất:

```text
Revision nào Traffic 100%
→ version đang chạy thật

Revision nào Traffic 0%
→ version cũ, không nhận request
```

Dùng khi cần kiểm tra:

- Code đã deploy lên STG chưa
- Revision mới nhất được deploy lúc nào
- Sau deploy lỗi có bắt đầu xuất hiện không
- Service đang chạy image nào

Không tự bấm:

```text
Manage traffic
Rollback
Edit & deploy new revision
Delete revision
```

---

## 10. Cloud Run Job là gì?

Cloud Run Job là task chạy một lần rồi kết thúc.

Khác với Cloud Run Service:

```text
Cloud Run Service
→ chạy liên tục, nhận request API/web

Cloud Run Job
→ chạy một lần, xong thì completed/fail
```

Ví dụ job có thể dùng để:

- Run migration
- Backfill data
- Sync data
- Import/export
- Recalculate dữ liệu
- Chạy command nội bộ

Ví dụ:

```text
lift-drive-api-migrate
```

Có thể là job dùng để chạy migration.

Cách xem:

```text
Cloud Run
→ Jobs
→ chọn job
→ History / Executions
→ Logs
```

Cần xem:

```text
Execution ID
Creation time
Status
End time
Logs
```

Không tự bấm:

```text
Execute
Edit job configuration
Delete
```

Vì bấm Execute có thể chạy migration/job thật.

---

## 11. Cloud Scheduler là gì?

Cloud Scheduler là nơi đặt lịch chạy cronjob.

Cách hiểu đơn giản:

```text
Cloud Scheduler = đồng hồ hẹn giờ
Cloud Run Job / API = việc được gọi để chạy
```

Cloud Scheduler không chứa logic nghiệp vụ. Nó chỉ đến giờ thì gọi một target.

Ví dụ:

```text
Mỗi ngày 17:30
→ gọi API /api/daily-report/cron-alert-daily-violation
→ BE xử lý logic gửi alert
```

Trong Cloud Scheduler cần xem:

```text
Name
Status of last execution
Region
State
Frequency
Target
Last run
Next run
```

Ý nghĩa:

```text
Name
→ tên cronjob

Frequency
→ lịch chạy

Target
→ gọi tới đâu

Last run
→ lần chạy gần nhất

Status of last execution
→ lần chạy gần nhất success/fail

Next run
→ lần chạy tiếp theo
```

Ví dụ:

```text
wky-api-live-alert-daily-violation
```

Target:

```text
https://wky-api-live-...run.app/api/daily-report/cron-alert-daily-violation
```

Flow:

```text
Cloud Scheduler
→ gọi URL API
→ wky-api-live nhận request
→ BE chạy logic cron
```

Không tự bấm:

```text
Force run
Pause
Resume
Edit
Delete
Create job
```

Vì Force run sẽ chạy cron ngay lập tức.

---

## 12. Job khác gì Scheduler?

Bảng nhớ nhanh:

| Thành phần        | Vai trò               | Cách chạy                      |
| ----------------- | --------------------- | ------------------------------ |
| Cloud Scheduler   | Hẹn giờ               | Đến giờ thì gọi target         |
| Cloud Run Service | App/API chạy liên tục | Nhận request từ user hoặc cron |
| Cloud Run Job     | Task chạy một lần     | Chạy xong thì dừng             |

Ví dụ Scheduler gọi API:

```text
Cloud Scheduler
→ gọi URL /api/daily-report/cron-alert-daily-violation
→ Cloud Run Service wky-api-live xử lý
```

Ví dụ Scheduler gọi Job:

```text
Cloud Scheduler
→ trigger Cloud Run Job
→ Job chạy command
→ Job completed/fail
```

Câu nhớ ngắn:

```text
Scheduler = lịch gọi
Job = task được chạy
Service/API = nơi nhận request và xử lý logic
```

---

## 13. Monitoring dùng để làm gì?

Monitoring / Observability dùng để quan sát sức khỏe hệ thống.

Các phần hay gặp:

```text
Logs Explorer
Error Reporting
Metrics
Dashboard
Alerting
```

Dùng để xem:

- Request count
- Error count
- Latency
- CPU
- Memory
- DB connections
- Storage
- Service có đang lỗi nhiều không
- Sau deploy error có tăng không
- API có bị chậm không

Với người mới, chỉ cần nắm:

```text
Log/error
→ xem trong Monitoring / Observability

Service cụ thể
→ xem trong Cloud Run Observability

DB performance
→ xem trong Cloud SQL Overview / System insights
```

---

## 14. IAM & Admin là gì?

IAM & Admin dùng để quản lý phân quyền trong Google Cloud.

Cần hiểu 2 khái niệm:

```text
IAM
→ phân quyền ai được làm gì trong project

Service Account
→ tài khoản máy/service dùng để chạy app, job, deploy
```

Ví dụ:

```text
Cloud Run service chạy bằng service account nào?
Job migrate chạy bằng service account nào?
Ai có quyền xem log?
Ai có quyền execute job?
Tại sao mình không thấy một số menu?
```

Với developer mới, chỉ cần biết để đọc hiểu. Không tự cấp quyền hoặc chỉnh quyền nếu chưa được giao.

---

## 15. Cloud Storage là gì?

Cloud Storage dùng để lưu file/object.

Ví dụ:

- File upload
- Export report
- File Excel/CSV
- Backup file
- Static/media file

Nếu dự án có chức năng upload/download/export report, có thể sẽ liên quan Cloud Storage.

Với level cơ bản, chỉ cần biết:

```text
Cloud Storage = nơi lưu file
Bucket = thư mục/container chứa file
Object = file cụ thể
```

Không tự xóa/sửa file trên bucket live nếu chưa được confirm.

---

## 16. Một số phần khác có thể gặp nhưng chưa cần học sâu

### APIs & Services

Dùng để bật/tắt API của Google Cloud.

Ví dụ:

```text
Cloud Run API
Cloud SQL Admin API
Cloud Scheduler API
Google Drive API
Google Maps API
```

Chỉ cần biết để kiểm tra API đã enable chưa. Không tự enable/disable nếu chưa confirm.

### VPC Network

Liên quan network nội bộ, private IP, firewall.

Ví dụ:

```text
Cloud Run connect Cloud SQL qua private IP
Service connect nội bộ
Firewall/network config
```

Phần này thường DevOps/Infra xử lý.

### Compute Engine

Là máy ảo VM.

Chỉ cần quan tâm nếu project có server, bastion hoặc tool nội bộ chạy trên VM.

### Kubernetes Engine

Dùng nếu hệ thống chạy bằng Kubernetes/GKE.

Nếu BE/FE đang chạy Cloud Run thì tạm thời chưa cần học sâu Kubernetes.

### BigQuery

Dùng cho data warehouse, analytics, report lớn.

Debug BE hằng ngày thường chưa cần đụng.

### Security

Liên quan bảo mật, policy, secret, certificate.

Chỉ xem khi team hướng dẫn hoặc khi có task liên quan.

---

## 17. Flow debug cơ bản trên Google Cloud

Khi tester hoặc PM báo lỗi, có thể đi theo flow:

```text
1. Xác định môi trường
   - STG hay LIVE

2. Xác định service
   - BE: wky-api-staging / wky-api-live
   - FE: wky-app-staging / wky-app-live

3. Nếu biết service lỗi
   → vào Cloud Run Logs

4. Nếu thấy exception lặp lại
   → vào Error Reporting

5. Nếu chưa biết lỗi nằm ở đâu
   → vào Logs Explorer

6. Nếu lỗi liên quan DB/schema/column
   → vào Cloud SQL / Cloud SQL Studio kiểm tra

7. Nếu lỗi liên quan migration/job
   → vào Cloud Run Jobs kiểm tra execution/log

8. Nếu lỗi liên quan cron chạy định kỳ
   → vào Cloud Scheduler xem last run/target
```

---

## 18. Cách nhớ nhanh theo loại lỗi

```text
App/API lỗi
→ Cloud Run Logs / Error Reporting

Không biết lỗi ở service nào
→ Logs Explorer

DB lỗi / thiếu column / check data
→ Cloud SQL / Cloud SQL Studio

Migration lỗi
→ Cloud Run Jobs

Cron không chạy / chạy fail
→ Cloud Scheduler

Deploy chưa ăn code
→ Cloud Run Revisions

Không có quyền
→ IAM & Admin

File/export/upload lỗi
→ Cloud Storage
```

---

## 19. Những nguyên tắc an toàn

Khi mới học hoặc mới vào dự án, ưu tiên chỉ xem, không chỉnh sửa.

Không tự bấm:

```text
Execute job
Force run scheduler
Restart service/database
Stop service/database
Delete resource
Edit config
Manage traffic
Rollback
Import/Export DB
Change user/password
Change IAM permission
```

Đặc biệt với môi trường LIVE/Production:

```text
Chỉ xem log/thông tin nếu được phép
Chỉ SELECT DB khi được confirm
Không chạy migration/job/cron thủ công nếu chưa có xác nhận
```

---

## 20. Thứ tự học đề xuất

Với developer BE mới vào dự án, nên học theo thứ tự:

```text
1. Cloud Run
2. Cloud Run Logs
3. Error Reporting
4. Logs Explorer
5. Cloud SQL
6. Cloud SQL Studio
7. Cloud Run Revisions
8. Cloud Run Jobs
9. Cloud Scheduler
10. IAM & Service Account basic
11. Cloud Storage basic nếu dự án có upload/export file
```

Các phần chưa cần học sâu ngay:

```text
VPC Network
Kubernetes Engine
Compute Engine
BigQuery
Security
Billing
Marketplace
Agent Platform
Google Maps Platform
```

---

## 21. Kết luận

Google Cloud trong dự án có thể hiểu đơn giản là nơi quản lý toàn bộ hạ tầng chạy app.

Với level cơ bản, chỉ cần nhớ:

```text
Cloud Run
→ nơi chạy BE/FE service

Cloud SQL
→ nơi chứa database

Monitoring / Logs Explorer / Error Reporting
→ nơi xem log và lỗi

Cloud Run Revisions
→ nơi xem version deploy đang chạy

Cloud Run Jobs
→ nơi xem job/migration/task chạy một lần

Cloud Scheduler
→ nơi xem cronjob/lịch chạy tự động

IAM & Admin
→ nơi quản lý quyền và service account

Cloud Storage
→ nơi lưu file/export/upload
```

Mục tiêu ban đầu không phải là biết hết Google Cloud, mà là biết vào đúng chỗ khi cần debug:

```text
Lỗi app → xem Cloud Run Logs / Error Reporting
Lỗi DB → xem Cloud SQL
Lỗi migration → xem Cloud Run Jobs
Lỗi cron → xem Cloud Scheduler
Lỗi deploy → xem Cloud Run Revisions
```
