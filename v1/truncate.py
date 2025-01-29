# Function to truncate the string to a certain number of characters
def truncate_string(input_text: str, max_chars: int = 90000) -> str:
    """Truncate the input string to ensure it's within the character limit."""
    return input_text[:max_chars] if len(input_text) > max_chars else input_text