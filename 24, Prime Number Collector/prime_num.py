import tkinter as tk


def find_primes():
    try:
        start = int(start_entry.get())
        end = int(end_entry.get())

        if start < 1 or end < 1:
            show_error("Numbers must be greater than 0.")
            return

        if start > end:
            show_error("Start number cannot be greater than end number.")
            return

        if end > 1000000:
            show_error("Please enter an end number up to 1,000,000.")
            return

        status_label.config(
            text="Finding prime numbers...",
            fg="#B8FF3D"
        )

        root.update_idletasks()

        sieve = bytearray(b"\x01") * (end + 1)
        sieve[0:2] = b"\x00\x00"

        limit = int(end ** 0.5)

        for number in range(2, limit + 1):
            if sieve[number]:
                start_index = number * number
                count = ((end - start_index) // number) + 1

                sieve[start_index:end + 1:number] = b"\x00" * count

        primes = [
            number
            for number in range(start, end + 1)
            if sieve[number]
        ]

        result_box.config(state="normal")
        result_box.delete("1.0", tk.END)

        if primes:
            for i in range(0, len(primes), 12):
                row = primes[i:i + 12]
                result_box.insert(
                    tk.END,
                    "     ".join(map(str, row)) + "\n"
                )

            status_label.config(
                text=f"Found {len(primes):,} prime numbers successfully.",
                fg="#B8FF3D"
            )

            largest_prime = primes[-1]

        else:
            result_box.insert(
                tk.END,
                "No prime numbers found in this range."
            )

            status_label.config(
                text="No prime numbers found.",
                fg="#FF6B6B"
            )

            largest_prime = "—"

        result_box.config(state="disabled")

        checked = end - start + 1

        checked_value.config(
            text=f"{checked:,}"
        )

        primes_value.config(
            text=f"{len(primes):,}"
        )

        largest_value.config(
            text=str(largest_prime)
        )

        range_label.config(
            text=f"Range: {start:,} → {end:,}"
        )

    except ValueError:
        show_error("Please enter valid whole numbers.")


def show_error(message):
    status_label.config(
        text=message,
        fg="#FF6B6B"
    )


def clear_all():
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)

    start_entry.insert(0, "1")
    end_entry.insert(0, "1000")

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.config(state="disabled")

    checked_value.config(
        text="0"
    )

    primes_value.config(
        text="0"
    )

    largest_value.config(
        text="—"
    )

    range_label.config(
        text="Range: —"
    )

    status_label.config(
        text="Ready to find prime numbers.",
        fg="#9CA3AF"
    )


def create_stat_card(parent, title, value, color):
    card = tk.Frame(
        parent,
        bg="#24212D",
        bd=1,
        relief="solid"
    )

    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 10, "bold"),
        bg="#24212D",
        fg="#9CA3AF"
    )

    title_label.pack(
        pady=(13, 3)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 21, "bold"),
        bg="#24212D",
        fg=color
    )

    value_label.pack(
        pady=(0, 13)
    )

    return card, value_label


root = tk.Tk()

root.title("Prime Number Finder")

root.geometry("1000x820")
root.minsize(800, 700)
root.resizable(True, True)

root.configure(
    bg="#17151C"
)


header = tk.Frame(
    root,
    bg="#17151C"
)

header.pack(
    fill="x",
    padx=45,
    pady=(25, 12)
)


title_label = tk.Label(
    header,
    text="PRIME FINDER",
    font=("Arial", 32, "bold"),
    bg="#17151C",
    fg="#C084FC"
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="Discover numbers that stand alone",
    font=("Arial", 13),
    bg="#17151C",
    fg="#A3A3A3"
)

subtitle_label.pack(
    pady=(4, 0)
)


main_frame = tk.Frame(
    root,
    bg="#211E29",
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


input_frame = tk.Frame(
    main_frame,
    bg="#211E29"
)

input_frame.pack(
    fill="x",
    padx=50,
    pady=(25, 10)
)


start_frame = tk.Frame(
    input_frame,
    bg="#211E29"
)

start_frame.pack(
    side="left",
    expand=True
)


start_label = tk.Label(
    start_frame,
    text="START NUMBER",
    font=("Arial", 10, "bold"),
    bg="#211E29",
    fg="#FF9F68"
)

start_label.pack(
    pady=(0, 7)
)


start_entry = tk.Entry(
    start_frame,
    font=("Arial", 16, "bold"),
    justify="center",
    bg="#15131A",
    fg="#F5F5F5",
    insertbackground="#C084FC",
    relief="solid",
    bd=1,
    width=15
)

start_entry.pack(
    ipady=9
)

start_entry.insert(
    0,
    "1"
)


end_frame = tk.Frame(
    input_frame,
    bg="#211E29"
)

end_frame.pack(
    side="right",
    expand=True
)


end_label = tk.Label(
    end_frame,
    text="END NUMBER",
    font=("Arial", 10, "bold"),
    bg="#211E29",
    fg="#B8FF3D"
)

end_label.pack(
    pady=(0, 7)
)


end_entry = tk.Entry(
    end_frame,
    font=("Arial", 16, "bold"),
    justify="center",
    bg="#15131A",
    fg="#F5F5F5",
    insertbackground="#C084FC",
    relief="solid",
    bd=1,
    width=15
)

end_entry.pack(
    ipady=9
)

end_entry.insert(
    0,
    "1000"
)


button_frame = tk.Frame(
    main_frame,
    bg="#211E29"
)

button_frame.pack(
    pady=15
)


find_button = tk.Button(
    button_frame,
    text="FIND PRIME NUMBERS",
    font=("Arial", 11, "bold"),
    bg="#7C3AED",
    fg="#FFFFFF",
    activebackground="#9333EA",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=find_primes
)

find_button.grid(
    row=0,
    column=0,
    padx=7,
    ipadx=28,
    ipady=10
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 11, "bold"),
    bg="#B83B5E",
    fg="#FFFFFF",
    activebackground="#D04A6D",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=clear_all
)

clear_button.grid(
    row=0,
    column=1,
    padx=7,
    ipadx=32,
    ipady=10
)


range_label = tk.Label(
    main_frame,
    text="Range: —",
    font=("Arial", 11, "bold"),
    bg="#211E29",
    fg="#FF9F68"
)

range_label.pack(
    pady=(0, 12)
)


stats_frame = tk.Frame(
    main_frame,
    bg="#211E29"
)

stats_frame.pack(
    fill="x",
    padx=40,
    pady=5
)


checked_card, checked_value = create_stat_card(
    stats_frame,
    "NUMBERS CHECKED",
    "0",
    "#FF9F68"
)

checked_card.grid(
    row=0,
    column=0,
    padx=7,
    sticky="nsew"
)


primes_card, primes_value = create_stat_card(
    stats_frame,
    "PRIMES FOUND",
    "0",
    "#B8FF3D"
)

primes_card.grid(
    row=0,
    column=1,
    padx=7,
    sticky="nsew"
)


largest_card, largest_value = create_stat_card(
    stats_frame,
    "LARGEST PRIME",
    "—",
    "#C084FC"
)

largest_card.grid(
    row=0,
    column=2,
    padx=7,
    sticky="nsew"
)


stats_frame.columnconfigure(
    0,
    weight=1
)

stats_frame.columnconfigure(
    1,
    weight=1
)

stats_frame.columnconfigure(
    2,
    weight=1
)


results_title = tk.Label(
    main_frame,
    text="PRIME NUMBERS",
    font=("Arial", 11, "bold"),
    bg="#211E29",
    fg="#F5F5F5"
)

results_title.pack(
    pady=(20, 8)
)


result_frame = tk.Frame(
    main_frame,
    bg="#15131A",
    bd=1,
    relief="solid"
)

result_frame.pack(
    fill="both",
    expand=True,
    padx=50,
    pady=(0, 10)
)


scrollbar = tk.Scrollbar(
    result_frame,
    orient="vertical"
)

scrollbar.pack(
    side="right",
    fill="y"
)


result_box = tk.Text(
    result_frame,
    font=("Consolas", 12, "bold"),
    bg="#15131A",
    fg="#B8FF3D",
    insertbackground="#B8FF3D",
    relief="flat",
    wrap="none",
    yscrollcommand=scrollbar.set
)

result_box.pack(
    side="left",
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

scrollbar.config(
    command=result_box.yview
)

result_box.config(
    state="disabled"
)


status_label = tk.Label(
    main_frame,
    text="Ready to find prime numbers.",
    font=("Arial", 10, "bold"),
    bg="#211E29",
    fg="#9CA3AF"
)

status_label.pack(
    pady=(5, 15)
)


footer = tk.Label(
    root,
    text="Uses the Sieve of Eratosthenes • Maximum range: 1,000,000",
    font=("Arial", 9),
    bg="#17151C",
    fg="#6B7280"
)

footer.pack(
    pady=(5, 15)
)


root.mainloop()