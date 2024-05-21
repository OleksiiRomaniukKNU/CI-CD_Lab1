import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class DifficultyDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.difficulty = None
        super().__init__(parent, "Choose Difficulty")

    def body(self, master):
        tk.Label(master, text="Select difficulty level:").grid(row=0)
        self.difficulty_var = tk.StringVar(master)
        self.difficulty_var.set("easy")  # default value
        self.option_menu = tk.OptionMenu(master, self.difficulty_var, "easy", "medium", "hard")
        self.option_menu.grid(row=1)

    def apply(self):
        self.difficulty = self.difficulty_var.get()

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper")
        self.setup_game()

    def setup_game(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.rows, self.columns, self.mines = self.choose_difficulty()
        self.buttons = {}
        self.mines_locations = []
        if self.rows and self.columns and self.mines:
            self.create_widgets()
            self.place_mines()

    def choose_difficulty(self):
        dialog = DifficultyDialog(self.master)
        difficulty = dialog.difficulty
        if difficulty == 'easy':
            return 8, 8, 10
        elif difficulty == 'medium':
            return 16, 16, 40
        elif difficulty == 'hard':
            return 24, 24, 99
        else:
            messagebox.showerror("Error", "Invalid difficulty level")
            return None, None, None

    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.columns):
                button = tk.Button(self.master, text="", width=2, height=1, command=lambda r=r, c=c: self.click(r, c))
                button.bind("<Button-3>", self.right_click)
                button.grid(row=r, column=c)
                self.buttons[(r, c)] = button

    def place_mines(self):
        self.mines_locations = random.sample(list(self.buttons.keys()), self.mines)
        for r, c in self.mines_locations:
            self.buttons[(r, c)].config(command=lambda r=r, c=c: self.game_over())

    def click(self, r, c):
        button = self.buttons[(r, c)]
        if button['state'] == tk.DISABLED:
            return
        if (r, c) in self.mines_locations:
            self.game_over()
        else:
            nearby_mines = self.count_nearby_mines(r, c)
            button.config(text=str(nearby_mines), state=tk.DISABLED)
            if nearby_mines == 0:
                self.reveal_neighbors(r, c)

    def count_nearby_mines(self, r, c):
        count = 0
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if (i, j) in self.mines_locations:
                    count += 1
        return count

    def reveal_neighbors(self, r, c):
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if (i, j) in self.buttons and self.buttons[(i, j)]['state'] != tk.DISABLED:
                    self.click(i, j)

    def right_click(self, event):
        button = event.widget
        if button['text'] == "":
            button.config(text="F", bg="orange")
        elif button['text'] == "F":
            button.config(text="", bg="SystemButtonFace")

    def game_over(self):
        for r, c in self.mines_locations:
            self.buttons[(r, c)].config(text="*", bg="red")
        for button in self.buttons.values():
            button.config(state=tk.DISABLED)
        if messagebox.askyesno("Game Over", "You clicked on a mine! Game over.\nDo you want to play again?"):
            self.setup_game()
        else:
            self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
