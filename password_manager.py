import inquirer
import pwinput
import json
from cryptography.fernet import Fernet

# Generate and store a key if it doesn't exist
key_file = "key.key"

try:
    with open(key_file, "rb") as file:
        key = file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open(key_file, "wb") as file:
        file.write(key)

cipher = Fernet(key)

# Load stored credentials
db_file = "passwords.json"
try:
    with open(db_file, "r") as file:
        db = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    db = {}

while True:
    choices_map = {
        'Add a New Password': 'add',
        'View all stored passwords': 'view',
        'Retrieve a password for a specific website': 'retrieve',
        'Delete a saved password': 'delete',
        'Exit the program': 'exit'
    }

    questions = [
        inquirer.List('option',
                      message='Choose an option',
                      choices=list(choices_map.keys())
                      ),
    ]

    answers = inquirer.prompt(questions)
    shortened_choice = choices_map[answers["option"]]

    if shortened_choice == 'add':
        website = input("Enter website: ").strip().lower()
        username = input("Enter username: ").strip()
        password = pwinput.pwinput(prompt="Enter password: ", mask="*")

        encrypted_password = cipher.encrypt(password.encode()).decode()  # Encrypt

        if website not in db:
            db[website] = []

        # Check if username already exists for the website
        existing_user = next((cred for cred in db[website] if cred['username'] == username), None)
        if existing_user:
            overwrite = input("⚠️ Username already exists! Overwrite password? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("❌ Password not updated.")
                continue
            existing_user['password'] = encrypted_password
        else:
            db[website].append({"username": username, "password": encrypted_password})

        with open(db_file, "w") as file:
            json.dump(db, file, indent=4)

        print(f"✅ Password saved for {website}.")

    elif shortened_choice == 'view':
        if db:
            for website, credentials in db.items():
                print(f"\n🌐 Website: {website}")
                for cred in credentials:
                    print(f"   👤 Username: {cred['username']}, 🔑 Password: {'********'}")  # Fixed length mask
        else:
            print("⚠️ No passwords stored.")

    elif shortened_choice == 'retrieve':
        website = input("Enter the website: ").strip().lower()
        if website in db:
            print(f"\n🔎 Stored credentials for {website}:")
            for cred in db[website]:
                decrypted_password = cipher.decrypt(cred['password'].encode()).decode()  # Decrypt
                print(f"   👤 Username: {cred['username']}, 🔑 Password: {decrypted_password}")
        else:
            print(f"⚠️ No stored passwords for {website}.")

    elif shortened_choice == 'delete':
        website = input("Enter the website to delete credentials: ").strip().lower()
        if website in db:
            del db[website]
            with open(db_file, "w") as file:
                json.dump(db, file, indent=4)
            print(f"🗑️ All credentials for {website} have been deleted.")
        else:
            print(f"⚠️ No stored passwords for {website}.")

    elif shortened_choice == 'exit':
        print("👋 Exiting the program...")
        break
