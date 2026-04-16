

tasks = []
def add_task():
    task = input("Nhập công việc: ")
    if task.strip(): # Kiểm tra nếu không bị trống
        tasks.append(task)
        print("Đã thêm công việc.")
    else:
        print("Công việc không được để trống!")

def show_task():
    print("\n--- DANH SÁCH CÔNG VIỆC ---")
    if not tasks:
        print("Danh sách công việc trống.")
        return
    
    # Dùng enumerate để in số thứ tự từ 1
    #for index, task in enumerate(tasks, start=1):
    #   print(f"{index}. {task}")

    for task in tasks:
        print(task)
    
def delete_task():
    if not tasks:
        print("Không có task nào để xoá.")
        return;
        
    show_task()
   
    try: 
        index = int(input("Nhập số thứ tự công việc cần xóa: "))
        if 1<=index<=len(tasks):
            removed = tasks.pop(index - 1)
            print(f"Đã xóa công việc: {removed}")
        else:
            print("Số thứ tự không tồn tại!")
    except ValueError:
        print("Vui lòng nhập số!")

while True:
    print("""======
Menu quản lý công việc
1. Thêm công việc
2. Hiển thị công việc
3. Xóa công việc
4. Thoát
""")
    try:
        choice = int(input("Nhập lựa chọn của bạn: "))
        
        if choice == 1:
            add_task()
        elif choice == 2:
            show_task()
        elif choice == 3:
            delete_task()
        elif choice == 4:
            print("Bạn đã chọn thoát")
            break
        else:
            print("Lựa chọn không hợp lệ")
    except ValueError:
        print("Vui lòng nhập số!")
