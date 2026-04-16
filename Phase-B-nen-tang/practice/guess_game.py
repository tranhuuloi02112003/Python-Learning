import random

def get_hint(guess, target):
    """Hàm so sánh số đoán và mục tiêu, trả về gợi ý"""
    if guess == target:
        return "correct"
    elif guess < target:
        return "Số của bạn nhỏ hơn số cần đoán"
    else:
        return "Số của bạn lớn hơn số cần đoán"


def play_game():
    target_number = random.randint(1, 20)
    max_attempts = 7
    print("=== Game đoán số ===")
    
    for attempt in range(1, max_attempts + 1):
        remaining = max_attempts - attempt + 1
        print(f"\nLượt thứ {attempt} (Còn {remaining} lượt)")
        
        try:
            guess = int(input("Hãy đoán số từ 1 đến 20: "))
        except ValueError:
            print("Vui lòng chỉ nhập số nguyên!")
            continue
        result = get_hint(guess, target_number)
        
        if result == "correct":
            print(f"Chúc mừng! Bạn đã đoán đúng số {target_number} ở lượt thứ {attempt}!")
            return
        else:
            print(result)
            
    print(f"\nRất tiếc, bạn đã hết lượt. Số đúng là: {target_number}")

play_game()
