import tkinter as tk
from tkinter import ttk, messagebox
import random
from tkinter.font import Font


class GuessTheNumberGame:
    LOWER_BOUND = 1
    UPPER_BOUND = 100
    MAX_ATTEMPTS = 10

    def __init__(self, master):
        self.master = master
        self.master.title("🎯 Guess The Number")
        self.set_window_geometry(500, 420)
        self.master.resizable(False, False)
        self.master.configure(bg="#2c3e50")

        self.target_number = 0
        self.attempts = 0

        self.setup_styles()
        self.create_widgets()
        self.start_new_game()

    def set_window_geometry(self, width, height):
        """Centers the window on the screen."""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        self.heading_font = Font(family="Segoe UI", size=18, weight="bold")
        self.label_font = Font(family="Segoe UI", size=11)
        self.entry_font = Font(family="Segoe UI", size=12)
        self.button_font = Font(family="Segoe UI", size=10, weight="bold")
        self.feedback_font = Font(family="Segoe UI", size=14, weight="bold")
        self.attempts_font = Font(family="Segoe UI", size=10)

        style.configure('TFrame', background='#34495e')
        style.configure('TLabel', background='#34495e', foreground='white', font=self.label_font)
        style.configure('Heading.TLabel', background='#2c3e50', foreground='#ecf0f1', font=self.heading_font)
        style.configure('Feedback.TLabel', background='#34495e', foreground='#ecf0f1', font=self.feedback_font)
        style.configure('Attempts.TLabel', background='#34495e', foreground='#bdc3c7', font=self.attempts_font)

        style.configure('TEntry', fieldbackground='#ecf0f1', foreground='#2c3e50', font=self.entry_font)

        style.configure('TButton',
                        background='#3498db',
                        foreground='white',
                        font=self.button_font,
                        padding=10,
                        relief='flat')
        style.map('TButton',
                  background=[('active', '#2980b9'), ('pressed', '#2980b9')],
                  foreground=[('active', 'white'), ('pressed', 'white')])

        style.configure('Red.TButton',
                        background='#e74c3c',
                        foreground='white')
        style.map('Red.TButton',
                  background=[('active', '#c0392b'), ('pressed', '#c0392b')],
                  foreground=[('active', 'white'), ('pressed', 'white')])

    def create_widgets(self):
        ttk.Label(self.master, text="Guess The Number!", style='Heading.TLabel').pack(pady=20)

        info_frame = ttk.Frame(self.master, padding="20 10", style='TFrame')
        info_frame.pack(padx=30, fill="x")

        self.instruction_label = ttk.Label(info_frame, text="", style='TLabel')
        self.instruction_label.pack(pady=4)

        self.attempts_label = ttk.Label(info_frame, text="", style='Attempts.TLabel')
        self.attempts_label.pack(pady=4)

        guess_frame = ttk.Frame(self.master, padding="15", style='TFrame')
        guess_frame.pack(padx=30, pady=10, fill="x")

        ttk.Label(guess_frame, text="Your Guess:").grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
        self.guess_entry = ttk.Entry(guess_frame, width=20, justify='center')
        self.guess_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.guess_entry.bind("<Return>", self.check_guess)

        self.guess_button = ttk.Button(guess_frame, text="Guess", command=self.check_guess, cursor="hand2")
        self.guess_button.grid(row=0, column=2, padx=(10, 0), pady=10)

        guess_frame.grid_columnconfigure(1, weight=1)

        self.feedback_label = ttk.Label(self.master, text="", style='Feedback.TLabel', wraplength=460, justify="center")
        self.feedback_label.pack(pady=15)

        self.new_game_button = ttk.Button(self.master, text="New Game", command=self.start_new_game, style='Red.TButton', cursor="hand2")
        self.new_game_button.pack(pady=(5, 15))

    def start_new_game(self):
        self.target_number = random.randint(self.LOWER_BOUND, self.UPPER_BOUND)
        self.attempts = 0
        self.update_attempts_label()
        self.update_instruction()
        self.set_feedback("Find the Number")
        self.set_input_state(enabled=True)
        self.clear_entry()
        self.guess_entry.focus_set()

    def update_attempts_label(self):
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.MAX_ATTEMPTS}")

    def update_instruction(self):
        self.instruction_label.config(text=f"I'm thinking of a number between {self.LOWER_BOUND} and {self.UPPER_BOUND}.")

    def clear_entry(self):
        self.guess_entry.delete(0, tk.END)

    def set_feedback(self, text, color=None):
        self.feedback_label.config(text=text)
        if color:
            self.feedback_label.config(foreground=color)

    def set_input_state(self, enabled=True):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.guess_entry.config(state=state)
        self.guess_button.config(state=state)
        self.new_game_button.config(state=tk.NORMAL if not enabled else tk.DISABLED)

    def check_guess(self, event=None):
        guess_str = self.guess_entry.get().strip()
        if not guess_str:
            self.set_feedback("⚠️ Please enter a number!", "#f1c40f")
            return

        try:
            guess = int(guess_str)
        except ValueError:
            self.set_feedback("❌ Invalid input. Enter a whole number.", "#e74c3c")
            self.clear_entry()
            return

        if not (self.LOWER_BOUND <= guess <= self.UPPER_BOUND):
            self.set_feedback(f"⚠️ Enter a number between {self.LOWER_BOUND} and {self.UPPER_BOUND}.", "#f1c40f")
            self.clear_entry()
            return

        self.attempts += 1
        self.update_attempts_label()

        diff = guess - self.target_number
        abs_diff = abs(diff)

        if abs_diff == 0:
            self.set_feedback(f"🎉 Correct! You guessed it in {self.attempts} attempts.", "#2ecc71")
            self.set_input_state(False)
            return
        elif abs_diff == 1:
            hint = "🔥 So close!"
        elif abs_diff <= 10:
            hint = "👌 You're close!"
        else:
            hint = "⬆️ Way too high!" if diff > 0 else "⬇️ Way too low!"

        self.set_feedback(hint, "#3498db")

        if self.attempts >= self.MAX_ATTEMPTS:
            self.set_feedback(f"💥 Game Over! The number was {self.target_number}.", "#e74c3c")
            self.set_input_state(False)

        self.clear_entry()


if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheNumberGame(root)
    root.mainloop()
