import random
import string

print(" === PASSWORD GENERATOR === ")

length = int(input("Enter password length: "))

print("Include letters? (y/n)")
letters = input("> ")

print("Include numbers? (y/n)")
numbers = input("> ")

print("Include symbols? (y/n)")
symbols = input("> ")

characters = ""

if letters == "y":
    characters += string.ascii_letters

if numbers == "y":
    characters += string.digits

if symbols == "y":
    characters += string.punctuation

if characters == "":
    print("You must select at least one option!")
else:
    password = ""
    for i in range(length):
        password += random.choice(characters)

    print("\nGenerated Password:")
    print(password)
