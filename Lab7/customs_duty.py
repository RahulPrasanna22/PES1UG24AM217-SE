import math


def _to_finite_float(text):
    """Convert text to a finite, non-negative float, or return None if invalid."""
    try:
        number = float(text.strip())
    except ValueError:
        return None
    if not math.isfinite(number) or number < 0:
        return None
    return number


def parse_declaration(text):
    """Parse 'category:value' into (category, value).

    Returns None for any invalid input (non-string, wrong number of ':',
    empty category, or a value that is not a finite non-negative number).
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    category = parts[0].strip().lower()
    if not category:
        return None
    value = _to_finite_float(parts[1])
    if value is None:
        return None
    return category, value


def duty_amount(text):
    """Compute duty from 'value@rate' (rate in percent).

    Returns None for any invalid input (non-string, wrong number of '@',
    non-numeric / negative / non-finite parts, or an overflowing result).
    """
    if not isinstance(text, str):
        return None
    parts = text.split('@')
    if len(parts) != 2:
        return None
    value = _to_finite_float(parts[0])
    rate = _to_finite_float(parts[1])
    if value is None or rate is None:
        return None
    duty = value * rate / 100
    if not math.isfinite(duty):
        return None
    return duty


def hs_chapter(code):
    """Return the 2-digit HS chapter (1-99) of a code like '8517.12'.

    Returns None for any invalid input (non-string, fewer than two leading
    ASCII digits before the first '.', or chapter 00).
    """
    if not isinstance(code, str):
        return None
    head = code.strip().split('.')[0]
    if len(head) < 2 or not (head.isascii() and head.isdigit()):
        return None
    chapter = int(head[:2])
    if chapter < 1:
        return None
    return chapter


def main():
    print("==== Running parse_declaration ====")
    user_input = input("Enter category:value (e.g. electronics:25000): ")
    result = parse_declaration(user_input)
    print("Category and Value:", result if result is not None else "Invalid declaration")

    print("\n==== Running duty_amount ====")
    user_input = input("Enter value@rate (e.g. 25000@20): ")
    result = duty_amount(user_input)
    print("Duty Amount:", result if result is not None else "Invalid value@rate input")

    print("\n==== Running hs_chapter ====")
    user_input = input("Enter an HS code (e.g. 8517.12): ")
    result = hs_chapter(user_input)
    print("Chapter:", result if result is not None else "Invalid HS code")


if __name__ == "__main__":
    main()