import tkinter as tk
import random
import string


def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4:
            password_box.delete(0, tk.END)
            password_box.insert(0, "Minimum length is 4")
            status_label.config(text="Please enter a bigger number", fg="#ffcc00")
            return

        characters = string.ascii_letters + string.digits + string.punctuation

        password = ''.join(
            random.SystemRandom().choice(characters)
            for _ in range(length)
        )

        password_box.delete(0, tk.END)
        password_box.insert(0, password)

        status_label.config(
            text="Password generated successfully!",
            fg="#9cff57"
        )

    except ValueError:
        password_box.delete(0, tk.END)
        password_box.insert(0, "Invalid length")
        status_label.config(
            text="Enter a number like 12 or 16",
            fg="#ffcc00"
        )


def clear_all():
    length_entry.delete(0, tk.END)
    length_entry.insert(0, "12")

    password_box.delete(0, tk.END)

    status_label.config(
        text="Ready",
        fg="#dddddd"
    )


root = tk.Tk()
root.title("My Password Generator")
root.geometry("500x570")
root.resizable(False, False)
root.configure(bg="#172117")


title = tk.Label(
    root,
    text="Password Generator",
    font=("Arial", 24, "bold"),
    bg="#172117",
    fg="#dfff72"
)
title.pack(pady=(35, 5))


subtitle = tk.Label(
    root,
    text="Create a random password in seconds",
    font=("Arial", 11),
    bg="#172117",
    fg="#b8c7b8"
)
subtitle.pack(pady=(0, 25))


main_frame = tk.Frame(
    root,
    bg="#243524",
    bd=1,
    relief="solid"
)
main_frame.pack(padx=35, fill="both", expand=True)


length_label = tk.Label(
    main_frame,
    text="Password length:",
    font=("Arial", 12, "bold"),
    bg="#243524",
    fg="#ffffff"
)
length_label.pack(pady=(35, 8))


length_entry = tk.Entry(
    main_frame,
    font=("Arial", 15),
    justify="center",
    width=10,
    bg="#111a11",
    fg="#ffffff",
    insertbackground="#ffffff",
    relief="solid",
    bd=1
)
length_entry.pack(ipady=7)
length_entry.insert(0, "12")


generate_button = tk.Button(
    main_frame,
    text="Generate Password",
    font=("Arial", 12, "bold"),
    bg="#75a943",
    fg="#101810",
    activebackground="#a6d957",
    activeforeground="#101810",
    relief="flat",
    cursor="hand2",
    command=generate_password
)
generate_button.pack(pady=25, ipadx=20, ipady=9)


password_label = tk.Label(
    main_frame,
    text="Your password:",
    font=("Arial", 12, "bold"),
    bg="#243524",
    fg="#ffffff"
)
password_label.pack(pady=(5, 8))


password_box = tk.Entry(
    main_frame,
    font=("Consolas", 13),
    justify="center",
    width=35,
    bg="#111a11",
    fg="#dfff72",
    insertbackground="#ffffff",
    relief="solid",
    bd=1
)
password_box.pack(ipady=9, padx=20)


status_label = tk.Label(
    main_frame,
    text="Ready",
    font=("Arial", 10),
    bg="#243524",
    fg="#dddddd"
)
status_label.pack(pady=18)


clear_button = tk.Button(
    main_frame,
    text="Clear",
    font=("Arial", 11),
    bg="#454d35",
    fg="#ffffff",
    activebackground="#5b6546",
    activeforeground="#ffffff",
    relief="flat",
    cursor="hand2",
    command=clear_all
)
clear_button.pack(ipadx=25, ipady=7)


info = tk.Label(
    main_frame,
    text="Tip: Use 12+ characters for better security.",
    font=("Arial", 9),
    bg="#243524",
    fg="#aeb9a5"
)
info.pack(pady=(20, 15))


root.mainloop()