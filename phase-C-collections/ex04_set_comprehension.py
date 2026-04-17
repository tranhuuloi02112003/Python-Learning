raw_emails = [" anth@gmail.com", "ANTH@gmail.com ", "test@Gmail.com", "anth@gmail.com"]

cleaned_emails = [email.strip().lower() for email in raw_emails]

unique_emails = set(cleaned_emails)

print(f"Danh sách sạch: {unique_emails}")


# Trong Python, Tuple thường dùng để lưu các "Hệ số" hoặc "Cấu hình" mà bạn không muốn code của mình vô tình sửa đổi.
# Ví dụ: Lưu tọa độ GPS hoặc các hằng số cấu hình App.
APP_CONFIG = ("Dark Mode", "Vietnam", "v1.0.2")