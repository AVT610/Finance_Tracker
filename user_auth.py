import json
import os

USERS_FILE = "users.json"

class UserAuth:
    @staticmethod
    def load_users():
        if not os.path.exists(USERS_FILE):
            return {}
        with open(USERS_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_users(users):
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

    @staticmethod
    def register(username, password):
        users = UserAuth.load_users()
        if username in users:
            print("Username already exists.")
            return False
        users[username] = password
        UserAuth.save_users(users)
        print("Registration successful.")
        return True

    @staticmethod
    def login(username, password):
        users = UserAuth.load_users()
        if users.get(username) == password:
            print(f"Welcome, {username}!")
            return True
        print("Invalid username or password.")
        return False
