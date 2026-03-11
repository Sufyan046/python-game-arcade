
import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from utils import user_manager, leaderboard
from games import tic_tac_toe, number_guessing_game, quiz_game

class GameArcade:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Gaming Arcade")
        self.root.geometry("400x300")
        self.current_user = None
        self.show_login_register()

    def show_login_register(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.label = tk.Label(self.root, text="Welcome to the Arcade!", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.login_button = tk.Button(self.root, text="Login", command=self.login_window)
        self.login_button.pack(pady=10)
        self.register_button = tk.Button(self.root, text="Register", command=self.register_window)
        self.register_button.pack()

    def login_window(self):
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring("Login", "Enter your password:", show='*')
        if username and password:
            success, message = user_manager.login_user(username, password)
            if success:
                self.current_user = username
                self.show_main_menu()
            else:
                messagebox.showerror("Login Failed", message)

    def register_window(self):
        username = simpledialog.askstring("Register", "Choose a username:")
        password = simpledialog.askstring("Register", "Choose a password:", show='*')
        if username and password:
            success, message = user_manager.register_user(username, password)
            if success:
                messagebox.showinfo("Registration Successful", message)
            else:
                messagebox.showerror("Registration Failed", message)

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.label = tk.Label(self.root, text=f"Welcome, {self.current_user}!", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.play_button = tk.Button(self.root, text="Play Games", command=self.show_game_selection)
        self.play_button.pack(pady=10)
        self.leaderboard_button = tk.Button(self.root, text="Leaderboard", command=self.show_leaderboard)
        self.leaderboard_button.pack()
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

    def show_game_selection(self):
        game_window = tk.Toplevel(self.root)
        game_window.title("Select a Game")
        game_window.geometry("300x200")

        tk.Label(game_window, text="Choose a game to play:", font=("Helvetica", 14)).pack(pady=10)

        tk.Button(game_window, text="Tic Tac Toe", command=lambda: self.start_game(tic_tac_toe)).pack(pady=5)
        tk.Button(game_window, text="Number Guessing Game", command=lambda: self.start_game(number_guessing_game)).pack(pady=5)
        tk.Button(game_window, text="Quiz Game", command=lambda: self.start_game(quiz_game)).pack(pady=5)

    def start_game(self, game_module):
        game_module.play(self.root, self.current_user)

    def show_leaderboard(self):
        lb_window = tk.Toplevel(self.root)
        lb_window.title("Arcade Leaderboard")
        lb_window.geometry("400x500")

        tk.Label(lb_window, text="--- TOP PLAYERS ---", font=("Helvetica", 16, "bold")).pack(pady=10)

        for game in ["Tic Tac Toe", "Number Guessing Game", "Quiz Game"]:
            frame = tk.LabelFrame(lb_window, text=game, font=("Helvetica", 12, "bold"), padx=10, pady=10)
            frame.pack(fill="both", expand="yes", padx=20, pady=10)

            top_scores = leaderboard.get_top_scores(game)
            if not top_scores:
                tk.Label(frame, text="No scores yet!").pack()
            else:
                for idx, (user, score) in enumerate(top_scores):
                    # For Number Guessing, lower is better (attempts), for others higher is better
                    suffix = "attempts" if game == "Number Guessing Game" else "points"
                    tk.Label(frame, text=f"{idx+1}. {user}: {score} {suffix}").pack(anchor="w")

        tk.Button(lb_window, text="Close", command=lb_window.destroy).pack(pady=10)

    def logout(self):
        self.current_user = None
        self.show_login_register()

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    root = tk.Tk()
    app = GameArcade(root)
    root.mainloop()
