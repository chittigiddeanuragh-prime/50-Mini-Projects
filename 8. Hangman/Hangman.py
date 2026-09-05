import tkinter as tk
import random


BG_COLOR = "#0B1026"
PANEL_COLOR = "#151D3A"
BOARD_COLOR = "#111936"

TITLE_COLOR = "#F5F7FF"
SUBTITLE_COLOR = "#7DD3FC"
LETTER_COLOR = "#38BDF8"
CORRECT_COLOR = "#22C55E"
WRONG_COLOR = "#FF4F81"

BUTTON_COLOR = "#26345F"
BUTTON_HOVER = "#394A82"

RESET_COLOR = "#7C3AED"
RESET_HOVER = "#9F67FF"

BORDER_COLOR = "#4C63D2"
TEXT_MUTED = "#8D9AC7"


WORDS = [
    "PYTHON",
    "COMPUTER",
    "PROGRAM",
    "KEYBOARD",
    "MONITOR",
    "INTERNET",
    "SOFTWARE",
    "HARDWARE",
    "CODING",
    "DATABASE",
    "ALGORITHM",
    "FUNCTION",
    "VARIABLE",
    "GITHUB",
    "DEVELOPER"
]

MAX_WRONG = 6


root = tk.Tk()
root.title("Hangman")
root.geometry("560x700")
root.resizable(False, False)
root.configure(bg=BG_COLOR)


word = ""
guessed_letters = set()
wrong_guesses = 0
game_over = False

letter_buttons = {}


def start_game():
    global word, guessed_letters, wrong_guesses, game_over

    word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    game_over = False

    update_display()
    update_hangman()

    status_label.config(
        text="💙 Guess the hidden word!",
        fg=SUBTITLE_COLOR
    )

    attempts_label.config(
        text=f"❌ Wrong Attempts: 0 / {MAX_WRONG}"
    )

    for button in letter_buttons.values():
        button.config(
            state="normal",
            bg=BUTTON_COLOR,
            fg=TITLE_COLOR
        )


def display_word():
    return " ".join(
        letter if letter in guessed_letters else "_"
        for letter in word
    )


def guess_letter(letter):
    global wrong_guesses, game_over

    if game_over:
        return

    guessed_letters.add(letter)

    letter_buttons[letter].config(
        state="disabled"
    )

    if letter in word:
        letter_buttons[letter].config(
            bg=CORRECT_COLOR,
            fg="white"
        )

        status_label.config(
            text="✅ Correct!",
            fg=CORRECT_COLOR
        )

    else:
        wrong_guesses += 1

        letter_buttons[letter].config(
            bg=WRONG_COLOR,
            fg="white"
        )

        status_label.config(
            text=f"❌ Wrong! {MAX_WRONG - wrong_guesses} attempts left",
            fg=WRONG_COLOR
        )

    attempts_label.config(
        text=f"❌ Wrong Attempts: {wrong_guesses} / {MAX_WRONG}"
    )

    update_display()
    update_hangman()

    if all(letter in guessed_letters for letter in word):
        game_over = True

        status_label.config(
            text="🏆 YOU WON!",
            fg=CORRECT_COLOR
        )

        disable_keyboard()

    elif wrong_guesses >= MAX_WRONG:
        game_over = True

        status_label.config(
            text=f"💀 GAME OVER! Word: {word}",
            fg=WRONG_COLOR
        )

        word_label.config(
            text=" ".join(word),
            fg=WRONG_COLOR
        )

        disable_keyboard()


def disable_keyboard():
    for button in letter_buttons.values():
        button.config(state="disabled")


def update_display():
    word_label.config(
        text=display_word()
    )


def update_hangman():
    canvas.delete("all")

    canvas.create_line(
        70, 300,
        250, 300,
        fill="#4C63D2",
        width=5
    )

    canvas.create_line(
        110, 300,
        110, 55,
        fill="#4C63D2",
        width=5
    )

    canvas.create_line(
        110, 55,
        230, 55,
        fill="#4C63D2",
        width=5
    )

    canvas.create_line(
        230, 55,
        230, 85,
        fill="#4C63D2",
        width=5
    )

    if wrong_guesses >= 1:
        canvas.create_oval(
            200, 85,
            260, 145,
            outline=LETTER_COLOR,
            width=5
        )

    if wrong_guesses >= 2:
        canvas.create_line(
            230, 145,
            230, 220,
            fill=LETTER_COLOR,
            width=5
        )

    if wrong_guesses >= 3:
        canvas.create_line(
            230, 160,
            190, 200,
            fill=LETTER_COLOR,
            width=5
        )

    if wrong_guesses >= 4:
        canvas.create_line(
            230, 160,
            270, 200,
            fill=LETTER_COLOR,
            width=5
        )

    if wrong_guesses >= 5:
        canvas.create_line(
            230, 220,
            195, 275,
            fill=LETTER_COLOR,
            width=5
        )

    if wrong_guesses >= 6:
        canvas.create_line(
            230, 220,
            265, 275,
            fill=WRONG_COLOR,
            width=5
        )


def button_enter(event, letter):
    if (
        not game_over
        and letter_buttons[letter]["state"] == "normal"
    ):
        letter_buttons[letter].config(
            bg=BUTTON_HOVER
        )


def button_leave(event, letter):
    if (
        not game_over
        and letter_buttons[letter]["state"] == "normal"
    ):
        letter_buttons[letter].config(
            bg=BUTTON_COLOR
        )


header_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

header_frame.pack(
    pady=(15, 3)
)


title_label = tk.Label(
    header_frame,
    text="✦ HANGMAN ✦",
    font=("Segoe UI", 27, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title_label.pack()


subtitle_label = tk.Label(
    header_frame,
    text="Guess the word • Don't get caught!",
    font=("Segoe UI", 11, "italic"),
    bg=BG_COLOR,
    fg=SUBTITLE_COLOR
)

subtitle_label.pack()


info_frame = tk.Frame(
    root,
    bg=PANEL_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=2
)

info_frame.pack(
    padx=60,
    pady=8,
    fill="x"
)


attempts_label = tk.Label(
    info_frame,
    text=f"❌ Wrong Attempts: 0 / {MAX_WRONG}",
    font=("Segoe UI", 12, "bold"),
    bg=PANEL_COLOR,
    fg=WRONG_COLOR
)

attempts_label.pack(
    pady=7
)


word_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 25, "bold"),
    bg=BG_COLOR,
    fg=LETTER_COLOR
)

word_label.pack(
    pady=7
)


status_label = tk.Label(
    root,
    text="💙 Guess the hidden word!",
    font=("Segoe UI", 14, "bold"),
    bg=BG_COLOR,
    fg=SUBTITLE_COLOR
)

status_label.pack(
    pady=3
)


hangman_frame = tk.Frame(
    root,
    bg=BOARD_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=2
)

hangman_frame.pack(
    padx=70,
    pady=7
)


canvas = tk.Canvas(
    hangman_frame,
    width=300,
    height=315,
    bg=BOARD_COLOR,
    highlightthickness=0
)

canvas.pack(
    padx=5,
    pady=5
)


keyboard_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

keyboard_frame.pack(
    pady=3
)


letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


for index, letter in enumerate(letters):

    button = tk.Button(
        keyboard_frame,
        text=letter,
        font=("Segoe UI", 10, "bold"),
        width=2,
        height=1,
        bg=BUTTON_COLOR,
        fg=TITLE_COLOR,
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda l=letter: guess_letter(l)
    )

    row = index // 9
    column = index % 9

    button.grid(
        row=row,
        column=column,
        padx=2,
        pady=2
    )

    button.bind(
        "<Enter>",
        lambda event, l=letter: button_enter(event, l)
    )

    button.bind(
        "<Leave>",
        lambda event, l=letter: button_leave(event, l)
    )

    letter_buttons[letter] = button


reset_button = tk.Button(
    root,
    text="🔄 NEW GAME",
    font=("Segoe UI", 13, "bold"),
    bg=RESET_COLOR,
    fg="white",
    activebackground=RESET_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=25,
    pady=7,
    command=start_game
)

reset_button.pack(
    pady=10
)


def reset_enter(event):
    reset_button.config(bg=RESET_HOVER)


def reset_leave(event):
    reset_button.config(bg=RESET_COLOR)


reset_button.bind("<Enter>", reset_enter)
reset_button.bind("<Leave>", reset_leave)


footer_label = tk.Label(
    root,
    text="✦ Good luck! ✦",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=TEXT_MUTED
)

footer_label.pack()


start_game()

root.mainloop()