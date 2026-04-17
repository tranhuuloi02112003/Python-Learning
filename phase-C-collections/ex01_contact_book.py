import csv 
contacts = []

def add_contact():
    name = input("Nhập tên:")
    phone = input("Nhập SDT:")
    email = input("Nhập email:")

    new_person = {
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(new_person)
    print("Đã thêm thành công")

def search_contact():
    keyword = input("Nhập tên cần tìm:")
    found = False
    for person in contacts:
        if keyword.lower() in person['name'].lower():
            print(f"Tên: {person['name']}, SDT: {person['phone']}, Email: {person['email']}")
            found = True
    if not found:
        print("Không tìm thấy liên hệ nào")

def delete_contact():
    name_to_delete = input("Nhập tên cần xóa:")
    
    for person in contacts:
        if person['name'].lower() == name_to_delete.lower():
            contacts.remove(person)
            print("Đã xóa thành công")
            return
    
    print("Không tìm thấy liên hệ nào")

def edit_contact():
    name_to_edit = input("Nhập tên cần sửa:")
    
    for person in contacts:
        if person['name'].lower() == name_to_edit.lower():
            print(f"Đang sửa thông tin của {person['name']}")
            new_phone = input("Nhập SDT mới:")
            new_email = input("Nhập email mới:")
            person['phone'] = new_phone
            person['email'] = new_email
            print("Đã cập nhật thành công")
            return
    
    print("Không tìm thấy liên hệ nào")

def show_contacts():
    print("DANH SÁCH DANH BẠ")
    if not contacts:
        print("Danh bạ đang trống!")
        return
    
    for person in contacts:
        print(f"Tên: {person['name']}, SDT: {person['phone']}, Email: {person['email']}")

def save_to_file():
    with open('phase-C-collections/contact_book_modular/contacts.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['name', 'phone', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)
    print("Đã lưu danh bạ vào file contacts.csv")

def load_from_file():
    try:
        with open('phase-C-collections/contact_book_modular/contacts.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
        print("Đã nạp dữ liệu từ file.")
    except FileNotFoundError:
        print("Chưa có file dữ liệu, bắt đầu danh bạ mới.")

def main():
    while True:
        
        print("""
--- MENU ---
1. Thêm liên hệ
2. Sửa thông tin liên hệ
3. Hiển thị danh bạ
4. Tìm kiếm theo tên
5. Xóa liên hệ
6. Lưu danh bạ vào file
7. Thoát
        """)
        
        choice = input("Nhập lựa chọn của bạn: ")
        
        if choice == "1":
            add_contact()
        elif choice == "2":
            edit_contact()
        elif choice == "3":
            show_contacts()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            save_to_file()
        elif choice == "7":
            print("Thoát...")
            break
        else:
            print("Lựa chọn không hợp lệ!")
load_from_file()
main()


