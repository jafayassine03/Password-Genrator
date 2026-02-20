import string
import secrets


def get_user_input():
    """Collect and validate user input."""
    try:
        length = int(input("Enter password length (minimum 4): "))
        if length < 4:
            raise ValueError("Password length must be at least 4.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None

    include_letters = input("Include letters? (y/n): ").strip().lower() == "y"
    include_numbers = input("Include numbers? (y/n): ").strip().lower() == "y"
    include_symbols = input("Include symbols? (y/n): ").strip().lower() == "y"

    if not any([include_letters, include_numbers, include_symbols]):
        print("You must select at least one character type.")
        return None

    return length, include_letters, include_numbers, include_symbols


def build_character_pool(include_letters, include_numbers, include_symbols):
    """Build character pool based on user preferences."""
    characters = ""

    if include_letters:
        characters += string.ascii_letters
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    return characters


def generate_password(length, characters):
    """Generate a secure password using secrets module."""
    return ''.join(secrets.choice(characters) for _ in range(length))


def main():
    print("===  Secure Password Generator ===")

    user_input = get_user_input()
    if not user_input:
        return

    length, include_letters, include_numbers, include_symbols = user_input
    characters = build_character_pool(include_letters, include_numbers, include_symbols)

    password = generate_password(length, characters)

    print("\n Generated Password:")
    print(password)


if __name__ == "__main__":
    main()