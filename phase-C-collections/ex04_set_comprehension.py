raw_emails = [" anth@gmail.com", "ANTH@gmail.com ", "test@Gmail.com", "anth@gmail.com"]

cleaned_emails = [email.strip().lower() for email in raw_emails]

unique_emails = set(cleaned_emails)

print(f"Danh sach sach: {unique_emails}")


# Trong Python, Tuple thuong dung de luu cac "He so" hoac "Cau hinh" ma ban khong muon code cua minh vo tinh sua doi.
# Vi du: Luu toa do GPS hoac cac hang so cau hinh App.
APP_CONFIG = ("Dark Mode", "Vietnam", "v1.0.2")