# Password Manager

## 📌 About
This is a **Password Manager** that allows users to securely store, retrieve, and manage passwords for different websites. It encrypts passwords using **Fernet encryption** from the `cryptography` module, ensuring security.

## ⚡ Features
- **Add a new password** 🔐
- **View all stored passwords** 🔍
- **Retrieve a password for a specific website** 🔎
- **Delete saved credentials** 🗑️
- **Secure encryption** using **Fernet**

## 🛠️ Installation
1. **Clone the repository**:
   ```sh
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
   ```
2. **Install required dependencies**:
   ```sh
   pip install inquirer pwinput cryptography
   ```

## 🚀 Usage
Run the script to start the password manager:
```sh
python password_manager.py
```
Follow the interactive prompts to store and manage passwords securely.

## 🔒 Security
- Uses **Fernet encryption** to securely store passwords.
- Stores encrypted passwords in `passwords.json`.
- Saves the encryption key in `key.key` (Do **not** share this file!).

## 📝 How It Works
1. **When first run**, it generates a new encryption key and saves it in `key.key`.
2. **Passwords are encrypted** before being stored in `passwords.json`.
3. **Users can retrieve stored passwords**, which are decrypted before display.

## 🛑 Notes
- If `key.key` is lost, encrypted passwords **cannot be recovered**.
- This is a simple password manager and is **not recommended for highly sensitive data**.

## 📜 License
This project is open-source. Feel free to modify and use it as needed.

