import tkinter as tk
import random


words = [
    "python",
    "galaxy",
    "planet",
    "rocket",
    "computer",
    "keyboard",
    "internet",
    "science",
    "program",
    "developer",
    "algorithm",
    "database",
    "network",
    "software",
    "technology",
    "universe",
    "astronaut",
    "satellite",
    "javascript",
    "artificial"
]

current_word = ""
scrambled_word = ""
current_round = 0
score = 0
correct_answers = 0
wrong_answers = 0
streak = 0
best_streak = 0
hint_used = False
game_finished = False


def scramble_word(word):
    letters = list(word)

    while True:
        random.shuffle(letters)
        scrambled = "".join(letters)

        if scrambled != word:
            return scrambled


def start_game():
    global current_round, score, correct_answers
    global wrong_answers, streak, best_streak, game_finished

    current_round = 0
    score = 0
    correct_answers = 0
    wrong_answers = 0
    streak = 0
    best_streak = 0
    game_finished = False

    update_stats()
    load_next_word()


def load_next_word():
    global current_word, scrambled_word, hint_used

    if current_round >= 10:
        finish_game()
        return

    hint_used = False

    current_word = random.choice(words)
    scrambled_word = scramble_word(current_word)

    round_label.config(
        text=f"ROUND {current_round + 1} / 10"
    )

    word_label.config(
        text="  ".join(scrambled_word.upper())
    )

    answer_entry.config(
        state="normal"
    )

    answer_entry.delete(
        0,
        tk.END
    )

    answer_entry.focus()

    hint_label.config(
        text="Need help? Use the HINT button.",
        fg="#7C8DB5"
    )

    status_label.config(
        text="✦ Waiting for your answer...",
        fg="#8B9CCB"
    )

    submit_button.config(
        state="normal",
        bg="#171B35"
    )

    hint_button.config(
        state="normal",
        bg="#171B35"
    )

    skip_button.config(
        state="normal",
        bg="#171B35"
    )

    update_progress()


def submit_answer():
    global current_round, score, correct_answers
    global wrong_answers, streak, best_streak

    if game_finished:
        return

    answer = answer_entry.get().strip().lower()

    if not answer:
        status_label.config(
            text="✦ Enter an answer first.",
            fg="#FF5C8A"
        )
        return

    if answer == current_word:
        current_round += 1
        correct_answers += 1
        streak += 1

        if streak > best_streak:
            best_streak = streak

        points = 10

        if hint_used:
            points = 5

        streak_bonus = min(streak * 2, 10)
        score += points + streak_bonus

        status_label.config(
            text="✦ Correct! Excellent decoding.",
            fg="#5EF2C2"
        )

        hint_label.config(
            text=f"+{points + streak_bonus} points",
            fg="#C4A7FF"
        )

        update_stats()

        root.after(
            900,
            load_next_word
        )

    else:
        wrong_answers += 1
        streak = 0

        status_label.config(
            text="✦ Not quite. Try again.",
            fg="#FF5C8A"
        )

        update_stats()


def show_hint():
    global hint_used

    if hint_used:
        return

    hint_used = True

    first_letter = current_word[0].upper()
    last_letter = current_word[-1].upper()

    hint_label.config(
        text=f"Hint: Starts with {first_letter} and ends with {last_letter}",
        fg="#FFD166"
    )

    status_label.config(
        text="✦ Hint revealed. Correct answer is now worth fewer points.",
        fg="#FFD166"
    )


def skip_word():
    global current_round, wrong_answers, streak

    if game_finished:
        return

    wrong_answers += 1
    streak = 0
    current_round += 1

    status_label.config(
        text=f"✦ Skipped. The word was {current_word.upper()}.",
        fg="#FF8A80"
    )

    update_stats()

    root.after(
        1000,
        load_next_word
    )


def update_stats():
    score_label.config(
        text=f"SCORE\n{score}"
    )

    streak_label.config(
        text=f"STREAK\n{streak}"
    )

    correct_label.config(
        text=f"Correct: {correct_answers}"
    )

    wrong_label.config(
        text=f"Wrong: {wrong_answers}"
    )

    best_label.config(
        text=f"Best Streak: {best_streak}"
    )


def update_progress():
    progress_canvas.delete("all")

    total_width = 700
    segment_width = 60
    gap = 10

    for i in range(10):
        x1 = i * (segment_width + gap)
        x2 = x1 + segment_width

        if i < current_round:
            fill_color = "#6D5DFB"
        elif i == current_round:
            fill_color = "#00D9FF"
        else:
            fill_color = "#171B35"

        progress_canvas.create_rectangle(
            x1,
            2,
            x2,
            12,
            fill=fill_color,
            outline=""
        )


def finish_game():
    global game_finished

    game_finished = True

    word_label.config(
        text="MISSION COMPLETE"
    )

    round_label.config(
        text="FINAL RESULTS"
    )

    answer_entry.delete(
        0,
        tk.END
    )

    answer_entry.config(
        state="disabled"
    )

    submit_button.config(
        state="disabled",
        bg="#101329"
    )

    hint_button.config(
        state="disabled",
        bg="#101329"
    )

    skip_button.config(
        state="disabled",
        bg="#101329"
    )

    if score >= 150:
        message = "✦ COSMIC MASTER ✦"
        message_color = "#5EF2C2"
    elif score >= 100:
        message = "✦ GREAT EXPLORER ✦"
        message_color = "#00D9FF"
    elif score >= 60:
        message = "✦ NICE JOURNEY ✦"
        message_color = "#C4A7FF"
    else:
        message = "✦ KEEP EXPLORING ✦"
        message_color = "#FFD166"

    status_label.config(
        text=message,
        fg=message_color
    )

    hint_label.config(
        text=f"You scored {score} points across 10 cosmic words.",
        fg="#8B9CCB"
    )

    update_progress()


def enter_answer(event):
    submit_answer()


root = tk.Tk()

root.title("Word Scramble - Cosmic Edition")

root.geometry("1000x820")
root.minsize(800, 700)
root.resizable(True, True)

root.configure(
    bg="#080B18"
)


header = tk.Frame(
    root,
    bg="#080B18"
)

header.pack(
    fill="x",
    padx=50,
    pady=(25, 10)
)


title_label = tk.Label(
    header,
    text="WORD SCRAMBLE",
    font=("Arial", 32, "bold"),
    bg="#080B18",
    fg="#C4A7FF"
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="DECODE THE COSMIC WORD",
    font=("Arial", 11, "bold"),
    bg="#080B18",
    fg="#00D9FF"
)

subtitle_label.pack(
    pady=(4, 0)
)


main_frame = tk.Frame(
    root,
    bg="#101329",
    bd=1,
    relief="solid",
    highlightbackground="#24294A",
    highlightthickness=2
)

main_frame.pack(
    padx=45,
    pady=5,
    fill="both",
    expand=True
)


top_bar = tk.Frame(
    main_frame,
    bg="#101329"
)

top_bar.pack(
    fill="x",
    padx=35,
    pady=(25, 8)
)


round_label = tk.Label(
    top_bar,
    text="ROUND 1 / 10",
    font=("Arial", 12, "bold"),
    bg="#101329",
    fg="#00D9FF"
)

round_label.pack(
    side="left"
)


score_label = tk.Label(
    top_bar,
    text="SCORE\n0",
    font=("Arial", 11, "bold"),
    bg="#101329",
    fg="#FFD166",
    justify="center"
)

score_label.pack(
    side="right",
    padx=20
)


streak_label = tk.Label(
    top_bar,
    text="STREAK\n0",
    font=("Arial", 11, "bold"),
    bg="#101329",
    fg="#FF5C8A",
    justify="center"
)

streak_label.pack(
    side="right",
    padx=20
)


progress_canvas = tk.Canvas(
    main_frame,
    height=14,
    width=700,
    bg="#0B0E20",
    highlightthickness=0
)

progress_canvas.pack(
    padx=35,
    pady=(5, 30),
    fill="x"
)


word_card = tk.Frame(
    main_frame,
    bg="#151A36",
    bd=1,
    relief="solid",
    highlightbackground="#302B59",
    highlightthickness=1
)

word_card.pack(
    padx=70,
    fill="x",
    pady=5
)


word_title = tk.Label(
    word_card,
    text="UNSCRAMBLE THIS",
    font=("Arial", 11, "bold"),
    bg="#151A36",
    fg="#7C8DB5"
)

word_title.pack(
    pady=(22, 8)
)


word_label = tk.Label(
    word_card,
    text="P Y T H O N",
    font=("Arial", 27, "bold"),
    bg="#151A36",
    fg="#00D9FF"
)

word_label.pack(
    pady=(5, 25)
)


answer_title = tk.Label(
    main_frame,
    text="YOUR ANSWER",
    font=("Arial", 11, "bold"),
    bg="#101329",
    fg="#8B9CCB"
)

answer_title.pack(
    pady=(22, 8)
)


answer_entry = tk.Entry(
    main_frame,
    font=("Arial", 18, "bold"),
    justify="center",
    bg="#080B18",
    fg="#F4F7FF",
    insertbackground="#00D9FF",
    relief="solid",
    bd=1,
    width=25
)

answer_entry.pack(
    ipady=9
)


button_frame = tk.Frame(
    main_frame,
    bg="#101329"
)

button_frame.pack(
    pady=20
)


submit_button = tk.Button(
    button_frame,
    text="SUBMIT",
    font=("Arial", 11, "bold"),
    bg="#171B35",
    fg="#5EF2C2",
    activebackground="#20264A",
    activeforeground="#5EF2C2",
    relief="solid",
    bd=1,
    cursor="hand2",
    command=submit_answer
)

submit_button.grid(
    row=0,
    column=0,
    padx=6,
    ipadx=25,
    ipady=9
)


hint_button = tk.Button(
    button_frame,
    text="HINT",
    font=("Arial", 11, "bold"),
    bg="#171B35",
    fg="#FFD166",
    activebackground="#20264A",
    activeforeground="#FFD166",
    relief="solid",
    bd=1,
    cursor="hand2",
    command=show_hint
)

hint_button.grid(
    row=0,
    column=1,
    padx=6,
    ipadx=27,
    ipady=9
)


skip_button = tk.Button(
    button_frame,
    text="SKIP",
    font=("Arial", 11, "bold"),
    bg="#171B35",
    fg="#FF8A80",
    activebackground="#20264A",
    activeforeground="#FF8A80",
    relief="solid",
    bd=1,
    cursor="hand2",
    command=skip_word
)

skip_button.grid(
    row=0,
    column=2,
    padx=6,
    ipadx=27,
    ipady=9
)


status_label = tk.Label(
    main_frame,
    text="✦ Waiting for your answer...",
    font=("Arial", 11, "bold"),
    bg="#101329",
    fg="#8B9CCB"
)

status_label.pack(
    pady=(5, 4)
)


hint_label = tk.Label(
    main_frame,
    text="Need help? Use the HINT button.",
    font=("Arial", 10),
    bg="#101329",
    fg="#7C8DB5"
)

hint_label.pack(
    pady=(0, 15)
)


stats_frame = tk.Frame(
    main_frame,
    bg="#0B0E20",
    bd=1,
    relief="solid"
)

stats_frame.pack(
    fill="x",
    padx=45,
    pady=(5, 20)
)


correct_label = tk.Label(
    stats_frame,
    text="Correct: 0",
    font=("Arial", 10, "bold"),
    bg="#0B0E20",
    fg="#5EF2C2"
)

correct_label.pack(
    side="left",
    padx=30,
    pady=13
)


wrong_label = tk.Label(
    stats_frame,
    text="Wrong: 0",
    font=("Arial", 10, "bold"),
    bg="#0B0E20",
    fg="#FF5C8A"
)

wrong_label.pack(
    side="left",
    padx=30,
    pady=13
)


best_label = tk.Label(
    stats_frame,
    text="Best Streak: 0",
    font=("Arial", 10, "bold"),
    bg="#0B0E20",
    fg="#C4A7FF"
)

best_label.pack(
    side="right",
    padx=30,
    pady=13
)


new_game_button = tk.Button(
    root,
    text="START NEW GAME",
    font=("Arial", 11, "bold"),
    bg="#171B35",
    fg="#C4A7FF",
    activebackground="#24294A",
    activeforeground="#FFFFFF",
    relief="solid",
    bd=1,
    cursor="hand2",
    command=start_game
)

new_game_button.pack(
    pady=(5, 18),
    ipadx=30,
    ipady=8
)


answer_entry.bind(
    "<Return>",
    enter_answer
)


start_game()

root.mainloop()