# Unit Converter - Chuyển đổi đơn vị

print("=== Unit Converter ===\n")

# Menu lựa chọn
print("Chọn loại chuyển đổi:")
print("1. Kilometer ↔ Mile")
print("2. VND → USD")
print()

choice = input("Lựa chọn của bạn (1/2): ")

if choice == '1':
    km = float(input("Nhập số km: "))
    mile = km * 0.621371
    print(f"{km} km = {mile:.2f} miles")
elif choice == '2':
    vnd = float(input("Nhập số VND: "))
    usd = vnd / 23000
    print(f"{vnd:,.0f} VND = {usd:.2f} USD")
# Giải thích:
# - if/elif/else: cấu trúc rẻ nhánh điều kiện
# - float(): ép sang số thập phân
# - :.2f: format số thành 2 chữ số thập phân
# - :,.0f: format số với dấu phân cách hàng ngàn
