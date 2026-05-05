import contacts_manager as manager

def main():
    manager.load_from_file()
    
    while True:
        print("""
--- QUAN LY DANH BA (Modular) ---
1. Them lien he
2. Sua thong tin lien he
3. Hien thi danh ba
4. Tim kiem theo ten
5. Xoa lien he
6. Luu danh ba vao file
7. Thoat
        """)
        
        choice = input("Lua chon cua ban: ")
        
        if choice == "1":
            name = input("Nhap ten:")
            phone = input("Nhap SDT:")
            email = input("Nhap email:")
            manager.add_contact(name, phone, email)
            print("Da them thanh cong")
            
        elif choice == "2":
            name = input("Nhap ten can sua:")
            phone = input("Nhap SDT moi:")
            email = input("Nhap email moi:")
            if manager.update_contact(name, phone, email):
                print("Da cap nhat thanh cong")
            else:
                print("Khong tim thay lien he")
                
        elif choice == "3":
            print("DANH SACH DANH BA")
            if not manager.contacts:
                print("Danh ba dang trong!")
            for p in manager.contacts:
                print(f"Ten: {p['name']}, SDT: {p['phone']}, Email: {p['email']}")
                
        elif choice == "4":
            keyword = input("Nhap ten can tim:")
            results = manager.search_contacts(keyword)
            if results:
                for r in results:
                    print(f"Ten: {r['name']}, SDT: {r['phone']}, Email: {r['email']}")
            else:
                print("Khong tim thay lien he nao")
                
        elif choice == "5":
            name = input("Nhap ten can xoa:")
            if manager.delete_contact(name):
                print("Da xoa thanh cong")
            else:
                print("Khong tim thay lien he nao")

        elif choice == "6":
            manager.save_to_file()
            print("Da luu danh ba vao file contacts.csv")

        elif choice == "7":
            manager.save_to_file()
            print("Thoat...")
            break

# Kiểm tra nếu file được chạy trực tiếp thì mới thực thi hàm main()
if __name__ == "__main__":
    main()
