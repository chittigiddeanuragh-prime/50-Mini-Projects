import tkinter as tk
import time
import random


texts = [
    "Python is a powerful programming language used to build applications, automate tasks, analyze data, and create useful solutions for real world problems.",

    "Learning to code takes practice, patience, and consistency. Every small project helps you understand programming concepts and become a better developer.",

    "Technology is changing the world every day. Programmers use creativity and problem solving skills to build applications that make people's lives easier.",

    "The best way to improve your programming skills is to write code regularly, make mistakes, understand them, and keep building new projects.",

    "Computer programming combines logic and creativity. With practice, you can turn simple ideas into useful applications and exciting software projects."
]


current_text = ""
start_time = None
timer_running = False
timer_seconds = 60
timer_job = None


def get_word_count(text):
    return len(text.split())


def start_test():
    global current_text
    global start_time
    global timer_running
    global timer_seconds
    global timer_job

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    current_text = random.choice(texts)

    text_display.config(
        text=current_text
    )

    typing_box.config(
        state="normal"
    )

    typing_box.delete(
        "1.0",
        tk.END
    )

    typing_box.focus()

    start_time = None
    timer_running = False
    timer_seconds = 60

    time_value.config(
        text="60"
    )

    wpm_value.config(
        text="0"
    )

    accuracy_value.config(
        text="0%"
    )

    words_value.config(
        text="0"
    )

    result_label.config(
        text="Start typing to begin the test.",
        fg="#365314"
    )

    status_label.config(
        text="Ready",
        fg="#15803D"
    )


def clear_text():
    global start_time
    global timer_running
    global timer_job

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None

    start_time = None
    timer_running = False

    typing_box.config(
        state="normal"
    )

    typing_box.delete(
        "1.0",
        tk.END
    )

    time_value.config(
        text="60"
    )

    wpm_value.config(
        text="0"
    )

    accuracy_value.config(
        text="0%"
    )

    words_value.config(
        text="0"
    )

    result_label.config(
        text="Text cleared. Start typing when ready.",
        fg="#365314"
    )

    status_label.config(
        text="Ready",
        fg="#15803D"
    )

    typing_box.focus()


def typing_started(event=None):
    global start_time
    global timer_running

    if timer_running:
        return

    if typing_box.get("1.0", tk.END).strip() == "":
        return

    if start_time is None:
        start_time = time.time()
        timer_running = True
        status_label.config(
            text="Test running...",
            fg="#0284C7"
        )
        update_timer()


def calculate_results():
    global start_time

    typed_text = typing_box.get(
        "1.0",
        tk.END
    ).rstrip("\n")

    if start_time is None:
        return

    elapsed_time = time.time() - start_time

    if elapsed_time <= 0:
        elapsed_time = 1

    words = len(typed_text.split())

    wpm = round(
        words / (elapsed_time / 60)
    )

    correct_characters = 0

    for i in range(
        min(
            len(typed_text),
            len(current_text)
        )
    ):
        if typed_text[i] == current_text[i]:
            correct_characters += 1

    if len(typed_text) > 0:
        accuracy = (
            correct_characters /
            len(typed_text)
        ) * 100
    else:
        accuracy = 0

    wpm_value.config(
        text=str(wpm)
    )

    accuracy_value.config(
        text=f"{accuracy:.1f}%"
    )

    words_value.config(
        text=str(words)
    )


def update_timer():
    global timer_seconds
    global timer_job

    if not timer_running:
        return

    typed_text = typing_box.get(
        "1.0",
        tk.END
    ).rstrip("\n")

    if typed_text == "":
        timer_job = root.after(
            100,
            update_timer
        )
        return

    timer_seconds -= 1

    time_value.config(
        text=str(timer_seconds)
    )

    calculate_results()

    if timer_seconds <= 0:
        finish_test()
        return

    timer_job = root.after(
        1000,
        update_timer
    )


def finish_test():
    global timer_running
    global timer_job

    timer_running = False

    if timer_job is not None:
        try:
            root.after_cancel(timer_job)
        except:
            pass

        timer_job = None

    calculate_results()

    typing_box.config(
        state="disabled"
    )

    status_label.config(
        text="Test completed!",
        fg="#DC2626"
    )

    result_label.config(
        text="Time is up! Click START / RESTART to try again.",
        fg="#DC2626"
    )


def check_completion(event=None):
    global timer_running

    if not timer_running:
        return

    typed_text = typing_box.get(
        "1.0",
        tk.END
    ).rstrip("\n")

    if len(typed_text) >= len(current_text):
        finish_test()


root = tk.Tk()

root.title(
    "Typing Speed Tester"
)

root.geometry(
    "1000x820"
)

root.minsize(
    800,
    700
)

root.resizable(
    True,
    True
)

root.configure(
    bg="#F7E84A"
)


header = tk.Frame(
    root,
    bg="#F7E84A"
)

header.pack(
    fill="x",
    padx=45,
    pady=(25, 12)
)


title_label = tk.Label(
    header,
    text="TYPING SPEED TEST",
    font=("Arial", 32, "bold"),
    bg="#F7E84A",
    fg="#14532D"
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="Test your typing speed, accuracy and consistency",
    font=("Arial", 13),
    bg="#F7E84A",
    fg="#3F6212"
)

subtitle_label.pack(
    pady=(4, 0)
)


main_frame = tk.Frame(
    root,
    bg="#ECF8D5",
    bd=2,
    relief="solid",
    highlightbackground="#65A30D",
    highlightthickness=2
)

main_frame.pack(
    padx=45,
    pady=5,
    fill="both",
    expand=True
)


stats_frame = tk.Frame(
    main_frame,
    bg="#ECF8D5"
)

stats_frame.pack(
    fill="x",
    padx=35,
    pady=(25, 15)
)


def create_stat(parent, title, value, color):
    card = tk.Frame(
        parent,
        bg="#FFFFFF",
        bd=1,
        relief="solid"
    )

    label = tk.Label(
        card,
        text=title,
        font=("Arial", 10, "bold"),
        bg="#FFFFFF",
        fg="#64748B"
    )

    label.pack(
        pady=(12, 2)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 22, "bold"),
        bg="#FFFFFF",
        fg=color
    )

    value_label.pack(
        pady=(0, 12)
    )

    return card, value_label


time_card, time_value = create_stat(
    stats_frame,
    "TIME",
    "60",
    "#0284C7"
)

time_card.grid(
    row=0,
    column=0,
    padx=7,
    sticky="nsew"
)


wpm_card, wpm_value = create_stat(
    stats_frame,
    "WPM",
    "0",
    "#15803D"
)

wpm_card.grid(
    row=0,
    column=1,
    padx=7,
    sticky="nsew"
)


accuracy_card, accuracy_value = create_stat(
    stats_frame,
    "ACCURACY",
    "0%",
    "#DC2626"
)

accuracy_card.grid(
    row=0,
    column=2,
    padx=7,
    sticky="nsew"
)


words_card, words_value = create_stat(
    stats_frame,
    "WORDS",
    "0",
    "#CA8A04"
)

words_card.grid(
    row=0,
    column=3,
    padx=7,
    sticky="nsew"
)


for column in range(4):
    stats_frame.columnconfigure(
        column,
        weight=1
    )


sample_title = tk.Label(
    main_frame,
    text="TYPE THE FOLLOWING TEXT",
    font=("Arial", 11, "bold"),
    bg="#ECF8D5",
    fg="#365314"
)

sample_title.pack(
    pady=(5, 8)
)


sample_frame = tk.Frame(
    main_frame,
    bg="#FFFFFF",
    bd=1,
    relief="solid"
)

sample_frame.pack(
    fill="x",
    padx=50
)


text_display = tk.Label(
    sample_frame,
    text="",
    font=("Arial", 14),
    bg="#FFFFFF",
    fg="#334155",
    wraplength=800,
    justify="left",
    anchor="w"
)

text_display.pack(
    fill="x",
    padx=20,
    pady=20
)


typing_title = tk.Label(
    main_frame,
    text="START TYPING HERE",
    font=("Arial", 11, "bold"),
    bg="#ECF8D5",
    fg="#365314"
)

typing_title.pack(
    pady=(18, 8)
)


typing_box = tk.Text(
    main_frame,
    font=("Arial", 14),
    bg="#F8FAFC",
    fg="#1E293B",
    insertbackground="#0284C7",
    relief="solid",
    bd=2,
    wrap="word",
    height=5
)

typing_box.pack(
    fill="both",
    expand=True,
    padx=50
)


typing_box.bind(
    "<KeyRelease>",
    typing_started
)

typing_box.bind(
    "<KeyRelease>",
    check_completion,
    add="+"
)


button_frame = tk.Frame(
    main_frame,
    bg="#ECF8D5"
)

button_frame.pack(
    pady=15
)


start_button = tk.Button(
    button_frame,
    text="START / RESTART",
    font=("Arial", 11, "bold"),
    bg="#38BDF8",
    fg="#082F49",
    activebackground="#0EA5E9",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=start_test
)

start_button.grid(
    row=0,
    column=0,
    padx=7,
    ipadx=25,
    ipady=9
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 11, "bold"),
    bg="#EF4444",
    fg="#FFFFFF",
    activebackground="#DC2626",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=clear_text
)

clear_button.grid(
    row=0,
    column=1,
    padx=7,
    ipadx=35,
    ipady=9
)


status_label = tk.Label(
    main_frame,
    text="Ready",
    font=("Arial", 11, "bold"),
    bg="#ECF8D5",
    fg="#15803D"
)

status_label.pack(
    pady=(0, 5)
)


result_label = tk.Label(
    main_frame,
    text="Start typing to begin the test.",
    font=("Arial", 11),
    bg="#ECF8D5",
    fg="#365314"
)

result_label.pack(
    pady=(0, 15)
)


footer = tk.Label(
    root,
    text="60-second typing challenge • WPM + Accuracy",
    font=("Arial", 10),
    bg="#F7E84A",
    fg="#3F6212"
)

footer.pack(
    pady=(5, 15)
)


start_test()

root.mainloop()