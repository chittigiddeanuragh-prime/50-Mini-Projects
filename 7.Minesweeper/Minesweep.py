import tkinter as tk
import random


BG_COLOR = "#0B1026"
PANEL_COLOR = "#151D3A"
CELL_COLOR = "#26345F"
CELL_HOVER = "#394A82"
REVEALED_COLOR = "#121A34"

TEXT_COLOR = "#F5F7FF"
ACCENT_COLOR = "#38BDF8"
FLAG_COLOR = "#FF4FD8"
MINE_COLOR = "#FF4757"
WIN_COLOR = "#22C55E"
RESET_COLOR = "#7C3AED"
RESET_HOVER = "#9F67FF"


ROWS = 10
COLS = 10
MINES = 15


root = tk.Tk()
root.title("Minesweeper")
root.geometry("600x720")
root.resizable(False, False)
root.configure(bg=BG_COLOR)


board = []
buttons = []
revealed = set()
flags = set()

game_over = False


def create_board():
    global board

    board = [
        [0 for _ in range(COLS)]
        for _ in range(ROWS)
    ]

    mine_positions = random.sample(
        range(ROWS * COLS),
        MINES
    )

    for position in mine_positions:
        row = position // COLS
        col = position % COLS
        board[row][col] = -1

    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] == -1:
                continue

            count = 0

            for row_offset in [-1, 0, 1]:
                for col_offset in [-1, 0, 1]:

                    new_row = row + row_offset
                    new_col = col + col_offset

                    if (
                        0 <= new_row < ROWS
                        and 0 <= new_col < COLS
                        and board[new_row][new_col] == -1
                    ):
                        count += 1

            board[row][col] = count


def create_buttons():

    global buttons

    buttons = []

    for row in range(ROWS):

        button_row = []

        for col in range(COLS):

            button = tk.Button(
                board_frame,
                text="",
                font=("Segoe UI", 11, "bold"),
                width=3,
                height=1,
                bg=CELL_COLOR,
                fg=TEXT_COLOR,
                activebackground=CELL_HOVER,
                activeforeground=TEXT_COLOR,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda r=row, c=col: reveal_cell(r, c)
            )

            button.grid(
                row=row,
                column=col,
                padx=2,
                pady=2
            )

            button.bind(
                "<Enter>",
                lambda event, r=row, c=col: cell_enter(r, c)
            )

            button.bind(
                "<Leave>",
                lambda event, r=row, c=col: cell_leave(r, c)
            )

            button.bind(
                "<Button-3>",
                lambda event, r=row, c=col: toggle_flag(r, c)
            )

            button_row.append(button)

        buttons.append(button_row)


def cell_enter(row, col):

    if (
        not game_over
        and (row, col) not in revealed
        and (row, col) not in flags
    ):
        buttons[row][col].config(
            bg=CELL_HOVER
        )


def cell_leave(row, col):

    if (
        not game_over
        and (row, col) not in revealed
        and (row, col) not in flags
    ):
        buttons[row][col].config(
            bg=CELL_COLOR
        )


def toggle_flag(row, col):

    if game_over:
        return

    if (row, col) in revealed:
        return

    if (row, col) in flags:

        flags.remove((row, col))

        buttons[row][col].config(
            text="",
            bg=CELL_COLOR,
            fg=TEXT_COLOR
        )

    else:

        if len(flags) >= MINES:
            status_label.config(
                text="⚠ Maximum flags reached!",
                fg="#FFD166"
            )
            return

        flags.add((row, col))

        buttons[row][col].config(
            text="⚑",
            bg=FLAG_COLOR,
            fg="white"
        )

    update_mine_counter()


def reveal_cell(row, col):

    global game_over

    if game_over:
        return

    if (row, col) in revealed:
        return

    if (row, col) in flags:
        return

    if board[row][col] == -1:

        reveal_all_mines()

        buttons[row][col].config(
            text="💣",
            bg=MINE_COLOR,
            fg="white"
        )

        game_over = True

        status_label.config(
            text="💥 BOOM! YOU HIT A MINE!",
            fg=MINE_COLOR
        )

        return

    reveal_area(row, col)

    if check_win():

        game_over = True

        status_label.config(
            text="🏆 YOU CLEARED THE BOARD!",
            fg=WIN_COLOR
        )


def reveal_area(row, col):

    if (
        row < 0
        or row >= ROWS
        or col < 0
        or col >= COLS
        or (row, col) in revealed
        or (row, col) in flags
        or board[row][col] == -1
    ):
        return

    revealed.add((row, col))

    number = board[row][col]

    buttons[row][col].config(
        bg=REVEALED_COLOR,
        relief="sunken",
        cursor="arrow"
    )

    if number == 0:

        buttons[row][col].config(
            text=""
        )

        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:

                if row_offset == 0 and col_offset == 0:
                    continue

                reveal_area(
                    row + row_offset,
                    col + col_offset
                )

    else:

        number_colors = {
            1: "#38BDF8",
            2: "#22C55E",
            3: "#FF6B6B",
            4: "#A78BFA",
            5: "#FF8FAB",
            6: "#22D3EE",
            7: "#FFFFFF",
            8: "#94A3B8"
        }

        buttons[row][col].config(
            text=str(number),
            fg=number_colors.get(
                number,
                TEXT_COLOR
            )
        )


def reveal_all_mines():

    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] == -1:

                buttons[row][col].config(
                    text="💣",
                    bg=MINE_COLOR,
                    fg="white"
                )


def check_win():

    safe_cells = ROWS * COLS - MINES

    return len(revealed) == safe_cells


def update_mine_counter():

    remaining = MINES - len(flags)

    mine_label.config(
        text=f"💣 Mines: {remaining}"
    )


def reset_game():

    global revealed
    global flags
    global game_over

    revealed = set()
    flags = set()
    game_over = False

    create_board()

    for row in range(ROWS):
        for col in range(COLS):

            buttons[row][col].config(
                text="",
                bg=CELL_COLOR,
                fg=TEXT_COLOR,
                relief="flat",
                cursor="hand2"
            )

    update_mine_counter()

    status_label.config(
        text="💙 Find all the safe cells!",
        fg=ACCENT_COLOR
    )


header_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

header_frame.pack(
    pady=(18, 5)
)


title_label = tk.Label(
    header_frame,
    text="✦ MINESWEEPER ✦",
    font=("Segoe UI", 27, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

title_label.pack()


subtitle_label = tk.Label(
    header_frame,
    text="Clear the board • Avoid the mines",
    font=("Segoe UI", 11, "italic"),
    bg=BG_COLOR,
    fg="#7DD3FC"
)

subtitle_label.pack(
    pady=(2, 0)
)


info_frame = tk.Frame(
    root,
    bg=PANEL_COLOR,
    highlightbackground="#4C63D2",
    highlightthickness=2
)

info_frame.pack(
    padx=70,
    pady=10,
    fill="x"
)


mine_label = tk.Label(
    info_frame,
    text=f"💣 Mines: {MINES}",
    font=("Segoe UI", 13, "bold"),
    bg=PANEL_COLOR,
    fg="#FF6B9D"
)

mine_label.pack(
    side="left",
    padx=20,
    pady=8
)


instruction_label = tk.Label(
    info_frame,
    text="Left: Reveal  |  Right: Flag",
    font=("Segoe UI", 10),
    bg=PANEL_COLOR,
    fg="#A9B7FF"
)

instruction_label.pack(
    side="right",
    padx=15,
    pady=8
)


status_label = tk.Label(
    root,
    text="💙 Find all the safe cells!",
    font=("Segoe UI", 15, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)

status_label.pack(
    pady=(3, 8)
)


board_frame = tk.Frame(
    root,
    bg="#080D20",
    highlightbackground="#4C63D2",
    highlightthickness=3
)

board_frame.pack(
    padx=20,
    pady=3
)


create_board()
create_buttons()


reset_button = tk.Button(
    root,
    text="🔄  NEW GAME",
    font=("Segoe UI", 14, "bold"),
    bg=RESET_COLOR,
    fg="white",
    activebackground=RESET_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=30,
    pady=8,
    command=reset_game
)

reset_button.pack(
    pady=15
)


def reset_enter(event):
    reset_button.config(
        bg=RESET_HOVER
    )


def reset_leave(event):
    reset_button.config(
        bg=RESET_COLOR
    )


reset_button.bind(
    "<Enter>",
    reset_enter
)

reset_button.bind(
    "<Leave>",
    reset_leave
)


footer_label = tk.Label(
    root,
    text="✦ Good luck, explorer! ✦",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg="#6975A8"
)

footer_label.pack(
    pady=(0, 5)
)


root.mainloop()