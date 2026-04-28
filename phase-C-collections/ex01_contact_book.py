import csv 
contacts = []

def add_contact():
    name = input("Nhap ten:")
    phone = input("Nhap SDT:")
    email = input("Nhap email:")

    new_person = {
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(new_person)
    print("Da them thanh cong")

def search_contact():
    keyword = input("Nhap ten can tim:")
    found = False
    for person in contacts:
        if keyword.lower() in person['name'].lower():
            print(f"Ten: {person['name']}, SDT: {person['phone']}, Email: {person['email']}")
            found = True
    if not found:
        print("Khong tim thay lien he nao")

def delete_contact():
    name_to_delete = input("Nhap ten can xoa:")
    
    for person in contacts:
        if person['name'].lower() == name_to_delete.lower():
            contacts.remove(person)
            print("Da xoa thanh cong")
            return
    
    print("Khong tim thay lien he nao")

def edit_contact():
    name_to_edit = input("Nhap ten can sua:")
    
    for person in contacts:
        if person['name'].lower() == name_to_edit.lower():
            print(f"Dang sua thong tin cua {person['name']}")
            new_phone = input("Nhap SDT moi:")
            new_email = input("Nhap email moi:")
            person['phone'] = new_phone
            person['email'] = new_email
            print("Da cap nhat thanh cong")
            return
    
    print("Khong tim thay lien he nao")

def show_contacts():
    print("DANH SACH DANH BA")
    if not contacts:
        print("Danh ba dang trong!")
        return
    
    for person in contacts:
        print(f"Ten: {person['name']}, SDT: {person['phone']}, Email: {person['email']}")

def save_to_file():
    with open('phase-C-collections/contact_book_modular/contacts.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['name', 'phone', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)
    print("Da luu danh ba vao file contacts.csv")

def load_from_file():
    try:
        with open('phase-C-collections/contact_book_modular/contacts.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
        print("Da nap du lieu tu file.")
    except FileNotFoundError:
        print("Chua co file du lieu, bat dau danh ba moi.")

def main():
    while True:
        
        print("""
--- MENU ---
1. Them lien he
2. Sua thong tin lien he
3. Hien thi danh ba
4. Tim kiem theo ten
5. Xoa lien he
6. Luu danh ba vao file
7. Thoat
        """)
        
        choice = input("Nhap lua chon cua ban: ")
        
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
            print("Thoat...")
            break
        else:
            print("Lua chon khong hop le!")
load_from_file()
main()


