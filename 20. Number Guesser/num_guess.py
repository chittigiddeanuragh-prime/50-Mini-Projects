import tkinter as tk
import random


def start_game():
    global secret_number, attempts, max_attempts, game_over

    difficulty = difficulty_var.get()

    if difficulty == "Easy":
        secret_number = random.randint(1, 50)
        max_attempts = 10
        upper_limit = 50
    elif difficulty == "Medium":
        secret_number = random.randint(1, 100)
        max_attempts = 8
        upper_limit = 100
    else:
        secret_number = random.randint(1, 500)
        max_attempts = 7
        upper_limit = 500

    attempts = 0
    game_over = False

    guess_entry.config(state="normal")
    guess_button.config(state="normal")

    guess_entry.delete(0, tk.END)
    guess_entry.focus()

    range_label.config(
        text=f"Guess a number between 1 and {upper_limit}"
    )

    attempts_label.config(
        text=f"Attempts: 0 / {max_attempts}"
    )

    score_label.config(
        text="Score: 0"
    )

    hint_label.config(
        text="Make your first guess!",
        fg="#38BDF8"
    )

    result_label.config(
        text="Good luck!",
        fg="#F8FAFC"
    )


def check_guess():
    global attempts, game_over

    if game_over:
        return

    try:
        guess = int(guess_entry.get())
    except ValueError:
        hint_label.config(
            text="Please enter a valid whole number.",
            fg="#FF5C5C"
        )
        return

    difficulty = difficulty_var.get()

    if difficulty == "Easy":
        upper_limit = 50
    elif difficulty == "Medium":
        upper_limit = 100
    else:
        upper_limit = 500

    if guess < 1 or guess > upper_limit:
        hint_label.config(
            text=f"Enter a number from 1 to {upper_limit}.",
            fg="#FF5C5C"
        )
        return

    attempts += 1

    attempts_label.config(
        text=f"Attempts: {attempts} / {max_attempts}"
    )

    if guess == secret_number:

        score = max(100 - ((attempts - 1) * 10), 20)

        if difficulty == "Easy":
            score += 20
        elif difficulty == "Medium":
            score += 40
        else:
            score += 60

        score_label.config(
            text=f"Score: {score}"
        )

        hint_label.config(
            text="Correct! You found the number!",
            fg="#22C55E"
        )

        result_label.config(
            text=f"The number was {secret_number}",
            fg="#FFD166"
        )

        game_over = True

        guess_button.config(
            state="disabled"
        )

        guess_entry.config(
            state="disabled"
        )

        return

    if guess < secret_number:
        hint_label.config(
            text="Too low! Try a higher number.",
            fg="#38BDF8"
        )
    else:
        hint_label.config(
            text="Too high! Try a lower number.",
            fg="#FF9F43"
        )

    if attempts >= max_attempts:

        hint_label.config(
            text="Game Over! No attempts left.",
            fg="#FF5C5C"
        )

        result_label.config(
            text=f"The number was {secret_number}",
            fg="#FFD166"
        )

        score_label.config(
            text="Score: 0"
        )

        game_over = True

        guess_button.config(
            state="disabled"
        )

        guess_entry.config(
            state="disabled"
        )


def clear_guess():
    guess_entry.delete(0, tk.END)
    guess_entry.focus()


def enter_guess(event):
    check_guess()


root = tk.Tk()

root.title("Number Guessing Game")

root.geometry("900x760")

root.minsize(750, 650)

root.resizable(True, True)

root.configure(
    bg="#111827"
)


title_label = tk.Label(
    root,
    text="NUMBER GUESSING GAME",
    font=("Arial", 30, "bold"),
    bg="#111827",
    fg="#FBBF24"
)

title_label.pack(
    pady=(25, 3)
)


subtitle_label = tk.Label(
    root,
    text="Guess the hidden number before you run out of attempts!",
    font=("Arial", 12),
    bg="#111827",
    fg="#9CA3AF"
)

subtitle_label.pack(
    pady=(0, 12)
)


main_frame = tk.Frame(
    root,
    bg="#1F2937",
    bd=2,
    relief="solid",
    highlightbackground="#6366F1",
    highlightthickness=2
)

main_frame.pack(
    padx=40,
    pady=5,
    fill="both",
    expand=True
)


difficulty_title = tk.Label(
    main_frame,
    text="Choose Difficulty",
    font=("Arial", 14, "bold"),
    bg="#1F2937",
    fg="#F8FAFC"
)

difficulty_title.pack(
    pady=(18, 5)
)


difficulty_var = tk.StringVar(
    value="Medium"
)


difficulty_menu = tk.OptionMenu(
    main_frame,
    difficulty_var,
    "Easy",
    "Medium",
    "Hard"
)

difficulty_menu.config(
    font=("Arial", 11, "bold"),
    bg="#6366F1",
    fg="#FFFFFF",
    activebackground="#818CF8",
    activeforeground="#FFFFFF",
    relief="flat",
    width=14
)

difficulty_menu["menu"].config(
    font=("Arial", 10),
    bg="#FFFFFF",
    fg="#111827"
)

difficulty_menu.pack()


range_label = tk.Label(
    main_frame,
    text="Guess a number between 1 and 100",
    font=("Arial", 12, "bold"),
    bg="#1F2937",
    fg="#38BDF8"
)

range_label.pack(
    pady=(10, 12)
)


guess_entry = tk.Entry(
    main_frame,
    font=("Arial", 20, "bold"),
    justify="center",
    bg="#111827",
    fg="#FFFFFF",
    insertbackground="#FBBF24",
    relief="solid",
    bd=2,
    width=11
)

guess_entry.pack(
    ipady=7
)


button_frame = tk.Frame(
    main_frame,
    bg="#1F2937"
)

button_frame.pack(
    pady=13
)


guess_button = tk.Button(
    button_frame,
    text="GUESS",
    font=("Arial", 11, "bold"),
    bg="#22C55E",
    fg="#FFFFFF",
    activebackground="#16A34A",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=check_guess
)

guess_button.grid(
    row=0,
    column=0,
    padx=5,
    ipadx=28,
    ipady=8
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 11, "bold"),
    bg="#F97316",
    fg="#FFFFFF",
    activebackground="#EA580C",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=clear_guess
)

clear_button.grid(
    row=0,
    column=1,
    padx=5,
    ipadx=25,
    ipady=8
)


new_game_button = tk.Button(
    button_frame,
    text="NEW GAME",
    font=("Arial", 11, "bold"),
    bg="#8B5CF6",
    fg="#FFFFFF",
    activebackground="#7C3AED",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=start_game
)

new_game_button.grid(
    row=0,
    column=2,
    padx=5,
    ipadx=20,
    ipady=8
)


stats_frame = tk.Frame(
    main_frame,
    bg="#1F2937"
)

stats_frame.pack(
    padx=35,
    pady=5,
    fill="x"
)


attempts_card = tk.Frame(
    stats_frame,
    bg="#243447",
    bd=1,
    relief="solid"
)

attempts_card.grid(
    row=0,
    column=0,
    padx=7,
    sticky="nsew"
)


attempts_label = tk.Label(
    attempts_card,
    text="Attempts: 0 / 8",
    font=("Arial", 14, "bold"),
    bg="#243447",
    fg="#38BDF8"
)

attempts_label.pack(
    pady=14
)


score_card = tk.Frame(
    stats_frame,
    bg="#243447",
    bd=1,
    relief="solid"
)

score_card.grid(
    row=0,
    column=1,
    padx=7,
    sticky="nsew"
)


score_label = tk.Label(
    score_card,
    text="Score: 0",
    font=("Arial", 14, "bold"),
    bg="#243447",
    fg="#FBBF24"
)

score_label.pack(
    pady=14
)


stats_frame.columnconfigure(
    0,
    weight=1
)

stats_frame.columnconfigure(
    1,
    weight=1
)


hint_label = tk.Label(
    main_frame,
    text="Make your first guess!",
    font=("Arial", 16, "bold"),
    bg="#1F2937",
    fg="#38BDF8",
    wraplength=700
)

hint_label.pack(
    pady=(14, 5)
)


result_label = tk.Label(
    main_frame,
    text="Good luck!",
    font=("Arial", 13, "bold"),
    bg="#1F2937",
    fg="#F8FAFC"
)

result_label.pack(
    pady=5
)


info_frame = tk.Frame(
    main_frame,
    bg="#172033",
    bd=1,
    relief="solid"
)

info_frame.pack(
    padx=30,
    pady=(15, 18),
    fill="x"
)


info_label = tk.Label(
    info_frame,
    text="Easy: 1–50    |    Medium: 1–100    |    Hard: 1–500\n"
         "Use the hints to find the hidden number.",
    font=("Arial", 10),
    bg="#172033",
    fg="#CBD5E1",
    justify="center"
)

info_label.pack(
    pady=12
)


guess_entry.bind(
    "<Return>",
    enter_guess
)


start_game()

root.mainloop()