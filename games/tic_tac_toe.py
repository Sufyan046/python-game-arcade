
import tkinter as tk
from tkinter import messagebox, simpledialog
from utils import user_manager

class TicTacToe:
    def __init__(self, root, current_user):
        self.root = root
        self.player1 = current_user
        self.player2 = simpledialog.askstring("Multiplayer", "Enter Player 2's name (or 'Computer'):") or "Player 2"
        
        self.game_window = tk.Toplevel(self.root)
        self.game_window.title("Tic Tac Toe")
        self.game_window.geometry("300x450")

        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.info_label = tk.Label(self.game_window, text=f"{self.player1} (X) vs {self.player2} (O)", font=("Helvetica", 10))
        self.info_label.grid(row=0, column=0, columnspan=3, pady=5)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.game_window, text="", font=("Helvetica", 20), width=5, height=2,
                                               command=lambda i=i, j=j: self.on_click(i, j))
                self.buttons[i][j].grid(row=i+1, column=j)

        self.status_label = tk.Label(self.game_window, text=f"{self.player1}'s turn", font=("Helvetica", 12))
        self.status_label.grid(row=4, column=0, columnspan=3, pady=10)

        self.play_again_button = tk.Button(self.game_window, text="Play Again", command=self.reset_game)
        self.play_again_button.grid(row=5, column=0, columnspan=3)

        self.back_button = tk.Button(self.game_window, text="Back to Menu", command=self.game_window.destroy)
        self.back_button.grid(row=6, column=0, columnspan=3, pady=5)

    def on_click(self, i, j):
        if self.board[i][j] == "":
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)
            
            if self.check_win(self.current_player):
                winner_name = self.player1 if self.current_player == "X" else self.player2
                messagebox.showinfo("Tic Tac Toe", f"{winner_name} wins!")
                # Record win to leaderboard if the winner is a registered user
                user_manager.increment_score(winner_name, "Tic Tac Toe")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                current_name = self.player1 if self.current_player == "X" else self.player2
                self.status_label.config(text=f"{current_name}'s turn")

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        self.status_label.config(text=f"{self.player1}'s turn")

def play(root, current_user):
    TicTacToe(root, current_user)
