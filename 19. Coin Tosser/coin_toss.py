import tkinter as tk
import random


def toss_coins():
    try:
        flips = int(flips_entry.get())

        if flips < 1 or flips > 100000:
            status_label.config(
                text="Enter a number between 1 and 100,000.",
                fg="#FF6B6B"
            )
            return

        heads = 0
        tails = 0

        for _ in range(flips):
            if random.choice(["Heads", "Tails"]) == "Heads":
                heads += 1
            else:
                tails += 1

        heads_percentage = (heads / flips) * 100
        tails_percentage = (tails / flips) * 100

        heads_label.config(
            text=f"{heads:,}",
            fg="#7FFFD4"
        )

        tails_label.config(
            text=f"{tails:,}",
            fg="#FF8A80"
        )

        heads_percent_label.config(
            text=f"{heads_percentage:.2f}%"
        )

        tails_percent_label.config(
            text=f"{tails_percentage:.2f}%"
        )

        total_label.config(
            text=f"Total Flips: {flips:,}"
        )

        update_chart(
            heads_percentage,
            tails_percentage
        )

        status_label.config(
            text=f"Simulation completed with {flips:,} flips!",
            fg="#7FFFD4"
        )

    except ValueError:
        status_label.config(
            text="Please enter a valid whole number.",
            fg="#FF6B6B"
        )


def update_chart(heads_percentage, tails_percentage):
    chart.delete("all")

    chart_width = 500
    chart_height = 260

    margin_left = 70
    margin_right = 40
    margin_top = 30
    margin_bottom = 50

    available_height = chart_height - margin_top - margin_bottom

    heads_height = (
        available_height * heads_percentage / 100
    )

    tails_height = (
        available_height * tails_percentage / 100
    )

    heads_x1 = 120
    heads_x2 = 250
    heads_y1 = chart_height - margin_bottom - heads_height
    heads_y2 = chart_height - margin_bottom

    tails_x1 = 300
    tails_x2 = 430
    tails_y1 = chart_height - margin_bottom - tails_height
    tails_y2 = chart_height - margin_bottom

    chart.create_rectangle(
        heads_x1,
        heads_y1,
        heads_x2,
        heads_y2,
        fill="#2EC4B6",
        outline=""
    )

    chart.create_rectangle(
        tails_x1,
        tails_y1,
        tails_x2,
        tails_y2,
        fill="#FF6B6B",
        outline=""
    )

    chart.create_text(
        (heads_x1 + heads_x2) / 2,
        heads_y1 - 15,
        text=f"{heads_percentage:.1f}%",
        fill="#7FFFD4",
        font=("Arial", 12, "bold")
    )

    chart.create_text(
        (tails_x1 + tails_x2) / 2,
        tails_y1 - 15,
        text=f"{tails_percentage:.1f}%",
        fill="#FF8A80",
        font=("Arial", 12, "bold")
    )

    chart.create_text(
        (heads_x1 + heads_x2) / 2,
        chart_height - 25,
        text="Heads",
        fill="#FFFFFF",
        font=("Arial", 11, "bold")
    )

    chart.create_text(
        (tails_x1 + tails_x2) / 2,
        chart_height - 25,
        text="Tails",
        fill="#FFFFFF",
        font=("Arial", 11, "bold")
    )


def clear_results():
    flips_entry.delete(0, tk.END)

    heads_label.config(
        text="0"
    )

    tails_label.config(
        text="0"
    )

    heads_percent_label.config(
        text="0%"
    )

    tails_percent_label.config(
        text="0%"
    )

    total_label.config(
        text="Total Flips: 0"
    )

    chart.delete("all")

    status_label.config(
        text="Ready to toss!",
        fg="#FFFFFF"
    )


def toss_with_enter(event):
    toss_coins()


root = tk.Tk()
root.title("Coin Toss Simulator")
root.geometry("950x850")
root.minsize(750, 700)
root.resizable(True, True)
root.configure(bg="#101B2D")


title = tk.Label(
    root,
    text="Coin Toss Simulator",
    font=("Arial", 34, "bold"),
    bg="#101B2D",
    fg="#FFD166"
)

title.pack(
    pady=(35, 5)
)


subtitle = tk.Label(
    root,
    text="Simulate hundreds or thousands of coin flips",
    font=("Arial", 13),
    bg="#101B2D",
    fg="#A8DADC"
)

subtitle.pack(
    pady=(0, 25)
)


main_frame = tk.Frame(
    root,
    bg="#1B2A41",
    bd=2,
    relief="solid",
    highlightbackground="#2EC4B6",
    highlightthickness=2
)

main_frame.pack(
    padx=50,
    pady=10,
    fill="both",
    expand=True
)


input_label = tk.Label(
    main_frame,
    text="Number of Coin Flips",
    font=("Arial", 14, "bold"),
    bg="#1B2A41",
    fg="#FFFFFF"
)

input_label.pack(
    pady=(30, 10)
)


flips_entry = tk.Entry(
    main_frame,
    font=("Arial", 17, "bold"),
    justify="center",
    bg="#0B1424",
    fg="#FFFFFF",
    insertbackground="#FFD166",
    relief="solid",
    bd=1,
    width=18
)

flips_entry.pack(
    ipady=10
)

flips_entry.insert(
    0,
    "1000"
)

flips_entry.bind(
    "<Return>",
    toss_with_enter
)


button_frame = tk.Frame(
    main_frame,
    bg="#1B2A41"
)

button_frame.pack(
    pady=22
)


toss_button = tk.Button(
    button_frame,
    text="TOSS COINS",
    font=("Arial", 12, "bold"),
    bg="#2EC4B6",
    fg="#101B2D",
    activebackground="#52D8C8",
    activeforeground="#101B2D",
    relief="flat",
    cursor="hand2",
    command=toss_coins
)

toss_button.grid(
    row=0,
    column=0,
    padx=8,
    ipadx=35,
    ipady=10
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 12, "bold"),
    bg="#FF6B6B",
    fg="#FFFFFF",
    activebackground="#FF8585",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=clear_results
)

clear_button.grid(
    row=0,
    column=1,
    padx=8,
    ipadx=35,
    ipady=10
)


results_frame = tk.Frame(
    main_frame,
    bg="#1B2A41"
)

results_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


heads_card = tk.Frame(
    results_frame,
    bg="#243B53",
    bd=1,
    relief="solid"
)

heads_card.grid(
    row=0,
    column=0,
    padx=10,
    sticky="nsew"
)


heads_title = tk.Label(
    heads_card,
    text="HEADS",
    font=("Arial", 12, "bold"),
    bg="#243B53",
    fg="#7FFFD4"
)

heads_title.pack(
    pady=(15, 5)
)


heads_label = tk.Label(
    heads_card,
    text="0",
    font=("Arial", 26, "bold"),
    bg="#243B53",
    fg="#7FFFD4"
)

heads_label.pack()


heads_percent_label = tk.Label(
    heads_card,
    text="0%",
    font=("Arial", 11),
    bg="#243B53",
    fg="#FFFFFF"
)

heads_percent_label.pack(
    pady=(3, 15)
)


tails_card = tk.Frame(
    results_frame,
    bg="#243B53",
    bd=1,
    relief="solid"
)

tails_card.grid(
    row=0,
    column=1,
    padx=10,
    sticky="nsew"
)


tails_title = tk.Label(
    tails_card,
    text="TAILS",
    font=("Arial", 12, "bold"),
    bg="#243B53",
    fg="#FF8A80"
)

tails_title.pack(
    pady=(15, 5)
)


tails_label = tk.Label(
    tails_card,
    text="0",
    font=("Arial", 26, "bold"),
    bg="#243B53",
    fg="#FF8A80"
)

tails_label.pack()


tails_percent_label = tk.Label(
    tails_card,
    text="0%",
    font=("Arial", 11),
    bg="#243B53",
    fg="#FFFFFF"
)

tails_percent_label.pack(
    pady=(3, 15)
)


results_frame.columnconfigure(
    0,
    weight=1
)

results_frame.columnconfigure(
    1,
    weight=1
)


total_label = tk.Label(
    main_frame,
    text="Total Flips: 0",
    font=("Arial", 14, "bold"),
    bg="#1B2A41",
    fg="#FFD166"
)

total_label.pack(
    pady=18
)


chart_title = tk.Label(
    main_frame,
    text="Results",
    font=("Arial", 14, "bold"),
    bg="#1B2A41",
    fg="#FFFFFF"
)

chart_title.pack(
    pady=(5, 5)
)


chart = tk.Canvas(
    main_frame,
    width=500,
    height=260,
    bg="#0B1424",
    highlightbackground="#34495E",
    highlightthickness=1
)

chart.pack(
    padx=30,
    pady=5
)


status_label = tk.Label(
    main_frame,
    text="Ready to toss!",
    font=("Arial", 11),
    bg="#1B2A41",
    fg="#FFFFFF"
)

status_label.pack(
    pady=(15, 20)
)


info_label = tk.Label(
    main_frame,
    text="Tip: As the number of flips increases, the results usually get closer to 50% Heads and 50% Tails.",
    font=("Arial", 10),
    bg="#1B2A41",
    fg="#8FA8C2",
    wraplength=700
)

info_label.pack(
    pady=(0, 25)
)


root.mainloop()