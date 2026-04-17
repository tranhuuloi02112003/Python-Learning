import random

questions = [
    {
        "question": "Thủ đô của Việt Nam là gì?",
        "options": ["A. TP.HCM", "B. Hà Nội", "C. Đà Nẵng", "D. Cần Thơ"],
        "answer": "B"
    },
    {
        "question": "Ai là người đã phát minh ra bóng đèn?",
        "options": ["A. Albert Einstein", "B. Isaac Newton", "C. Thomas Edison", "D. Nikola Tesla"],
        "answer": "C"
    },
    {
        "question": "Thành phố nào được mệnh danh là 'Thành phố không ngủ'?",
        "options": ["A. New York", "B. Paris", "C. Tokyo", "D. Las Vegas"],
        "answer": "A"
    }
]

random.shuffle(questions)
score = 0
total = len(questions)

print("--- CHÀO MỪNG BẠN ĐẾN VỚI TRÒ CHƠI TRẮC NGHIỆM ---")

for i, item in enumerate(questions, start=1):
    print(f"\nCâu {i}: {item['question']}")

    for option in item['options']:
        print(option)

    user_answer = input("Nhập câu trả lời của bạn (A/B/C/D): ").strip().upper()

    if user_answer == item['answer']:
        score += 1
        print("Đúng!")
    else:
        print(f"Sai rồi! Đáp án đúng là: {item['answer']}")

print("\n" + "="*30)
print(f"TRÒ CHƠI KẾT THÚC!")
print(f"Kết quả của bạn: {score}/{total} câu đúng.")

percentage = (score / total) * 100
if percentage == 100:
    print("Xếp loại: Xuất sắc!")
elif percentage >= 50:
    print("Xếp loại: Khá tốt!")
else:
    print("Xếp loại: Cần cố gắng thêm!")