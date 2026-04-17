import utils

def analyze_text(file_path):
    total_lines = 0
    total_chars = 0
    word_count = {} # Dictionary để đếm từ

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                total_lines += 1
                total_chars += len(line)

                clean_line = utils.clear_text(line)
                words = clean_line.split()

                for word in words:
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1

        utils.print_header("Báo Cáo Phân Tích")
        print(f"Tổng số dòng: {total_lines}")
        print(f"Tổng số ký tự: {total_chars}")

        print("Top 5 từ xuất hiện nhiều nhất:")
        sorted_word = sorted(word_count.items(), key = lambda word: word[1], reverse=True)

        for word, count in sorted_word[:5]:
            print(f"- {word}: {count} lần")
            
    except FileNotFoundError:
        print(f"Lỗi: Không thể tìm thấy file '{file_path}'. Vui lòng kiểm tra lại đường dẫn!")


analyze_text("phase-C-collections/sample_text.txt")