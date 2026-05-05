def analyze_log():
    status_count = {
        "INFO": 0,
        "ERROR": 0,
        "WARNING": 0
    }

    error_lines = []

    total_lines = 0
    with open('phase-C-collections/app.log', mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            total_lines += 1
            if "ERROR" in line:
                status_count["ERROR"] += 1
                error_lines.append(line)
            elif "INFO" in line:
                status_count["INFO"] += 1
            elif "WARNING" in line:
                status_count["WARNING"] += 1

    print(f"=== BAO CAO LOG (Tong so dong: {total_lines}) ===")
    print(f"So loi Error: {status_count['ERROR']}")
    print(f"So canh bao Warning: {status_count['WARNING']}")
    print(f"So thong tin Info: {status_count['INFO']}")
    
    print("\n--- CHI TIET CAC DONG LOI (ERROR) ---")
    for err in error_lines:
        print(f"{err}")

analyze_log()