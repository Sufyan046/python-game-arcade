
import json
import os

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def get_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Error saving users: {e}")

def register_user(username, password):
    users = get_users()
    if username in users:
        return False, "Username already exists."
    
    users[username] = {"password": password, "scores": {}}
    save_users(users)
    return True, "Registration successful!"

def login_user(username, password):
    users = get_users()
    if username not in users or users[username]["password"] != password:
        return False, "Invalid username or password."
    return True, "Login successful!"

def update_score(username, game, score):
    users = get_users()
    if username in users:
        # For Number Guessing, lower is better. For others, higher is better.
        if game == "Number Guessing Game":
            if game not in users[username]["scores"] or score < users[username]["scores"][game]:
                users[username]["scores"][game] = score
                save_users(users)
        else:
            if game not in users[username]["scores"] or score > users[username]["scores"][game]:
                users[username]["scores"][game] = score
                save_users(users)

def increment_score(username, game):
    users = get_users()
    if username in users:
        current_score = users[username]["scores"].get(game, 0)
        users[username]["scores"][game] = current_score + 1
        save_users(users)
