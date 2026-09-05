import tkinter as tk


def generate_fibonacci():
    try:
        terms = int(terms_entry.get())

        if terms < 1 or terms > 100:
            status_label.config(
                text="Enter a number between 1 and 100.",
                fg="#FF6B8A"
            )
            return

        sequence = []

        if terms >= 1:
            sequence.append(0)

        if terms >= 2:
            sequence.append(1)

        for i in range(2, terms):
            sequence.append(sequence[i - 1] + sequence[i - 2])

        display_sequence(sequence)
        display_steps(sequence)
        draw_growth(sequence)

        terms_value.config(
            text=str(terms)
        )

        last_value.config(
            text=f"{sequence[-1]:,}"
        )

        status_label.config(
            text=f"Generated {terms} Fibonacci terms successfully.",
            fg="#5EEAD4"
        )

    except ValueError:
        status_label.config(
            text="Please enter a valid whole number.",
            fg="#FF6B8A"
        )


def display_sequence(sequence):
    sequence_box.config(
        state="normal"
    )

    sequence_box.delete(
        "1.0",
        tk.END
    )

    for i, number in enumerate(sequence):
        if i == len(sequence) - 1:
            sequence_box.insert(
                tk.END,
                f"{number:,}"
            )
        else:
            sequence_box.insert(
                tk.END,
                f"{number:,}   →   "
            )

    sequence_box.config(
        state="disabled"
    )


def display_steps(sequence):
    steps_box.config(
        state="normal"
    )

    steps_box.delete(
        "1.0",
        tk.END
    )

    if len(sequence) == 1:
        steps_box.insert(
            tk.END,
            "Starting value:\n\n0"
        )

    elif len(sequence) >= 2:

        steps_box.insert(
            tk.END,
            "Starting values:\n\n"
        )

        steps_box.insert(
            tk.END,
            "Term 1  →  0\n"
        )

        steps_box.insert(
            tk.END,
            "Term 2  →  1\n\n"
        )

        steps_box.insert(
            tk.END,
            "Each new number is created by adding the previous two:\n\n"
        )

        for i in range(2, len(sequence)):
            steps_box.insert(
                tk.END,
                f"{sequence[i - 2]:,} + {sequence[i - 1]:,} = {sequence[i]:,}\n"
            )

    steps_box.config(
        state="disabled"
    )


def draw_growth(sequence):
    chart.delete(
        "all"
    )

    if not sequence:
        return

    width = max(
        chart.winfo_width(),
        700
    )

    height = max(
        chart.winfo_height(),
        240
    )

    padding = 45

    max_value = max(
        sequence
    )

    if max_value == 0:
        max_value = 1

    usable_width = width - (padding * 2)
    usable_height = height - (padding * 2)

    points = []

    if len(sequence) == 1:
        x = width / 2
        y = height - padding
        points.append(
            (x, y)
        )

    else:
        for i, value in enumerate(sequence):
            x = padding + (
                i / (len(sequence) - 1)
            ) * usable_width

            y = height - padding - (
                value / max_value
            ) * usable_height

            points.append(
                (x, y)
            )

    if len(points) > 1:
        for i in range(len(points) - 1):
            chart.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                fill="#A78BFA",
                width=3
            )

    for i, point in enumerate(points):

        chart.create_oval(
            point[0] - 5,
            point[1] - 5,
            point[0] + 5,
            point[1] + 5,
            fill="#F472B6",
            outline=""
        )

        if len(sequence) <= 20:
            chart.create_text(
                point[0],
                point[1] - 15,
                text=str(sequence[i]),
                fill="#F8FAFC",
                font=("Arial", 9, "bold")
            )


def clear_all():
    terms_entry.delete(
        0,
        tk.END
    )

    terms_entry.insert(
        0,
        "15"
    )

    sequence_box.config(
        state="normal"
    )

    sequence_box.delete(
        "1.0",
        tk.END
    )

    sequence_box.config(
        state="disabled"
    )

    steps_box.config(
        state="normal"
    )

    steps_box.delete(
        "1.0",
        tk.END
    )

    steps_box.config(
        state="disabled"
    )

    chart.delete(
        "all"
    )

    terms_value.config(
        text="0"
    )

    last_value.config(
        text="—"
    )

    status_label.config(
        text="Ready to generate a Fibonacci sequence.",
        fg="#94A3B8"
    )


def resize_chart(event):
    if sequence_box.get(
        "1.0",
        tk.END
    ).strip():

        sequence_text = sequence_box.get(
            "1.0",
            tk.END
        ).strip()

        values = []

        parts = sequence_text.split("→")

        for part in parts:
            part = part.strip()

            try:
                values.append(
                    int(part.replace(",", ""))
                )
            except ValueError:
                pass

        if values:
            draw_growth(values)


root = tk.Tk()

root.title(
    "Fibonacci Lab"
)

root.geometry(
    "1100x850"
)

root.minsize(
    850,
    700
)

root.resizable(
    True,
    True
)

root.configure(
    bg="#12101F"
)


header = tk.Frame(
    root,
    bg="#12101F"
)

header.pack(
    fill="x",
    padx=45,
    pady=(25, 10)
)


title_label = tk.Label(
    header,
    text="FIBONACCI LAB",
    font=("Arial", 32, "bold"),
    bg="#12101F",
    fg="#A78BFA"
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="Explore how one number leads to the next",
    font=("Arial", 13),
    bg="#12101F",
    fg="#94A3B8"
)

subtitle_label.pack(
    pady=(4, 0)
)


main_frame = tk.Frame(
    root,
    bg="#211D35",
    bd=2,
    relief="solid",
    highlightbackground="#7C3AED",
    highlightthickness=2
)

main_frame.pack(
    padx=45,
    pady=5,
    fill="both",
    expand=True
)


control_frame = tk.Frame(
    main_frame,
    bg="#211D35"
)

control_frame.pack(
    fill="x",
    padx=45,
    pady=(25, 15)
)


terms_label = tk.Label(
    control_frame,
    text="NUMBER OF TERMS",
    font=("Arial", 10, "bold"),
    bg="#211D35",
    fg="#CBD5E1"
)

terms_label.pack(
    side="left",
    padx=(0, 10)
)


terms_entry = tk.Entry(
    control_frame,
    font=("Arial", 14, "bold"),
    justify="center",
    bg="#151225",
    fg="#F8FAFC",
    insertbackground="#A78BFA",
    relief="solid",
    bd=1,
    width=8
)

terms_entry.pack(
    side="left",
    ipady=7
)

terms_entry.insert(
    0,
    "15"
)


generate_button = tk.Button(
    control_frame,
    text="GENERATE",
    font=("Arial", 10, "bold"),
    bg="#7C3AED",
    fg="#FFFFFF",
    activebackground="#8B5CF6",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=generate_fibonacci
)

generate_button.pack(
    side="left",
    padx=10,
    ipadx=22,
    ipady=9
)


clear_button = tk.Button(
    control_frame,
    text="CLEAR",
    font=("Arial", 10, "bold"),
    bg="#BE185D",
    fg="#FFFFFF",
    activebackground="#DB2777",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=clear_all
)

clear_button.pack(
    side="left",
    ipadx=25,
    ipady=9
)


content_frame = tk.Frame(
    main_frame,
    bg="#211D35"
)

content_frame.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=5
)


sequence_frame = tk.Frame(
    content_frame,
    bg="#18152A",
    bd=1,
    relief="solid"
)

sequence_frame.grid(
    row=0,
    column=0,
    padx=8,
    sticky="nsew"
)


sequence_title = tk.Label(
    sequence_frame,
    text="FIBONACCI SEQUENCE",
    font=("Arial", 11, "bold"),
    bg="#18152A",
    fg="#5EEAD4"
)

sequence_title.pack(
    pady=(18, 8)
)


sequence_box = tk.Text(
    sequence_frame,
    font=("Consolas", 12, "bold"),
    bg="#18152A",
    fg="#F472B6",
    relief="flat",
    wrap="word",
    height=8
)

sequence_box.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

sequence_box.config(
    state="disabled"
)


steps_frame = tk.Frame(
    content_frame,
    bg="#18152A",
    bd=1,
    relief="solid"
)

steps_frame.grid(
    row=0,
    column=1,
    padx=8,
    sticky="nsew"
)


steps_title = tk.Label(
    steps_frame,
    text="HOW FIBONACCI WORKS",
    font=("Arial", 11, "bold"),
    bg="#18152A",
    fg="#FBBF24"
)

steps_title.pack(
    pady=(18, 8)
)


steps_box = tk.Text(
    steps_frame,
    font=("Consolas", 11),
    bg="#18152A",
    fg="#CBD5E1",
    relief="flat",
    wrap="word",
    height=8
)

steps_box.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

steps_box.config(
    state="disabled"
)


content_frame.columnconfigure(
    0,
    weight=1
)

content_frame.columnconfigure(
    1,
    weight=1
)

content_frame.rowconfigure(
    0,
    weight=1
)


chart_title = tk.Label(
    main_frame,
    text="VISUAL GROWTH",
    font=("Arial", 11, "bold"),
    bg="#211D35",
    fg="#A78BFA"
)

chart_title.pack(
    pady=(15, 7)
)


chart = tk.Canvas(
    main_frame,
    bg="#151225",
    highlightbackground="#352D55",
    highlightthickness=1,
    height=210
)

chart.pack(
    fill="x",
    padx=50
)


bottom_frame = tk.Frame(
    main_frame,
    bg="#211D35"
)

bottom_frame.pack(
    fill="x",
    padx=50,
    pady=(15, 20)
)


terms_value = tk.Label(
    bottom_frame,
    text="0",
    font=("Arial", 10, "bold"),
    bg="#211D35",
    fg="#5EEAD4"
)

tk.Label(
    bottom_frame,
    text="Terms:",
    font=("Arial", 10, "bold"),
    bg="#211D35",
    fg="#94A3B8"
).pack(
    side="left"
)

terms_value.pack(
    side="left",
    padx=(5, 30)
)


tk.Label(
    bottom_frame,
    text="Last Number:",
    font=("Arial", 10, "bold"),
    bg="#211D35",
    fg="#94A3B8"
).pack(
    side="left"
)


last_value = tk.Label(
    bottom_frame,
    text="—",
    font=("Arial", 10, "bold"),
    bg="#211D35",
    fg="#F472B6"
)

last_value.pack(
    side="left",
    padx=(5, 30)
)


status_label = tk.Label(
    bottom_frame,
    text="Ready to generate a Fibonacci sequence.",
    font=("Arial", 10, "bold"),
    bg="#211D35",
    fg="#94A3B8"
)

status_label.pack(
    side="right"
)


footer = tk.Label(
    root,
    text="Fibonacci Rule: Each number is the sum of the two numbers before it.",
    font=("Arial", 9),
    bg="#12101F",
    fg="#6B7280"
)

footer.pack(
    pady=(5, 15)
)


root.bind(
    "<Return>",
    lambda event: generate_fibonacci()
)

generate_fibonacci()

root.mainloop()