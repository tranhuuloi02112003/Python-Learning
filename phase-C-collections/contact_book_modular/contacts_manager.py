import csv

contacts = []

def add_contact(name, phone, email):
    new_person = {"name": name, "phone": phone, "email": email}
    contacts.append(new_person)

def search_contacts(keyword):
    # Dùng List Comprehension để lọc dữ liệu
    return [p for p in contacts if keyword.lower() in p['name'].lower()]

def delete_contact(name):
    for person in contacts:
        if person['name'].lower() == name.lower():
            contacts.remove(person)
            return True
    return False

def update_contact(name_to_find, new_phone, new_email):
    for person in contacts:
        if person['name'].lower() == name_to_find.lower():
            person['phone'] = new_phone
            person['email'] = new_email
            return True
    return False

def save_to_file():
    with open('phase-C-collections/contact_book_modular/contacts.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['name', 'phone', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)

def load_from_file():
    try:
        with open('phase-C-collections/contact_book_modular/contacts.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
        print("Đã nạp dữ liệu từ file.")
    except FileNotFoundError:
        print("Chưa có file dữ liệu, bắt đầu danh bạ mới.")
