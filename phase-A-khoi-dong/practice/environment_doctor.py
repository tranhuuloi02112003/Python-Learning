# Environment Doctor - Kiểm tra môi trường Python

import sys
import os
import platform


print(" Thong tin he thong")
print(f"OS: {platform.system()} {platform.release()}")
print(f"Processor: {platform.machine()}")

# Thông tin Python
print("\n Thong tin python")
print(f"Version: {sys.version}")
print(f"Executable: {sys.executable}")
print(f"Python Path: {sys.prefix}")

# Các thư viện đã cài
print("\n📦 Cac thu vien da cai")
installed_modules = sys.modules.keys()
# Chỉ hiển thị những thư viện phổ biến
common_libs = ['requests', 'django', 'flask', 'numpy', 'pandas', 'urllib3', 'certifi']

# Cách khác: found_libs = [lib for lib in common_libs if lib in installed_modules]
found_libs = []
for lib in common_libs:
    if lib in installed_modules:
        found_libs.append(lib)

if found_libs:
    print("✓ Thu vien pho bien da cai:")
    for lib in found_libs:
        print(f"  - {lib}")
else:
    print("(Khong tim thay thu vien pho bien nao)")

# Kiểm tra venv
print("\n🎯 Moi truong ao (VENV)")
venv_path = os.environ.get('VIRTUAL_ENV')
if venv_path:
    print(f"✓ Venv dang hoat dong: {venv_path}")
else:
    print("✗ Venv chua duoc kich hoat")

print("\n" + "="*50)
print("Kiểm tra hoàn tất!\n")

# Giải thích:
# - import sys: module hệ thống của Python
# - import platform: module kiểm tra thông tin máy
# - sys.version: phiên bản Python đang dùng
# - sys.executable: đường dẫn Python interpreter
# - sys.modules: các module đã được import
# - os.environ.get(): đọc biến môi trường
