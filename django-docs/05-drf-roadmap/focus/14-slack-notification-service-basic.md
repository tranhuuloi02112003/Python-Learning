# Slack Notification Service Cơ Bản Trong Django

Bài này tổng hợp kiến thức cơ bản để đọc hiểu một file Slack service trong project Django/DRF thực tế.

Mục tiêu không phải học sâu toàn bộ Slack API, mà là hiểu:

```text
Django backend
-> slack_sdk WebClient
-> Slack Web API
-> Slack Bot gửi message
```

---

## 1. Project Dùng Gì Để Gửi Slack?

Trong file `slack_service.py`, project dùng:

```python
from slack_sdk import WebClient
```

Thư viện chính là:

```text
slack_sdk
```

Class chính là:

```text
WebClient
```

Hiểu đơn giản:

```text
WebClient = object giúp Python gọi Slack Web API.
```

Thay vì tự gọi HTTP thủ công:

```python
requests.post("https://slack.com/api/chat.postMessage", ...)
```

ta dùng:

```python
client.chat_postMessage(...)
```

`slack_sdk` sẽ lo phần gọi API, auth, parse response.

---

## 2. WebClient Cần Gì Để Chạy?

`WebClient` cần Slack Bot Token.

Ví dụ:

```python
self._client = WebClient(
    token=_cred.get("SLACK_BOT_TOKEN"),
)
```

Token quan trọng là:

```text
SLACK_BOT_TOKEN
```

Hiểu đơn giản:

```text
SLACK_BOT_TOKEN = chìa khóa để backend gọi Slack API với quyền của bot.
```

Lưu ý:

```text
Không paste token ra report, log, code review, tài liệu public.
```

Token là secret.

---

## 3. Các Slack API Đang Dùng

Trong service, `WebClient` thường gọi các API chính sau:

| API | Dùng để làm gì |
|:----|:---------------|
| `auth_test()` | Kiểm tra token có hợp lệ không |
| `chat_postMessage(...)` | Gửi message vào channel hoặc DM |
| `conversations_open(users=user_id)` | Mở DM với một Slack user |
| `users_list(...)` | Lấy danh sách Slack users |
| `conversations_list(...)` | Lấy danh sách Slack channels |

Flow cơ bản:

```text
Bot Token
-> WebClient
-> Slack API
-> Slack Message
```

---

## 4. Các Import Quan Trọng

Đầu file có thể có:

```python
import json
import os
import re
from datetime import datetime
```

Dùng để build message, xử lý text, xử lý thời gian.

Có thể có:

```python
import requests
```

Dùng cho vài case gọi HTTP trực tiếp, ví dụ upload file.

Có thể có:

```python
from django.conf import settings
```

Dùng để lấy config Django, ví dụ env hoặc client URL.

Quan trọng nhất:

```python
from slack_sdk import WebClient
```

Dùng để gọi Slack Web API.

Ví dụ credential:

```python
from __LP_Library.Slack_Api._credentials import SLACK_BOT_CRED
```

`SLACK_BOT_CRED` là nơi map token theo môi trường hoặc theo bot.

---

## 5. Helper `get_slack_user`

Ví dụ:

```python
def get_slack_user(employee):
```

Hàm này dùng để convert `employee` thành text mention Slack.

Nếu employee có:

```python
employee.slack_user_id
```

thì trả về dạng:

```text
<@Uxxxx>
```

Slack sẽ render thành mention user thật.

Nếu không có `slack_user_id`, hàm có thể fallback sang:

```text
@firstnamelastname
```

hoặc:

```text
@email_prefix
```

Lưu ý:

```text
get_slack_user chỉ phục vụ hiển thị mention trong message.
Nó không phải hàm gửi Slack.
```

---

## 6. `SlackBaseService` Là Gì?

Ví dụ:

```python
class SlackBaseService(object):
```

Đây là class nền để gom các phần chung khi làm việc với Slack.

Nó thường chứa:

- Slack client
- logic chọn token
- logic chọn channel theo env
- hàm gửi message cơ bản
- hàm lấy users/channels từ Slack

Ví dụ các biến channel:

```text
TEST_CHANNEL_ID
CHANNEL_ID_DATA
CHANNEL_ID_MTG_DATA
CHANNEL_ID_BPO_TASK
BPO_PROJECT_SLACK_CHANNEL_STAGING
BPO_PROJECT_SLACK_CHANNEL_PROD
CHANNEL_ID_LOCK_OPERATION
```

Các biến này thường là mapping channel theo môi trường hoặc theo tính năng.

Ví dụ:

```python
CHANNEL_ID_DATA = {
    "local": TEST_CHANNEL_ID,
    "dev": TEST_CHANNEL_ID,
    "staging": TEST_CHANNEL_ID,
    "production": "C..."
}
```

Ý nghĩa:

```text
local/dev/staging -> gửi vào test channel
production        -> gửi vào channel thật
```

---

## 7. Constructor `__init__`

Ví dụ:

```python
def __init__(self, current_env="local", bot_key=None):
    self._client = self.__get_client(current_env, bot_key)
    self.current_env = current_env
    self.bot_key = bot_key
    self.current_time = ...
    self._base_channel_id = self._get_channel_id(current_env)
```

Khi tạo object:

```python
SlackNotifyService(settings.CONFIG_ENV_TYPE, "bpo_task_notification")
```

nó thường làm các việc:

1. Lấy Slack client bằng `__get_client`.
2. Lưu `current_env`.
3. Lưu `bot_key`.
4. Tạo `current_time` để gắn vào message.
5. Lấy channel mặc định theo env.

---

## 8. Hàm `__get_client`

Hàm này dùng để chọn bot/token.

Logic thường gặp:

```python
def __get_client(self, current_env, bot_key=None):
    if bot_key and bot_key in SLACK_BOT_CRED:
        _cred = SLACK_BOT_CRED.get(bot_key)
    else:
        _cred = SLACK_BOT_CRED.get(current_env)

    self._client = WebClient(
        token=_cred.get("SLACK_BOT_TOKEN"),
    )
    self._client.auth_test()
```

Dịch ra:

```text
Nếu có bot_key hợp lệ -> dùng bot riêng.
Nếu không có bot_key -> dùng bot theo môi trường.
```

Sau đó:

```text
Tạo WebClient bằng SLACK_BOT_TOKEN.
Gọi auth_test để kiểm tra token.
```

---

## 9. Gửi Message Vào Channel

Ví dụ:

```python
def send_message_to_channel(
    self,
    channel_id=None,
    message_title="",
    message_content: list = []
):
```

Nếu không truyền `channel_id`, service tự lấy channel mặc định theo env:

```python
channel_id = self._get_channel_id(self.current_env)
```

Sau đó gọi:

```python
self._chat_post_message(
    channel=channel_id,
    attachments=...,
    blocks=...,
    text=self.__get_msg_with_prefix(message_title),
)
```

Ý nghĩa:

```text
send_message_to_channel
-> _chat_post_message
-> WebClient.chat_postMessage
-> Slack API
```

---

## 10. Hàm Gửi Thấp Nhất `_chat_post_message`

Ví dụ:

```python
def _chat_post_message(self, **kwargs):
    return self._client.chat_postMessage(**kwargs)
```

Đây là wrapper thấp nhất để gửi message.

Nói ngắn gọn:

```text
Muốn biết message có thật sự gửi ra Slack không,
hãy lần về _chat_post_message hoặc chat_postMessage.
```

---

## 11. Gửi DM Tới User

Ví dụ:

```python
def send_message_to_user(
    self,
    user_id,
    message_title="",
    message_content: list = []
):
```

Flow gửi DM:

```python
response = self._client.conversations_open(users=user_id)
dm_channel_id = response["channel"]["id"]

response = self._chat_post_message(
    channel=dm_channel_id,
    blocks=message_content,
)
```

Dịch ra:

1. Nhận Slack user id, ví dụ `U09RN80CETV`.
2. Gọi Slack API mở DM với user đó.
3. Slack trả về DM channel id, ví dụ `Dxxxx`.
4. Gửi message vào DM channel đó.

Lưu ý:

```text
Gửi DM cần Slack user_id.
Không gửi trực tiếp bằng email hoặc username.
```

---

## 12. Lấy Danh Sách Slack Users

Ví dụ:

```python
def get_all_users(self):
```

Hàm này dùng Slack API:

```python
self._client.users_list(...)
```

Sau đó build dict theo email:

```python
users_dict[email] = {
    "id": user_id,
    "real_name": real_name,
    "display_name": display_name,
    "email": email,
    "image": image,
}
```

Hàm này thường dùng để:

```text
sync Slack user id về employee trong hệ thống.
```

---

## 13. Lấy Danh Sách Slack Channels

Ví dụ:

```python
def get_all_channels(self):
```

Hàm này dùng Slack API:

```python
self._client.conversations_list(...)
```

Kết quả thường được map về:

```python
{
    "channel_name": "channel_id"
}
```

Hàm này giúp biết:

```text
Tên channel nào tương ứng với channel id nào.
```

---

## 14. `SlackNotifyService` Là Gì?

Ví dụ:

```python
class SlackNotifyService(SlackBaseService):
```

Class này kế thừa `SlackBaseService`.

Nó không tự tạo lại Slack client từ đầu, mà gọi:

```python
super().__init__(current_env, bot_key)
```

Tức là dùng lại:

- logic chọn token
- logic tạo `WebClient`
- logic chọn channel
- các hàm gửi message cơ bản

Phần còn lại của `SlackNotifyService` là các hàm nghiệp vụ.

Ví dụ:

```text
send_request_need_approve
send_request_notify
send_check_in
send_check_out
send_logwork_warning_to_members
send_comment_alert
send_notify_block_to_supporter
send_bpo_task_assigned_message
notify_new_bpo_task
alert_bpo_man_month
```

Mỗi hàm nghiệp vụ thường làm 3 bước:

```text
1. Lấy data nghiệp vụ
2. Build Slack blocks/text
3. Gọi send_message_to_user, send_message_to_channel hoặc _chat_post_message
```

---

## 15. Message Content Và Slack Blocks

Slack message có thể là text thường hoặc blocks.

Project thường dùng Slack Block Kit:

```python
blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Nội dung message"
        }
    }
]
```

Hiểu đơn giản:

```text
blocks = format layout message của Slack
mrkdwn = markdown của Slack
```

Một số cú pháp hay gặp:

| Cú pháp | Ý nghĩa |
|:--------|:--------|
| `<link|title>` | Hyperlink |
| `<@Uxxxx>` | Mention user |
| `*text*` | Bold |

Ví dụ:

```python
text = f"Manager đã assign task <{link}|{title}> cho <@{slack_user_id}>"
```

Slack sẽ render thành:

```text
Manager đã assign task title cho @user
```

---

## 16. Flow Gửi DM Hoàn Chỉnh

Ví dụ code:

```python
SlackNotifyService(
    settings.CONFIG_ENV_TYPE,
    "bpo_task_notification"
).send_message_to_user(
    employee.slack_user_id,
    "Title",
    blocks
)
```

Flow trong code:

```text
SlackNotifyService
-> SlackBaseService.__init__
   -> __get_client
      -> WebClient(token=SLACK_BOT_TOKEN)
      -> auth_test
-> send_message_to_user
   -> conversations_open(users=user_id)
   -> _chat_post_message
      -> chat_postMessage(channel=dm_channel_id, blocks=blocks)
```

Flow thực tế:

```text
BE Django
-> slack_sdk WebClient
-> Slack Web API
-> Slack Bot gửi message
-> User nhận DM
```

---

## 17. Để Slack Notify Hoạt Động Cần Gì?

Cần đủ các phần sau:

1. Có Slack App/Bot trong workspace.
2. Có `SLACK_BOT_TOKEN` đúng.
3. Token được config trong `SLACK_BOT_CRED`.
4. Code chọn đúng bot qua `current_env` hoặc `bot_key`.
5. Bot có quyền gửi message.
6. Nếu gửi DM: employee có `slack_user_id` đúng.
7. Nếu gửi channel: `channel_id` đúng.
8. Nếu gửi channel: bot đã được add vào channel nếu channel yêu cầu.
9. Server gọi được internet tới Slack API.
10. Message `blocks` đúng format.
11. Code nghiệp vụ thật sự gọi hàm gửi.

---

## 18. Checklist Debug Khi Không Gửi Được Slack

## 18.1. Token Có Đúng Không?

Kiểm tra:

```python
self._client.auth_test()
```

Nếu token sai hoặc hết quyền, thường lỗi sẽ xuất hiện ở bước này.

---

## 18.2. Đúng Bot Chưa?

Kiểm tra:

```python
SlackNotifyService(settings.CONFIG_ENV_TYPE, "bpo_task_notification")
```

Cần biết:

```text
current_env là gì?
bot_key là gì?
bot_key có tồn tại trong SLACK_BOT_CRED không?
```

---

## 18.3. Gửi DM Hay Channel?

Gửi DM:

```text
cần Slack user_id dạng Uxxxx
phải gọi conversations_open trước
```

Gửi channel:

```text
cần channel_id dạng Cxxxx hoặc Gxxxx
bot phải có quyền gửi vào channel
```

---

## 18.4. Message Có Đúng Format Không?

Nếu dùng blocks, kiểm tra:

```python
blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "..."
        }
    }
]
```

Sai format blocks có thể làm Slack API trả lỗi.

---

## 18.5. Code Có Chạy Tới Hàm Gửi Không?

Đặt log/print ở các tầng:

```python
print("before SlackNotifyService")
print("before send_message_to_user")
print("before _chat_post_message")
```

Nếu không tới `_chat_post_message`, lỗi nằm ở flow nghiệp vụ trước đó.

---

## 19. Dry-run Slack Notify

Khi muốn debug flow gửi Slack nhưng không muốn gửi Slack thật, có thể mock hàm gửi thấp nhất.

Ví dụ:

```python
from unittest.mock import patch


def fake_chat_post_message(*args, **kwargs):
    print("SLACK WOULD BE SENT")
    print("args:", args)
    print("kwargs:", kwargs)


with patch(
    "path.to.slack_service.SlackBaseService._chat_post_message",
    fake_chat_post_message
):
    run_business_flow()
```

Nếu flow có thay đổi DB, kết hợp thêm transaction rollback:

```python
from django.db import transaction

with transaction.atomic():
    run_business_flow()
    transaction.set_rollback(True)
```

Nhớ:

```text
Patch đúng import path nơi code đang dùng.
```

---

## 20. Nhớ Ngắn Gọn

File Slack service thường có cấu trúc:

```text
Import thư viện
-> Helper get_slack_user
-> SlackBaseService
   -> chọn token
   -> tạo WebClient
   -> gửi channel
   -> gửi DM
   -> lấy users/channels
-> SlackNotifyService
   -> các hàm notification nghiệp vụ
```

Các keyword cần nhớ:

| Keyword | Ý nghĩa |
|:--------|:--------|
| `slack_sdk` | Thư viện Python để gọi Slack |
| `WebClient` | Client gọi Slack Web API |
| `SLACK_BOT_TOKEN` | Token của Slack Bot |
| `SLACK_BOT_CRED` | Nơi map token theo env/bot |
| `auth_test` | Kiểm tra token |
| `chat_postMessage` | Gửi message thật |
| `conversations_open` | Mở DM với user |
| `users_list` | Lấy danh sách users |
| `conversations_list` | Lấy danh sách channels |
| `blocks` | Layout message Slack |
| `mrkdwn` | Markdown format của Slack |

Tóm tắt một câu:

```text
Django gọi SlackNotifyService,
SlackNotifyService dùng SlackBaseService,
SlackBaseService dùng WebClient,
WebClient gọi Slack API bằng SLACK_BOT_TOKEN.
```
