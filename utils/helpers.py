def get_text_input(prompt) -> str:
    while True:
        text = input(prompt).strip().lower()
        if not text:
            print("Input cannot be empty. Please try again.")
            continue
        return text
