import tkinter as tk


BG_COLOR = "#0D1028"
PANEL_COLOR = "#1A1F4A"
BOARD_COLOR = "#101735"

TITLE_COLOR = "#F8FAFF"
SUBTITLE_COLOR = "#7DD3FC"

X_COLOR = "#38BDF8"
O_COLOR = "#FF5ACD"

BUTTON_COLOR = "#24316B"
BUTTON_HOVER = "#3B4FA1"

RESET_COLOR = "#7C3AED"
RESET_HOVER = "#9F67FF"

BORDER_COLOR = "#4C63D2"
WIN_COLOR = "#22C55E"
STATUS_COLOR = "#FFD166"


root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("650x780")
root.resizable(False, False)
root.configure(bg=BG_COLOR)


current_player = "X"
game_over = False

x_score = 0
o_score = 0
draw_score = 0

buttons = []

winning_combinations = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]


def check_winner():
    for a, b, c in winning_combinations:
        if (
            buttons[a]["text"] != ""
            and buttons[a]["text"] == buttons[b]["text"]
            and buttons[a]["text"] == buttons[c]["text"]
        ):
            return (a, b, c)

    return None


def check_draw():
    for button in buttons:
        if button["text"] == "":
            return False

    return True


def update_status():
    if current_player == "X":
        status_label.config(
            text="💙 PLAYER X'S TURN",
            fg=X_COLOR
        )
    else:
        status_label.config(
            text="💖 PLAYER O'S TURN",
            fg=O_COLOR
        )


def update_score():
    score_label.config(
        text=f"X  {x_score}     •     DRAW  {draw_score}     •     O  {o_score}"
    )


def button_enter(index):
    if buttons[index]["text"] == "" and not game_over:
        buttons[index].config(bg=BUTTON_HOVER)


def button_leave(index):
    if buttons[index]["text"] == "" and not game_over:
        buttons[index].config(bg=BUTTON_COLOR)


def button_click(index):
    global current_player
    global game_over
    global x_score
    global o_score
    global draw_score

    if game_over:
        return

    if buttons[index]["text"] != "":
        return

    buttons[index].config(text=current_player)

    if current_player == "X":
        buttons[index].config(fg=X_COLOR)
    else:
        buttons[index].config(fg=O_COLOR)

    winner = check_winner()

    if winner:
        game_over = True

        if current_player == "X":
            x_score += 1
        else:
            o_score += 1

        update_score()

        for position in winner:
            buttons[position].config(
                bg=WIN_COLOR,
                fg="white"
            )

        status_label.config(
            text=f"🏆 PLAYER {current_player} WINS!",
            fg=STATUS_COLOR
        )

        return

    if check_draw():
        game_over = True
        draw_score += 1

        update_score()

        status_label.config(
            text="🤝 IT'S A DRAW!",
            fg=SUBTITLE_COLOR
        )

        return

    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

    update_status()


def reset_game():
    global current_player
    global game_over

    current_player = "X"
    game_over = False

    for button in buttons:
        button.config(
            text="",
            bg=BUTTON_COLOR,
            fg=TITLE_COLOR
        )

    update_status()


header_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

header_frame.pack(
    pady=(20, 5)
)


title_label = tk.Label(
    header_frame,
    text="✦ TIC TAC TOE ✦",
    font=("Segoe UI", 28, "bold"),
    bg=BG_COLOR,
    fg=TITLE_COLOR
)

title_label.pack()


subtitle_label = tk.Label(
    header_frame,
    text="Neon Edition • X vs O",
    font=("Segoe UI", 12, "italic"),
    bg=BG_COLOR,
    fg=SUBTITLE_COLOR
)

subtitle_label.pack(
    pady=(3, 0)
)


score_frame = tk.Frame(
    root,
    bg=PANEL_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=2
)

score_frame.pack(
    padx=70,
    pady=12,
    fill="x"
)


score_label = tk.Label(
    score_frame,
    text="X  0     •     DRAW  0     •     O  0",
    font=("Segoe UI", 16, "bold"),
    bg=PANEL_COLOR,
    fg=TITLE_COLOR
)

score_label.pack(
    pady=12
)


status_label = tk.Label(
    root,
    text="💙 PLAYER X'S TURN",
    font=("Segoe UI", 19, "bold"),
    bg=BG_COLOR,
    fg=X_COLOR
)

status_label.pack(
    pady=(5, 10)
)


board_frame = tk.Frame(
    root,
    bg=BOARD_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=3
)

board_frame.pack(
    padx=30,
    pady=5
)


for i in range(9):

    button = tk.Button(
        board_frame,
        text="",
        font=("Segoe UI", 30, "bold"),
        width=4,
        height=1,
        bg=BUTTON_COLOR,
        fg=TITLE_COLOR,
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda index=i: button_click(index)
    )

    button.grid(
        row=i // 3,
        column=i % 3,
        padx=4,
        pady=4
    )

    button.bind(
        "<Enter>",
        lambda event, index=i: button_enter(index)
    )

    button.bind(
        "<Leave>",
        lambda event, index=i: button_leave(index)
    )

    buttons.append(button)


reset_button = tk.Button(
    root,
    text="🎮  NEW GAME",
    font=("Segoe UI", 16, "bold"),
    bg=RESET_COLOR,
    fg="white",
    activebackground=RESET_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=35,
    pady=10,
    command=reset_game
)

reset_button.pack(
    pady=18
)


def reset_enter(event):
    reset_button.config(bg=RESET_HOVER)


def reset_leave(event):
    reset_button.config(bg=RESET_COLOR)


reset_button.bind("<Enter>", reset_enter)
reset_button.bind("<Leave>", reset_leave)


footer_label = tk.Label(
    root,
    text="✦ Choose your move wisely • May the best player win ✦",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg="#6975A8"
)

footer_label.pack(
    pady=(0, 8)
)


root.mainloop()