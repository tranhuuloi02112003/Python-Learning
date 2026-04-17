import contacts_manager as manager

def main():
    manager.load_from_file()
    
    while True:
        print("""
--- QUẢN LÝ DANH BẠ (Modular) ---
1. Thêm liên hệ
2. Sửa thông tin liên hệ
3. Hiển thị danh bạ
4. Tìm kiếm theo tên
5. Xóa liên hệ
6. Lưu danh bạ vào file
7. Thoát
        """)
        
        choice = input("Lựa chọn của bạn: ")
        
        if choice == "1":
            name = input("Nhập tên:")
            phone = input("Nhập SDT:")
            email = input("Nhập email:")
            manager.add_contact(name, phone, email)
            print("Đã thêm thành công")
            
        elif choice == "2":
            name = input("Nhập tên cần sửa:")
            phone = input("Nhập SDT mới:")
            email = input("Nhập email mới:")
            if manager.update_contact(name, phone, email):
                print("Đã cập nhật thành công")
            else:
                print("Không tìm thấy liên hệ")
                
        elif choice == "3":
            print("DANH SÁCH DANH BẠ")
            if not manager.contacts:
                print("Danh bạ đang trống!")
            for p in manager.contacts:
                print(f"Tên: {p['name']}, SDT: {p['phone']}, Email: {p['email']}")
                
        elif choice == "4":
            keyword = input("Nhập tên cần tìm:")
            results = manager.search_contacts(keyword)
            if results:
                for r in results:
                    print(f"Tên: {r['name']}, SDT: {r['phone']}, Email: {r['email']}")
            else:
                print("Không tìm thấy liên hệ nào")
                
        elif choice == "5":
            name = input("Nhập tên cần xóa:")
            if manager.delete_contact(name):
                print("Đã xóa thành công")
            else:
                print("Không tìm thấy liên hệ nào")

        elif choice == "6":
            manager.save_to_file()
            print("Đã lưu danh bạ vào file contacts.csv")

        elif choice == "7":
            manager.save_to_file()
            print("Thoát...")
            break

# Kiểm tra nếu file được chạy trực tiếp thì mới thực thi hàm main()
if __name__ == "__main__":
    main()
