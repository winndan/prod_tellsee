def validate_input(raw_text: str):
    if not raw_text:
        raise ValueError("Input cannot be empty")

    if len(raw_text) > 3000:
        raise ValueError("Input exceeds 3000 characters")
