import random

questions = [
    {
        "question": "Thu do cua Viet Nam la gi?",
        "options": ["A. TP.HCM", "B. Ha Noi", "C. Da Nang", "D. Can Tho"],
        "answer": "B"
    },
    {
        "question": "Ai la nguoi da phat minh ra bong den?",
        "options": ["A. Albert Einstein", "B. Isaac Newton", "C. Thomas Edison", "D. Nikola Tesla"],
        "answer": "C"
    },
    {
        "question": "Thanh pho nao duoc menh danh la 'Thanh pho khong ngu'?",
        "options": ["A. New York", "B. Paris", "C. Tokyo", "D. Las Vegas"],
        "answer": "A"
    }
]

random.shuffle(questions)
score = 0
total = len(questions)

print("--- CHAO MUNG BAN DEN VOI TRO CHOI TRAC NGHIEM ---")

for i, item in enumerate(questions, start=1):
    print(f"\nCau {i}: {item['question']}")

    for option in item['options']:
        print(option)

    user_answer = input("Nhap cau tra loi cua ban (A/B/C/D): ").strip().upper()

    if user_answer == item['answer']:
        score += 1
        print("Dung!")
    else:
        print(f"Sai roi! Dap an dung la: {item['answer']}")

print("\n" + "="*30)
print(f"TRO CHOI KET THUC!")
print(f"Ket qua cua ban: {score}/{total} cau dung.")

percentage = (score / total) * 100
if percentage == 100:
    print("Xep loai: Xuat sac!")
elif percentage >= 50:
    print("Xep loai: Kha tot!")
else:
    print("Xep loai: Can co gang them!")