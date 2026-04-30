import string
import secrets
import random
import pyperclip
import math

def get_user_input():
    try:
        length = int(input("Enter password length (minimum 4): "))
        if length < 4:
            raise ValueError
    except:
        print("Invalid length")
        return None

    include_letters = input("Include letters? (y/n): ").strip().lower() == "y"
    include_numbers = input("Include numbers? (y/n): ").strip().lower() == "y"
    include_symbols = input("Include symbols? (y/n): ").strip().lower() == "y"
    exclude_ambiguous = input("Exclude ambiguous characters (l,1,I,O,0)? (y/n): ").strip().lower() == "y"

    try:
        quantity = int(input("How many passwords to generate?: "))
        if quantity < 1:
            raise ValueError
    except:
        print("Invalid quantity")
        return None

    if not any([include_letters, include_numbers, include_symbols]):
        print("Select at least one character type")
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
        return "Weak ❌", score
    elif score <= 3:
        return "Medium ⚠️", score
    else:
        return "Strong 💪", score

def calculate_entropy(password, pool_size):
    return len(password) * math.log2(pool_size)

def estimate_crack_time(entropy):
    guesses_per_second = 1e10
    seconds = (2 ** entropy) / guesses_per_second
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"

def visualize_strength(score):
    return "█" * score + "-" * (4 - score)

def save_passwords(passwords):
    try:
        filename = input("Enter filename: ").strip()
        with open(filename, "w") as f:
            for i, (pwd, strength, entropy, crack, bar) in enumerate(passwords, start=1):
                f.write(f"{i}. {pwd} → {strength} | {bar} | Entropy: {entropy:.2f} bits | Crack Time: {crack}\n")
        print("Saved successfully")
    except:
        print("Error saving file")

def copy_to_clipboard(passwords):
    try:
        choice = int(input("Enter password number to copy: "))
        if 1 <= choice <= len(passwords):
            pyperclip.copy(passwords[choice - 1][0])
            print("Copied")
        else:
            print("Invalid choice")
    except:
        print("Invalid input")

def regenerate_one(generated, length, characters, include_letters, include_numbers, include_symbols, pool_size):
    try:
        choice = int(input("Enter password number to regenerate: "))
        if 1 <= choice <= len(generated):
            password = generate_password(length, characters, include_letters, include_numbers, include_symbols)
            strength, score = check_strength(password)
            entropy = calculate_entropy(password, pool_size)
            crack = estimate_crack_time(entropy)
            bar = visualize_strength(score)

            generated[choice - 1] = (password, strength, entropy, crack, bar)

            print(f"Updated {choice}: {password} → {strength} | {bar} | Entropy: {entropy:.2f} bits | Crack Time: {crack}")
        else:
            print("Invalid choice")
    except:
        print("Invalid input")

def main():
    print("=== Advanced Secure Password Generator ===")

    user_input = get_user_input()
    if not user_input:
        return

    length, include_letters, include_numbers, include_symbols, exclude_ambiguous, quantity = user_input

    characters = build_character_pool(include_letters, include_numbers, include_symbols, exclude_ambiguous)
    pool_size = len(characters)

    print("\nGenerated Password(s):\n")

    generated = []
    seen = set()

    while len(generated) < quantity:
        password = generate_password(length, characters, include_letters, include_numbers, include_symbols)
        if password in seen:
            continue
        seen.add(password)

        strength, score = check_strength(password)
        entropy = calculate_entropy(password, pool_size)
        crack = estimate_crack_time(entropy)
        bar = visualize_strength(score)

        print(f"{len(generated)+1}. {password} → {strength} | {bar} | Entropy: {entropy:.2f} bits | Crack Time: {crack}")
        generated.append((password, strength, entropy, crack, bar))

    if input("\nRegenerate a password? (y/n): ").strip().lower() == "y":
        regenerate_one(generated, length, characters, include_letters, include_numbers, include_symbols, pool_size)

    if input("\nCopy a password? (y/n): ").strip().lower() == "y":
        copy_to_clipboard(generated)

    if input("\nSave passwords? (y/n): ").strip().lower() == "y":
        save_passwords(generated)

if __name__ == "__main__":
    main()