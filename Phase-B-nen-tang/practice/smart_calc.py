history = []
def add(a, b):
    res = a + b
    history.append(f"{a} + {b} = {res}")
    return res

def subtract(a, b):
    res = a - b
    history.append(f"{a} - {b} = {res}")
    return res

def multiply(a, b):
    res = a * b
    history.append(f"{a} * {b} = {res}")
    return res

def divide(a, b):
    if b == 0:
        return "Lỗi: Không thể chia cho 0!"
    res = a / b
    history.append(f"{a} / {b} = {res}")
    return res

def show_history():
    print("\n--- LỊCH SỬ TÍNH TOÁN ---")
    if not history:
        print("Trống.")
    else:
        for item in history:
            print(item)
    print("------------------------")


def main_calculator():
    while True:
        try:
            print("\n--- MÁY TÍNH ---")
            print("1. Thực hiện phép tính")
            print("2. Xem lịch sử")
            print("3. Thoát")
            
            choice = input("Chọn menu: ")
            
            if choice == '1':
                try:
                    n1 = float(input("Nhập số thứ nhất: "))
                    n2 = float(input("Nhập số thứ hai: "))
                    op = input("Chọn phép tính (+, -, *, /): ")
                    
                    if op == '+': print("Kết quả:", add(n1, n2))
                    elif op == '-': print("Kết quả:", subtract(n1, n2))
                    elif op == '*': print("Kết quả:", multiply(n1, n2))
                    elif op == '/': print("Kết quả:", divide(n1, n2))
                    else: print("Phép tính không hợp lệ!")
                except ValueError:
                    print("Lỗi: Vui lòng nhập số!")
                    
            elif choice == '2':
                show_history()
            elif choice == '3':
                print("Tạm biệt!")
                break
            else:
                print("Lựa chọn không hợp lệ.")
        except ValueError:
            print("Vui lòng nhập số!")
            
main_calculator()