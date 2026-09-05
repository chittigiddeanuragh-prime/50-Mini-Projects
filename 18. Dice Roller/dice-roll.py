import tkinter as tk
import random


def roll_dice():
    try:
        number = int(dice_entry.get())

        if number < 1 or number > 12:
            status_label.config(
                text="Choose between 1 and 12 dice.",
                fg="#FF6B6B"
            )
            return

        for widget in dice_frame.winfo_children():
            widget.destroy()

        rolls = [random.randint(1, 6) for _ in range(number)]
        total = sum(rolls)

        for i, value in enumerate(rolls):
            dice_box = tk.Frame(
                dice_frame,
                bg="#FFE66D",
                width=120,
                height=120,
                bd=3,
                relief="raised"
            )

            dice_box.grid(
                row=i // 4,
                column=i % 4,
                padx=15,
                pady=15
            )

            dice_box.grid_propagate(False)

            number_label = tk.Label(
                dice_box,
                text=str(value),
                font=("Arial", 42, "bold"),
                bg="#FFE66D",
                fg="#4B1D6B"
            )

            number_label.pack(
                expand=True
            )

            label = tk.Label(
                dice_frame,
                text=f"Dice {i + 1}",
                font=("Arial", 10, "bold"),
                bg="#2D174D",
                fg="#7DF9FF"
            )

            label.grid(
                row=(i // 4) * 2 + 1,
                column=i % 4,
                pady=(0, 8)
            )

        total_label.config(
            text=f"Total: {total}",
            fg="#7DF9FF"
        )

        status_label.config(
            text=f"You rolled {number} dice!",
            fg="#7DF9FF"
        )

    except ValueError:
        status_label.config(
            text="Please enter a valid number.",
            fg="#FF6B6B"
        )


def clear_dice():
    for widget in dice_frame.winfo_children():
        widget.destroy()

    total_label.config(
        text="Total: 0",
        fg="#FFE66D"
    )

    status_label.config(
        text="Ready to roll!",
        fg="#FFFFFF"
    )


def roll_with_enter(event):
    roll_dice()


root = tk.Tk()
root.title("Dice Rolling Simulator")
root.geometry("900x800")
root.minsize(700, 650)
root.resizable(True, True)
root.configure(bg="#2D174D")


title = tk.Label(
    root,
    text="Dice Rolling Simulator",
    font=("Arial", 32, "bold"),
    bg="#2D174D",
    fg="#FF7EB6"
)

title.pack(
    pady=(35, 5)
)


subtitle = tk.Label(
    root,
    text="Roll the dice and see what luck brings!",
    font=("Arial", 13),
    bg="#2D174D",
    fg="#7DF9FF"
)

subtitle.pack(
    pady=(0, 25)
)


main_frame = tk.Frame(
    root,
    bg="#3F2461",
    bd=2,
    relief="solid",
    highlightbackground="#FF7EB6",
    highlightthickness=2
)

main_frame.pack(
    padx=50,
    pady=10,
    fill="both",
    expand=True
)


control_label = tk.Label(
    main_frame,
    text="How many dice do you want to roll?",
    font=("Arial", 14, "bold"),
    bg="#3F2461",
    fg="#FFFFFF"
)

control_label.pack(
    pady=(30, 10)
)


dice_entry = tk.Entry(
    main_frame,
    font=("Arial", 17, "bold"),
    justify="center",
    bg="#211333",
    fg="#FFFFFF",
    insertbackground="#7DF9FF",
    relief="solid",
    bd=1,
    width=10
)

dice_entry.pack(
    ipady=9
)

dice_entry.insert(
    0,
    "2"
)

dice_entry.bind(
    "<Return>",
    roll_with_enter
)


button_frame = tk.Frame(
    main_frame,
    bg="#3F2461"
)

button_frame.pack(
    pady=25
)


roll_button = tk.Button(
    button_frame,
    text="ROLL DICE",
    font=("Arial", 13, "bold"),
    bg="#FF7EB6",
    fg="#2D174D",
    activebackground="#FF9DC8",
    activeforeground="#2D174D",
    relief="flat",
    cursor="hand2",
    command=roll_dice
)

roll_button.grid(
    row=0,
    column=0,
    padx=8,
    ipadx=35,
    ipady=10
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 13, "bold"),
    bg="#7DF9FF",
    fg="#2D174D",
    activebackground="#A7FCFF",
    activeforeground="#2D174D",
    relief="flat",
    cursor="hand2",
    command=clear_dice
)

clear_button.grid(
    row=0,
    column=1,
    padx=8,
    ipadx=35,
    ipady=10
)


dice_frame = tk.Frame(
    main_frame,
    bg="#2D174D"
)

dice_frame.pack(
    padx=30,
    pady=10,
    fill="both",
    expand=True
)


total_label = tk.Label(
    main_frame,
    text="Total: 0",
    font=("Arial", 22, "bold"),
    bg="#3F2461",
    fg="#FFE66D"
)

total_label.pack(
    pady=(15, 5)
)


status_label = tk.Label(
    main_frame,
    text="Ready to roll!",
    font=("Arial", 11),
    bg="#3F2461",
    fg="#FFFFFF"
)

status_label.pack(
    pady=(5, 20)
)


info_label = tk.Label(
    main_frame,
    text="You can roll between 1 and 12 dice.",
    font=("Arial", 10),
    bg="#3F2461",
    fg="#BFA9D8"
)

info_label.pack(
    pady=(0, 25)
)


root.mainloop()