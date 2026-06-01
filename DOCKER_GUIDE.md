# Docker Guide Cho Lift WKY API

Tài liệu này giải thích Docker theo đúng flow của project hiện tại. Mục tiêu là khi mở các file như `Dockerfile`, `docker-compose-local.yaml`, `.env_dev`, `.env_staging`, bạn hiểu app đang chạy từ đâu, đọc config ở đâu, và khác nhau giữa local/staging/live như thế nào.

## 1. Docker Là Gì?

Docker là công cụ đóng gói app cùng môi trường chạy của app.

Nếu không dùng Docker, mỗi máy dev phải tự cài:

- Python đúng version.
- MySQL đúng version.
- Thư viện hệ thống.
- Biến môi trường.
- Cách chạy server.

Nếu dùng Docker, project mô tả các thứ đó bằng file. Sau đó Docker tạo ra môi trường chạy giống nhau hơn giữa máy dev, staging và live.

Nói đơn giản:

- `Dockerfile`: công thức để build ra image.
- `Image`: bản đóng gói app + môi trường.
- `Container`: một image đang được chạy.
- `docker-compose`: file dùng để chạy nhiều container cùng lúc, ví dụ app Django + MySQL.

Ví dụ dễ hiểu:

```text
Dockerfile  -> build -> Image
Image       -> run   -> Container
```

## 2. Vì Sao Project Này Dùng Docker?

Project này là Django API. Khi chạy cần nhiều thứ đi cùng nhau:

- Source code Django trong `source_code/`.
- File env để biết đang là local/dev/staging/live.
- Database MySQL.
- Lệnh migrate database.
- Lệnh runserver hoặc chạy trên Cloud Run.
- Một số config deploy lên Google Cloud.

Docker giúp project chạy được theo cùng một flow:

```text
source code + env + dependencies -> Docker image -> Docker container
```

Ở local, project chạy bằng Docker Compose:

```text
api-server container + mysql-server container
```

Ở staging/live, project build Docker image rồi deploy lên Google Cloud Run.

## 3. Các File Docker Chính Trong Project

Các file quan trọng nhất:

```text
_build_local/_docker_compose/docker-compose-local.yaml
_build_local/_dockerfile/local/Dockerfile.workify_api_web.local
_build_local/_docker_compose/_init.sh

gcp_builder/dockerfile/Dockerfile.staging
gcp_builder/dockerfile/Dockerfile.live
gcp_builder/build_and_deploy.sh
gcp_builder/deploy_scheduler.sh

source_code/.env_local
source_code/.env_dev
source_code/.env_staging
source_code/.env_live
source_code/main/settings.py
```

Trong đó:

- Local chủ yếu xem `_build_local/...`.
- Staging/live chủ yếu xem `gcp_builder/...`.
- Django luôn đọc file `.env` trong thư mục `source_code/`, không tự đọc trực tiếp `.env_dev`, `.env_staging`, `.env_live`.

## 4. Flow Local

Local dùng file:

```text
_build_local/_docker_compose/docker-compose-local.yaml
```

Trong file này có 2 service chính:

```text
mysql-server
api-server
```

### mysql-server

Đây là container MySQL.

Nó có tên container:

```text
wky_api_db
```

Điểm quan trọng: trong Docker network, container Django có thể gọi database bằng host `wky_api_db`.

Vì vậy trong env local/dev thường thấy:

```text
DATABASE_HOST='wky_api_db'
```

Nó không dùng `localhost` vì bên trong container, `localhost` là chính container đó, không phải MySQL container.

### api-server

Đây là container chạy Django API.

Trong `docker-compose-local.yaml`, service này:

- Build từ Dockerfile local.
- Mount source code vào `/wky_api`.
- Chạy command `bash /_setup/_init.sh runserver`.
- Map port `19000:443`.

Port mapping nghĩa là:

```text
Máy bạn:19000 -> Container:443
```

Nên khi gọi API từ máy local, thường dùng:

```text
http://localhost:19000
```

## 5. Flow Local Chi Tiết

Flow local có thể hiểu như sau:

```text
docker-compose-local.yaml
        |
        | build api-server
        v
Dockerfile.workify_api_web.local
        |
        | copy source_code vào /wky_api
        | copy env vào /wky_api/.env
        v
container api-server
        |
        | chạy /_setup/_init.sh runserver
        v
python manage.py migrate
python manage.py runserver 0.0.0.0:443
```

File `_build_local/_docker_compose/_init.sh` có flow quan trọng:

```sh
python manage.py migrate
python manage.py runserver 0.0.0.0:443
```

Nghĩa là khi container API start, nó migrate database trước rồi mới chạy Django server.

## 6. Dockerfile Local Đang Làm Gì?

File:

```text
_build_local/_dockerfile/local/Dockerfile.workify_api_web.local
```

Ý chính:

```dockerfile
FROM python:3.12
COPY source_code/ /wky_api/
COPY source_code/.env_dev /wky_api/.env
ENTRYPOINT ["bash", "/_setup/_init.sh"]
```

Giải thích:

- `FROM python:3.12`: image này bắt đầu từ môi trường Python 3.12.
- `COPY source_code/ /wky_api/`: copy source code vào trong container.
- `COPY source_code/.env_dev /wky_api/.env`: copy `.env_dev` thành `.env`.
- `ENTRYPOINT`: khi container chạy thì gọi script init.

Lưu ý quan trọng: Dockerfile local hiện đang copy `.env_dev`, không phải `.env_local`.

```text
source_code/.env_dev -> /wky_api/.env
```

Nhưng do `docker-compose-local.yaml` có mount:

```text
${CURRENT_SOURCE_PATH}/source_code:/wky_api
```

thư mục source trên máy bạn sẽ được gắn vào `/wky_api` trong container. Vì vậy thực tế local có thể phụ thuộc vào file `.env` hiện có trong `source_code/` trên máy bạn.

Muốn biết local đang đọc env nào thì xem file:

```text
source_code/.env
```

## 7. Django Đọc Env Ở Đâu?

File:

```text
source_code/main/settings.py
```

Có đoạn:

```py
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
```

Nghĩa là Django đọc:

```text
source_code/.env
```

Nó không tự động đọc:

```text
source_code/.env_dev
source_code/.env_staging
source_code/.env_live
```

Các file `.env_dev`, `.env_staging`, `.env_live` chỉ là nguồn. Khi build Docker, Dockerfile sẽ copy một file env phù hợp thành `.env`.

Ví dụ staging:

```text
.env_staging -> /wky_api/.env
```

Ví dụ live:

```text
.env_live -> /wky_api/.env
```

Sau đó Django chỉ đọc `/wky_api/.env`.

## 8. Env Local, Dev, Staging, Live Khác Nhau Như Nào?

Các file env chính:

```text
source_code/.env_local
source_code/.env_dev
source_code/.env_staging
source_code/.env_live
```

Trong đó có biến quan trọng:

```text
ENV_TYPE
CURRENT_URL
CLIENT_URL
DATABASE_HOST
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

Ví dụ:

```text
local/dev DATABASE_HOST = wky_api_db
staging DATABASE_HOST  = /cloudsql/...
live DATABASE_HOST     = /cloudsql/...
```

Ý nghĩa:

- Local/dev kết nối tới MySQL container trong Docker network.
- Staging/live kết nối tới Cloud SQL trên Google Cloud.

Trong `settings.py`, project tạo các cờ:

```py
IS_PRODUCTION = env("ENV_TYPE") == "live"
IS_STG = env("ENV_TYPE") == "stg"
IS_DEV = env("ENV_TYPE") == "dev"
IS_LOCAL = env("ENV_TYPE") == "local"
CONFIG_ENV_TYPE = env("ENV_TYPE")
```

Lưu ý nhỏ: trong `source_code/.env_staging`, `ENV_TYPE` là `"staging"`, nhưng `settings.py` đang check `IS_STG = env("ENV_TYPE") == "stg"`. Nếu code nào dùng `IS_STG`, cần kiểm tra kỹ vì có khả năng không true ở staging. Nhưng nhiều chỗ khác trong project dùng `CONFIG_ENV_TYPE` nên vẫn đi theo giá trị `"staging"`.

## 9. Flow Staging Và Live

Staging/live không chạy bằng `docker-compose-local.yaml`.

Chúng dùng:

```text
gcp_builder/build_and_deploy.sh
```

Flow tổng quát:

```text
build_and_deploy.sh staging
        |
        | dùng Dockerfile.staging
        v
build Docker image
        |
        | push image lên Google Artifact Registry
        v
gcloud run deploy
        |
        v
Cloud Run service staging
```

Live tương tự:

```text
build_and_deploy.sh live
        |
        | dùng Dockerfile.live
        v
build Docker image
push image
deploy Cloud Run service live
```

## 10. Dockerfile Staging Và Live

File staging:

```text
gcp_builder/dockerfile/Dockerfile.staging
```

Điểm quan trọng:

```dockerfile
COPY source_code/ /wky_api/
COPY .env_staging /wky_api/.env
ENTRYPOINT ["bash", "/_setup/_init_staging.sh"]
```

Nghĩa là container staging có:

```text
/wky_api/.env
```

nhưng nội dung lấy từ:

```text
.env_staging
```

File live:

```text
gcp_builder/dockerfile/Dockerfile.live
```

Điểm quan trọng:

```dockerfile
COPY source_code/ /wky_api/
COPY .env_live /wky_api/.env
ENTRYPOINT ["bash", "/_setup/_init_live.sh"]
```

Nghĩa là container live có:

```text
/wky_api/.env
```

nhưng nội dung lấy từ:

```text
.env_live
```

## 11. Build Và Deploy Đọc Config Ở Đâu?

File:

```text
gcp_builder/build_and_deploy.sh
```

Khi deploy staging/live, script sẽ source config theo môi trường:

```sh
source const/gcp_variable.$environment.cfg
```

Nếu environment là `staging`, nó đọc:

```text
gcp_builder/const/gcp_variable.staging.cfg
```

Nếu environment là `live`, nó đọc:

```text
gcp_builder/const/gcp_variable.live.cfg
```

Trong các file này có config như:

```text
PROJECT_ID
REGION
SERVICE_NAME
IMAGE_URL
SERVICE_ACCOUNT
DOMAIN
```

Sau đó script chạy:

```sh
docker build ...
docker push ...
gcloud run deploy ...
```

Nói ngắn gọn:

```text
gcp_variable.*.cfg quyết định deploy lên project/service/domain nào.
Dockerfile.* quyết định image bên trong chứa code/env nào.
```

## 12. Docker Liên Quan Gì Đến Cloud Run?

Cloud Run chạy container.

Project này build Docker image trước, rồi đưa image đó lên Cloud Run.

Flow:

```text
Dockerfile
   -> docker build
   -> Docker image
   -> docker push
   -> Cloud Run deploy image
   -> Cloud Run chạy container
```

Vậy Docker không chỉ dùng ở local. Với staging/live, Docker là cách đóng gói app để Cloud Run chạy.

## 13. Docker Liên Quan Gì Đến Scheduler?

Scheduler không nằm trong Dockerfile chính của API.

Scheduler được deploy bằng:

```text
gcp_builder/deploy_scheduler.sh
```

Script này đọc config môi trường:

```sh
source const/gcp_variable.$environment.cfg
```

Sau đó chạy:

```sh
python scheduler/jobs.py
```

Trong `scheduler/jobs.py`, project tạo các job gọi API theo lịch.

Ví dụ job notify report status:

```text
POST {DOMAIN}/api/report/crontab-notify-report-status
```

Với staging, `DOMAIN` lấy từ:

```text
gcp_builder/const/gcp_variable.staging.cfg
```

Với live, `DOMAIN` lấy từ:

```text
gcp_builder/const/gcp_variable.live.cfg
```

Nghĩa là:

```text
Cloud Scheduler -> gọi URL API trên Cloud Run -> Django xử lý crontab view
```

## 14. Cách Đọc Một Dockerfile

Khi mở Dockerfile, đọc theo thứ tự này:

### FROM

Ví dụ:

```dockerfile
FROM python:3.12
```

Nghĩa là image bắt đầu từ Python 3.12.

### WORKDIR

Ví dụ:

```dockerfile
WORKDIR /wky_api
```

Nghĩa là các lệnh sau đó chạy trong thư mục `/wky_api`.

### COPY

Ví dụ:

```dockerfile
COPY source_code/ /wky_api/
COPY .env_staging /wky_api/.env
```

Nghĩa là copy code/env từ máy build vào image.

### RUN

Ví dụ:

```dockerfile
RUN pip install -r requirements.txt
```

Nghĩa là chạy lệnh lúc build image.

### EXPOSE

Ví dụ:

```dockerfile
EXPOSE 8080
```

Nghĩa là container dự kiến listen port 8080.

### ENTRYPOINT

Ví dụ:

```dockerfile
ENTRYPOINT ["bash", "/_setup/_init_staging.sh"]
```

Nghĩa là khi container start, nó chạy script này trước.

## 15. Cách Đọc docker-compose-local.yaml

Khi mở file compose, đọc theo thứ tự này:

### services

Mỗi service là một container hoặc một nhóm container cùng loại.

Project này có:

```text
mysql-server
api-server
```

### build

Cho biết service build từ Dockerfile nào.

Ví dụ api-server build từ:

```text
_build_local/_dockerfile/local/Dockerfile.workify_api_web.local
```

### ports

Ví dụ:

```text
19000:443
```

Nghĩa là:

```text
host port 19000 -> container port 443
```

### volumes

Ví dụ:

```text
${CURRENT_SOURCE_PATH}/source_code:/wky_api
```

Nghĩa là thư mục `source_code` trên máy bạn được gắn vào `/wky_api` trong container.

Nhờ vậy sửa code ở máy local thì container thấy code mới.

### depends_on

Ví dụ:

```yaml
depends_on:
  - mysql-server
```

Nghĩa là api-server phụ thuộc mysql-server.

Nhưng lưu ý: `depends_on` chỉ đảm bảo container MySQL được start trước, không chắc database đã sẵn sàng nhận kết nối.

## 16. Những Điểm Dễ Nhầm Trong Project Này

### 1. Django đọc `.env`, không đọc trực tiếp `.env_dev`

Trong `settings.py`, Django đọc:

```text
source_code/.env
```

Các file `.env_dev`, `.env_staging`, `.env_live` chỉ được copy thành `.env` trong quá trình build/deploy.

### 2. `localhost` trong container không phải máy bạn

Nếu Django container gọi:

```text
localhost:3306
```

nó đang gọi chính container Django, không phải MySQL container.

Vì vậy local dùng:

```text
DATABASE_HOST=wky_api_db
```

do `wky_api_db` là tên container MySQL.

### 3. Port bên trái và bên phải khác nhau

Trong compose:

```text
19000:443
```

Bên trái là port trên máy bạn.

Bên phải là port trong container.

Nên browser/Postman gọi:

```text
http://localhost:19000
```

không phải `http://localhost:443`.

### 4. Local Dockerfile copy `.env_dev`

Dockerfile local hiện có:

```text
COPY source_code/.env_dev /wky_api/.env
```

Điều này có nghĩa image local mặc định dùng env dev. Nhưng khi chạy compose có volume mount source code vào `/wky_api`, file `.env` trên máy local có thể override nội dung trong image.

Khi debug env local, nên kiểm tra trực tiếp:

```text
source_code/.env
```

### 5. Staging/live dùng Cloud SQL

Local/dev database host thường là:

```text
wky_api_db
```

Staging/live database host là Cloud SQL socket:

```text
/cloudsql/...
```

Vì staging/live chạy trên Google Cloud, không dùng MySQL container local.

## 17. Nên Bắt Đầu Debug Từ Đâu?

Nếu lỗi local không chạy:

1. Kiểm tra `docker-compose-local.yaml`.
2. Kiểm tra container `mysql-server` có chạy không.
3. Kiểm tra container `api-server` có chạy không.
4. Kiểm tra `source_code/.env`.
5. Kiểm tra `DATABASE_HOST`.
6. Kiểm tra port `19000:443`.
7. Kiểm tra log container API.

Nếu lỗi staging/live:

1. Kiểm tra `gcp_builder/build_and_deploy.sh`.
2. Kiểm tra `gcp_builder/const/gcp_variable.staging.cfg` hoặc `.live.cfg`.
3. Kiểm tra Dockerfile staging/live copy đúng env chưa.
4. Kiểm tra Cloud Run log.
5. Kiểm tra Cloud SQL connection.
6. Kiểm tra `ENV_TYPE`, `CURRENT_URL`, `CLIENT_URL`.

Nếu lỗi crontab/scheduler:

1. Kiểm tra `gcp_builder/deploy_scheduler.sh`.
2. Kiểm tra `gcp_builder/scheduler/jobs.py`.
3. Kiểm tra `DOMAIN` trong `gcp_variable.*.cfg`.
4. Kiểm tra endpoint Django có tồn tại không.
5. Kiểm tra Cloud Scheduler có gọi đúng method `POST` không.

## 18. Bản Đồ Flow Ngắn Gọn

Local:

```text
docker-compose-local.yaml
  -> build api-server từ Dockerfile local
  -> chạy mysql-server
  -> chạy api-server
  -> _init.sh runserver
  -> migrate
  -> Django runserver port 443 trong container
  -> máy bạn gọi localhost:19000
```

Staging:

```text
build_and_deploy.sh staging
  -> đọc gcp_variable.staging.cfg
  -> build bằng Dockerfile.staging
  -> copy .env_staging thành /wky_api/.env
  -> push image
  -> deploy Cloud Run staging
```

Live:

```text
build_and_deploy.sh live
  -> đọc gcp_variable.live.cfg
  -> build bằng Dockerfile.live
  -> copy .env_live thành /wky_api/.env
  -> push image
  -> deploy Cloud Run live
```

Scheduler:

```text
deploy_scheduler.sh staging/live
  -> đọc gcp_variable.*.cfg
  -> chạy scheduler/jobs.py
  -> tạo Cloud Scheduler job
  -> Cloud Scheduler gọi API trên DOMAIN
```

## 19. Glossary Nhanh

`Dockerfile`

File công thức để build image.

`Image`

Bản đóng gói app, dependencies, env file, entrypoint.

`Container`

Image đang được chạy.

`docker-compose`

Công cụ chạy nhiều container cùng lúc bằng một file YAML.

`Service`

Một service trong compose thường tương ứng với một loại container, ví dụ `api-server`, `mysql-server`.

`Volume`

Cách gắn thư mục/file từ máy host vào container.

`Port mapping`

Map port máy host vào port container, ví dụ `19000:443`.

`Cloud Run`

Dịch vụ Google Cloud dùng để chạy container.

`Cloud Scheduler`

Dịch vụ Google Cloud dùng để gọi endpoint theo lịch.

`ENTRYPOINT`

Lệnh/script chạy khi container start.

`ENV_TYPE`

Biến env cho biết app đang chạy ở môi trường nào: local/dev/staging/live.

## 20. Cách Nghĩ Đúng Khi Đọc Docker Trong Project Này

Đừng đọc Docker như một thứ riêng biệt. Hãy đọc theo câu hỏi:

```text
Môi trường nào?
Local hay staging/live?
File env nào được biến thành .env?
Container chạy command nào?
App connect database bằng host nào?
Port ngoài máy map vào port nào trong container?
Nếu deploy thì image được build bằng Dockerfile nào?
```

Nếu trả lời được các câu này, bạn đã nắm được phần quan trọng nhất của Docker trong project này.
