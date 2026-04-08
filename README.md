🔐 Password Generator (Python)
A secure and beginner-friendly password generator that runs directly in the terminal.

This project was built while practicing Python fundamentals and completing daily coding challenges to improve step by step. It focuses on clean logic, structured code, user input validation, and secure randomness generation.

Simple. Practical. Reliable.

🚀 Features
Generate random passwords directly from the terminal

Choose custom password length

Select character types:
✅ Letters (uppercase & lowercase)
✅ Numbers
✅ Symbols

Exclude ambiguous characters (like l, 1, I, O, 0)

Input validation for safer usage

Generate multiple passwords at once

Built-in password strength indicator (Weak ❌, Medium ⚠️, Strong 💪)

Option to save generated passwords to a file

Built using only Python standard libraries

Lightweight and easy to modify or extend

🧠 How It Works
The user enters the desired password length.

The user selects which character types to include.

The program builds a character pool based on the selections.

A secure random password is generated using the secrets module.

Password strength is automatically checked and displayed.

Multiple passwords can be generated in one run.

Optionally, passwords can be saved to a text file for later use.

Fast. Simple. Effective.

🛠️ Built With
Python 3

string module

secrets module (for cryptographically secure randomness)

random module (for shuffling characters)

⚠️ Note: The secrets module is recommended over random for generating secure passwords.

▶️ How to Run
bash
python password_generator.py
Make sure you have Python 3 installed on your system.
You can check your version with:

bash
python --version
📌 Future Improvements
Add copy-to-clipboard support

Create a GUI version (Tkinter)

Convert into a pip-installable package

Add command-line argument support (argparse)

Add encryption for saved password files

📖 What I Learned
Handling and validating user input

Using conditional logic effectively

Working with Python standard libraries

Writing clean and modular functions

Structuring a project for GitHub

Improving readability and documentation

Adding persistence features (file saving)

Implementing password strength checks

📜 License
Totally free to use! Play around with it and make it your own 😄
