import string
import secrets
import random


def get_user_input():
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
    exclude_ambiguous = input("Exclude ambiguous characters (l,1,I,O,0)? (y/n): ").strip().lower() == "y"

    try:
        quantity = int(input("How many passwords to generate?: "))
        if quantity < 1:
            raise ValueError
    except ValueError:
        print("Invalid quantity.")
        return None

    if not any([include_letters, include_numbers, include_symbols]):
        print("You must select at least one character type.")
        return None

    return length, include_letters, include_numbers, include_symbols, exclude_ambiguous, quantity


def build_character_pool(include_letters, include_numbers, include_symbols, exclude_ambiguous):
    characters = ""
    ambiguous = "l1IO0"

    if include_letters:
        characters += string.ascii_letters
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    if exclude_ambiguous:
        characters = ''.join(c for c in characters if c not in ambiguous)

    return characters


def generate_password(length, characters, include_letters, include_numbers, include_symbols):
    password = []

    if include_letters:
        password.append(secrets.choice(string.ascii_letters))
    if include_numbers:
        password.append(secrets.choice(string.digits))
    if include_symbols:
        password.append(secrets.choice(string.punctuation))

    while len(password) < length:
        password.append(secrets.choice(characters))

    random.shuffle(password)

    return ''.join(password)


def check_strength(password):
    score = 0

    if len(password) >= 12:
        score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 1:
        return "Weak ❌"
    elif score == 2 or score == 3:
        return "Medium ⚠️"
    else:
        return "Strong 💪"


def save_passwords(passwords):
    try:
        filename = input("Enter filename to save passwords (e.g., passwords.txt): ").strip()
        with open(filename, "w") as f:
            for i, (pwd, strength) in enumerate(passwords, start=1):
                f.write(f"{i}. {pwd}  →  {strength}\n")
        print(f"✅ Passwords saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving passwords: {e}")


def main():
    print("=== 🔐 Advanced Secure Password Generator ===")

    user_input = get_user_input()
    if not user_input:
        return

    length, include_letters, include_numbers, include_symbols, exclude_ambiguous, quantity = user_input

    characters = build_character_pool(
        include_letters,
        include_numbers,
        include_symbols,
        exclude_ambiguous
    )

    print("\nGenerated Password(s):\n")

    generated = []
    for i in range(quantity):
        password = generate_password(
            length,
            characters,
            include_letters,
            include_numbers,
            include_symbols
        )
        strength = check_strength(password)
        print(f"{i+1}. {password}  →  {strength}")
        generated.append((password, strength))

    save_option = input("\nDo you want to save these passwords to a file? (y/n): ").strip().lower()
    if save_option == "y":
        save_passwords(generated)


if __name__ == "__main__":
    main()
