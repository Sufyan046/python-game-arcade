
import tkinter as tk
from tkinter import messagebox
import random
from utils import user_manager

class QuizGame:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Quiz Game")
        self.game_window.geometry("500x300")

        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["Berlin", "Madrid", "Paris", "Rome"],
                "answer": "Paris"
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "answer": "4"
            },
            {
                "question": "What is the largest planet in our solar system?",
                "options": ["Earth", "Jupiter", "Mars", "Saturn"],
                "answer": "Jupiter"
            }
        ]
        self.current_question = 0
        self.score = 0

        self.question_label = tk.Label(self.game_window, text="", font=("Helvetica", 14), wraplength=480)
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.game_window, text="", font=("Helvetica", 12), command=lambda i=i: self.check_answer(i))
            self.option_buttons.append(button)
            button.pack(pady=5)

        self.next_question()

    def next_question(self):
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.question_label.config(text=q["question"])
            random.shuffle(q["options"])
            for i in range(4):
                self.option_buttons[i].config(text=q["options"][i])
        else:
            self.show_score()

    def check_answer(self, selected_option_index):
        q = self.questions[self.current_question]
        selected_answer = self.option_buttons[selected_option_index]["text"]
        if selected_answer == q["answer"]:
            self.score += 1
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            messagebox.showerror("Incorrect!", f"Sorry, the correct answer was {q['answer']}.")
        
        self.current_question += 1
        self.next_question()

    def show_score(self):
        user_manager.update_score(self.current_user, "Quiz Game", self.score)
        for widget in self.game_window.winfo_children():
            widget.destroy()
        
        score_label = tk.Label(self.game_window, text=f"Your final score is: {self.score}/{len(self.questions)}", font=("Helvetica", 16))
        score_label.pack(pady=20)

        play_again_button = tk.Button(self.game_window, text="Play Again", command=self.reset_game)
        play_again_button.pack(pady=10)

        back_button = tk.Button(self.game_window, text="Back to Menu", command=self.game_window.destroy)
        back_button.pack(pady=5)

    def reset_game(self):
        self.current_question = 0
        self.score = 0
        # Re-create the widgets for the quiz
        self.__init__(self.root, self.current_user)

def play(root, current_user):
    QuizGame(root, current_user)
