import string
import secrets
import random
import pyperclip
import math
import json
from datetime import datetime

HISTORY_FILE = "password_history.json"

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
    no_repeat = input("Disallow repeating characters? (y/n): ").strip().lower() == "y"

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

    return length, include_letters, include_numbers, include_symbols, exclude_ambiguous, quantity, no_repeat

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

def generate_password(length, characters, include_letters, include_numbers, include_symbols, no_repeat):
    password = []

    if include_letters:
        password.append(secrets.choice(string.ascii_letters))
    if include_numbers:
        password.append(secrets.choice(string.digits))
    if include_symbols:
        password.append(secrets.choice(string.punctuation))

    used = set(password)

    while len(password) < length:
        c = secrets.choice(characters)

        if no_repeat and c in used:
            continue

        password.append(c)
        used.add(c)

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
                f.write(
                    f"{i}. {pwd} → {strength} | {bar} | "
                    f"Entropy: {entropy:.2f} bits | Crack Time: {crack}\n"
                )

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

def regenerate_one(
    generated,
    length,
    characters,
    include_letters,
    include_numbers,
    include_symbols,
    pool_size,
    no_repeat
):
    try:
        choice = int(input("Enter password number to regenerate: "))

        if 1 <= choice <= len(generated):

            password = generate_password(
                length,
                characters,
                include_letters,
                include_numbers,
                include_symbols,
                no_repeat
            )

            strength, score = check_strength(password)
            entropy = calculate_entropy(password, pool_size)
            crack = estimate_crack_time(entropy)
            bar = visualize_strength(score)

            generated[choice - 1] = (
                password,
                strength,
                entropy,
                crack,
                bar
            )

            print(
                f"Updated {choice}: {password} → {strength} | "
                f"{bar} | Entropy: {entropy:.2f} bits | Crack Time: {crack}"
            )

        else:
            print("Invalid choice")

    except:
        print("Invalid input")

def save_history(passwords):
    history = []

    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except:
        history = []

    for pwd, strength, entropy, crack, bar in passwords:
        history.append({
            "password": pwd,
            "strength": strength,
            "entropy": round(entropy, 2),
            "crack_time": crack,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def view_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

        if not history:
            print("No history found")
            return

        print("\nPassword History:\n")

        for i, item in enumerate(history, start=1):
            print(
                f"{i}. {item['password']} | "
                f"{item['strength']} | "
                f"Entropy: {item['entropy']} bits | "
                f"Crack Time: {item['crack_time']} | "
                f"{item['date']}"
            )

    except:
        print("No history found")

def main():
    print("=== Advanced Secure Password Generator ===")

    if input("View previous history? (y/n): ").strip().lower() == "y":
        view_history()

    user_input = get_user_input()

    if not user_input:
        return

    (
        length,
        include_letters,
        include_numbers,
        include_symbols,
        exclude_ambiguous,
        quantity,
        no_repeat
    ) = user_input

    characters = build_character_pool(
        include_letters,
        include_numbers,
        include_symbols,
        exclude_ambiguous
    )

    pool_size = len(characters)

    print("\nGenerated Password(s):\n")

    generated = []
    seen = set()

    while len(generated) < quantity:

        password = generate_password(
            length,
            characters,
            include_letters,
            include_numbers,
            include_symbols,
            no_repeat
        )

        if password in seen:
            continue

        seen.add(password)

        strength, score = check_strength(password)
        entropy = calculate_entropy(password, pool_size)
        crack = estimate_crack_time(entropy)
        bar = visualize_strength(score)

        print(
            f"{len(generated)+1}. {password} → {strength} | "
            f"{bar} | Entropy: {entropy:.2f} bits | Crack Time: {crack}"
        )

        generated.append((
            password,
            strength,
            entropy,
            crack,
            bar
        ))

    save_history(generated)

    if input("\nRegenerate a password? (y/n): ").strip().lower() == "y":
        regenerate_one(
            generated,
            length,
            characters,
            include_letters,
            include_numbers,
            include_symbols,
            pool_size,
            no_repeat
        )

    if input("\nCopy a password? (y/n): ").strip().lower() == "y":
        copy_to_clipboard(generated)

    if input("\nSave passwords? (y/n): ").strip().lower() == "y":
        save_passwords(generated)

if __name__ == "__main__":
    main()