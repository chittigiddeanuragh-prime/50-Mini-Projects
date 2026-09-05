import tkinter as tk
import random


questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "answer": "Mars"
    },
    {
        "question": "What is 12 × 8?",
        "options": ["86", "96", "108", "112"],
        "answer": "96"
    },
    {
        "question": "Which language is mainly used to style web pages?",
        "options": ["Python", "HTML", "CSS", "Java"],
        "answer": "CSS"
    },
    {
        "question": "How many continents are there?",
        "options": ["5", "6", "7", "8"],
        "answer": "7"
    },
    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
        "answer": "Carbon Dioxide"
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": [
            "Isaac Newton",
            "Albert Einstein",
            "Galileo Galilei",
            "Nikola Tesla"
        ],
        "answer": "Albert Einstein"
    },
    {
        "question": "Which data type stores True or False values in Python?",
        "options": ["String", "Integer", "Boolean", "Float"],
        "answer": "Boolean"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": [
            "Atlantic Ocean",
            "Indian Ocean",
            "Arctic Ocean",
            "Pacific Ocean"
        ],
        "answer": "Pacific Ocean"
    },
    {
        "question": "Which device is used to connect a computer to a network?",
        "options": ["Monitor", "Router", "Keyboard", "Printer"],
        "answer": "Router"
    }
]


questions = questions.copy()
random.shuffle(questions)

current_question = 0
score = 0
selected_answer = None
quiz_finished = False


def load_question():
    global selected_answer

    selected_answer = None

    if current_question >= len(questions):
        show_result()
        return

    question_data = questions[current_question]

    question_number_label.config(
        text=f"QUESTION {current_question + 1} / {len(questions)}"
    )

    score_label.config(
        text=f"SCORE: {score}"
    )

    question_label.config(
        text=question_data["question"]
    )

    progress = ((current_question) / len(questions)) * 100
    progress_canvas.delete("all")

    progress_width = 700 * (progress / 100)

    progress_canvas.create_rectangle(
        0,
        0,
        progress_width,
        12,
        fill="#22C55E",
        outline=""
    )

    for i in range(4):
        option_buttons[i].config(
            text=f"{chr(65 + i)}   {question_data['options'][i]}",
            bg="#26354D",
            fg="#F8FAFC",
            state="normal"
        )

    next_button.config(
        state="disabled",
        bg="#475569"
    )

    status_label.config(
        text="Select an answer to continue",
        fg="#94A3B8"
    )


def select_answer(index):
    global selected_answer

    if quiz_finished:
        return

    selected_answer = index

    for button in option_buttons:
        button.config(
            bg="#26354D"
        )

    option_buttons[index].config(
        bg="#2563EB"
    )

    next_button.config(
        state="normal",
        bg="#F59E0B"
    )

    status_label.config(
        text="Answer selected. Click Next Question.",
        fg="#38BDF8"
    )


def next_question():
    global current_question, score

    if selected_answer is None:
        return

    question_data = questions[current_question]

    selected_text = question_data["options"][selected_answer]

    if selected_text == question_data["answer"]:
        score += 10

        option_buttons[selected_answer].config(
            bg="#16A34A"
        )

        status_label.config(
            text="Correct answer!",
            fg="#22C55E"
        )

    else:
        option_buttons[selected_answer].config(
            bg="#DC2626"
        )

        for i, option in enumerate(question_data["options"]):
            if option == question_data["answer"]:
                option_buttons[i].config(
                    bg="#16A34A"
                )

        status_label.config(
            text=f"Correct answer: {question_data['answer']}",
            fg="#FBBF24"
        )

    root.after(900, move_to_next)


def move_to_next():
    global current_question

    current_question += 1

    if current_question < len(questions):
        load_question()
    else:
        show_result()


def show_result():
    global quiz_finished

    quiz_finished = True

    progress_canvas.delete("all")

    progress_canvas.create_rectangle(
        0,
        0,
        700,
        12,
        fill="#22C55E",
        outline=""
    )

    question_label.config(
        text="QUIZ COMPLETED!"
    )

    question_number_label.config(
        text="FINAL RESULT"
    )

    score_label.config(
        text=f"SCORE: {score}"
    )

    for button in option_buttons:
        button.config(
            text="",
            bg="#1E293B",
            state="disabled"
        )

    if score == 100:
        message = "Excellent! Perfect score!"
        result_color = "#22C55E"
    elif score >= 70:
        message = "Great job! You have strong knowledge."
        result_color = "#38BDF8"
    elif score >= 50:
        message = "Good attempt! Keep practicing."
        result_color = "#FBBF24"
    else:
        message = "Keep learning and try again!"
        result_color = "#F97316"

    status_label.config(
        text=message,
        fg=result_color
    )

    next_button.config(
        text="PLAY AGAIN",
        state="normal",
        bg="#8B5CF6",
        command=restart_quiz
    )


def restart_quiz():
    global questions, current_question, score, quiz_finished

    questions = questions.copy()
    random.shuffle(questions)

    current_question = 0
    score = 0
    quiz_finished = False

    next_button.config(
        text="NEXT QUESTION",
        command=next_question
    )

    load_question()


root = tk.Tk()

root.title("Quiz Master")

root.geometry("1000x850")
root.minsize(800, 700)
root.resizable(True, True)

root.configure(
    bg="#0F172A"
)


header = tk.Frame(
    root,
    bg="#0F172A"
)

header.pack(
    fill="x",
    padx=50,
    pady=(25, 10)
)


title_label = tk.Label(
    header,
    text="QUIZ MASTER",
    font=("Arial", 32, "bold"),
    bg="#0F172A",
    fg="#FBBF24"
)

title_label.pack()


subtitle_label = tk.Label(
    header,
    text="Test your knowledge and challenge yourself",
    font=("Arial", 13),
    bg="#0F172A",
    fg="#94A3B8"
)

subtitle_label.pack(
    pady=(3, 0)
)


main_frame = tk.Frame(
    root,
    bg="#1E293B",
    bd=2,
    relief="solid",
    highlightbackground="#334155",
    highlightthickness=2
)

main_frame.pack(
    padx=45,
    pady=10,
    fill="both",
    expand=True
)


top_bar = tk.Frame(
    main_frame,
    bg="#1E293B"
)

top_bar.pack(
    fill="x",
    padx=35,
    pady=(25, 8)
)


question_number_label = tk.Label(
    top_bar,
    text="QUESTION 1 / 10",
    font=("Arial", 13, "bold"),
    bg="#1E293B",
    fg="#38BDF8"
)

question_number_label.pack(
    side="left"
)


score_label = tk.Label(
    top_bar,
    text="SCORE: 0",
    font=("Arial", 13, "bold"),
    bg="#1E293B",
    fg="#FBBF24"
)

score_label.pack(
    side="right"
)


progress_canvas = tk.Canvas(
    main_frame,
    height=12,
    bg="#334155",
    highlightthickness=0
)

progress_canvas.pack(
    fill="x",
    padx=35,
    pady=(0, 25)
)


question_card = tk.Frame(
    main_frame,
    bg="#243447",
    bd=1,
    relief="solid"
)

question_card.pack(
    fill="x",
    padx=50,
    pady=5
)


question_label = tk.Label(
    question_card,
    text="Question",
    font=("Arial", 21, "bold"),
    bg="#243447",
    fg="#F8FAFC",
    wraplength=750,
    justify="center"
)

question_label.pack(
    padx=30,
    pady=28
)


options_frame = tk.Frame(
    main_frame,
    bg="#1E293B"
)

options_frame.pack(
    fill="both",
    expand=True,
    padx=50,
    pady=20
)


option_buttons = []


for i in range(4):

    button = tk.Button(
        options_frame,
        text="",
        font=("Arial", 13, "bold"),
        bg="#26354D",
        fg="#F8FAFC",
        activebackground="#3B82F6",
        activeforeground="#FFFFFF",
        relief="solid",
        bd=1,
        cursor="hand2",
        command=lambda index=i: select_answer(index)
    )

    row = i // 2
    column = i % 2

    button.grid(
        row=row,
        column=column,
        padx=10,
        pady=10,
        sticky="nsew"
    )

    option_buttons.append(button)


options_frame.rowconfigure(0, weight=1)
options_frame.rowconfigure(1, weight=1)

options_frame.columnconfigure(0, weight=1)
options_frame.columnconfigure(1, weight=1)


bottom_frame = tk.Frame(
    main_frame,
    bg="#1E293B"
)

bottom_frame.pack(
    fill="x",
    padx=50,
    pady=(5, 25)
)


status_label = tk.Label(
    bottom_frame,
    text="Select an answer to continue",
    font=("Arial", 11),
    bg="#1E293B",
    fg="#94A3B8"
)

status_label.pack(
    pady=(0, 12)
)


next_button = tk.Button(
    bottom_frame,
    text="NEXT QUESTION",
    font=("Arial", 12, "bold"),
    bg="#475569",
    fg="#FFFFFF",
    activebackground="#F59E0B",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    state="disabled",
    command=next_question
)

next_button.pack(
    ipadx=45,
    ipady=11
)


footer = tk.Label(
    root,
    text="10 Questions  •  10 Points Each  •  Choose the best answer",
    font=("Arial", 10),
    bg="#0F172A",
    fg="#64748B"
)

footer.pack(
    pady=(5, 15)
)


load_question()

root.mainloop()