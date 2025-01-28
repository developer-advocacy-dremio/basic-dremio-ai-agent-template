# Function: `truncate_string`

## Description
The `truncate_string` function ensures that a given input string does not exceed a specified maximum number of characters. If the input string's length exceeds the specified limit, it is truncated to fit within the limit. Otherwise, the original string is returned unchanged.

---

## Function Signature
```python
def truncate_string(input_text: str, max_chars: int = 90000) -> str:
