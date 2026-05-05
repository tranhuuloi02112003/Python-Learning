import utils

def analyze_text(file_path):
    total_lines = 0
    total_chars = 0
    word_count = {} # Dictionary de dem tu

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

        utils.print_header("Bao Cao Phan Tich")
        print(f"Tong so dong: {total_lines}")
        print(f"Tong so ky tu: {total_chars}")

        print("Top 5 tu xuat hien nhieu nhat:")
        sorted_word = sorted(word_count.items(), key = lambda word: word[1], reverse=True)

        for word, count in sorted_word[:5]:
            print(f"- {word}: {count} lan")
            
    except FileNotFoundError:
        print(f"Loi: Khong the tim thay file '{file_path}'. Vui long kiem tra lai duong dan!")


analyze_text("phase-C-collections/sample_text.txt")