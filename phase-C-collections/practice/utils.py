def print_header(title):
    banner_length = len(title) + 8
    print("=" * banner_length)
    print(f"  {title.upper()}  ")
    print("=" * banner_length)
    
def clear_text(text):
    return text.lower().replace(',','').replace('.','').replace('"','').strip();