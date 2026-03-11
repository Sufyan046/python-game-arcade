
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from utils import user_manager

class NumberGuessingGame:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Number Guessing Game")
        self.game_window.geometry("300x200")

        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        self.label = tk.Label(self.game_window, text="I'm thinking of a number between 1 and 100.", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.game_window)
        self.entry.pack(pady=5)

        self.guess_button = tk.Button(self.game_window, text="Guess", command=self.check_guess)
        self.guess_button.pack(pady=5)

        self.play_again_button = tk.Button(self.game_window, text="Play Again", command=self.reset_game)
        self.play_again_button.pack(pady=5)

        self.back_button = tk.Button(self.game_window, text="Back to Menu", command=self.game_window.destroy)
        self.back_button.pack(pady=5)

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            if guess < self.secret_number:
                messagebox.showinfo("Result", "Too low!")
            elif guess > self.secret_number:
                messagebox.showinfo("Result", "Too high!")
            else:
                user_manager.update_score(self.current_user, "Number Guessing Game", self.attempts)
                messagebox.showinfo("Congratulations!", f"You guessed it in {self.attempts} attempts!")
                self.reset_game()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.entry.delete(0, tk.END)

def play(root, current_user):
    NumberGuessingGame(root, current_user)
