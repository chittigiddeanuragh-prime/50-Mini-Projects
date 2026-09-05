import tkinter as tk
import json
import os


FILE_NAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    return []


def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def update_list():
    task_list.delete(0, tk.END)

    for task in tasks:
        if task["completed"]:
            task_list.insert(tk.END, "✓ " + task["name"])
            task_list.itemconfig(tk.END, fg="#70E1FF")
        else:
            task_list.insert(tk.END, "○ " + task["name"])
            task_list.itemconfig(tk.END, fg="#FFFFFF")

    completed = sum(task["completed"] for task in tasks)

    count_label.config(
        text=f"Tasks: {len(tasks)}   Completed: {completed}"
    )


def add_task():
    task = task_entry.get().strip()

    if not task:
        status_label.config(
            text="Please enter a task",
            fg="#FFD166"
        )
        return

    tasks.append({
        "name": task,
        "completed": False
    })

    task_entry.delete(0, tk.END)
    save_tasks()
    update_list()

    status_label.config(
        text="Task added!",
        fg="#70E1FF"
    )


def complete_task():
    selected = task_list.curselection()

    if not selected:
        status_label.config(
            text="Select a task first",
            fg="#FFD166"
        )
        return

    index = selected[0]

    tasks[index]["completed"] = not tasks[index]["completed"]

    save_tasks()
    update_list()

    status_label.config(
        text="Task updated!",
        fg="#70E1FF"
    )


def delete_task():
    selected = task_list.curselection()

    if not selected:
        status_label.config(
            text="Select a task first",
            fg="#FFD166"
        )
        return

    index = selected[0]

    tasks.pop(index)

    save_tasks()
    update_list()

    status_label.config(
        text="Task deleted",
        fg="#FF8FB1"
    )


def clear_tasks():
    if not tasks:
        status_label.config(
            text="There are no tasks to clear",
            fg="#FFD166"
        )
        return

    tasks.clear()

    save_tasks()
    update_list()

    status_label.config(
        text="All tasks cleared",
        fg="#FF8FB1"
    )


def add_with_enter(event):
    add_task()


tasks = load_tasks()


root = tk.Tk()
root.title("My To-Do List")

root.geometry("650x750")
root.minsize(500, 600)
root.resizable(True, True)

root.configure(bg="#172B4D")


title = tk.Label(
    root,
    text="My To-Do List",
    font=("Arial", 25, "bold"),
    bg="#172B4D",
    fg="#FF8FB1"
)
title.pack(pady=(30, 5))


subtitle = tk.Label(
    root,
    text="Keep track of the things you need to do",
    font=("Arial", 11),
    bg="#172B4D",
    fg="#70E1FF"
)
subtitle.pack(pady=(0, 20))


main_frame = tk.Frame(
    root,
    bg="#243B63",
    bd=2,
    relief="solid",
    highlightbackground="#70E1FF",
    highlightthickness=1
)
main_frame.pack(
    padx=30,
    pady=(0, 20),
    fill="both",
    expand=True
)


task_entry = tk.Entry(
    main_frame,
    font=("Arial", 14),
    bg="#101D35",
    fg="#FFFFFF",
    insertbackground="#70E1FF",
    relief="solid",
    bd=1
)
task_entry.pack(
    padx=25,
    pady=(25, 10),
    fill="x",
    ipady=9
)

task_entry.bind("<Return>", add_with_enter)


add_button = tk.Button(
    main_frame,
    text="Add Task",
    font=("Arial", 11, "bold"),
    bg="#FF8FB1",
    fg="#172B4D",
    activebackground="#FFB6C9",
    activeforeground="#172B4D",
    relief="flat",
    cursor="hand2",
    command=add_task
)
add_button.pack(
    ipadx=25,
    ipady=7
)


task_list = tk.Listbox(
    main_frame,
    font=("Arial", 12),
    bg="#101D35",
    fg="#FFFFFF",
    selectbackground="#3C8DAD",
    selectforeground="#FFFFFF",
    relief="solid",
    bd=1,
    height=13
)
task_list.pack(
    padx=25,
    pady=20,
    fill="both",
    expand=True
)


count_label = tk.Label(
    main_frame,
    text="Tasks: 0   Completed: 0",
    font=("Arial", 10, "bold"),
    bg="#243B63",
    fg="#70E1FF"
)
count_label.pack(pady=(0, 10))


button_frame = tk.Frame(
    main_frame,
    bg="#243B63"
)
button_frame.pack(pady=(0, 10))


complete_button = tk.Button(
    button_frame,
    text="Complete",
    font=("Arial", 10, "bold"),
    bg="#70E1FF",
    fg="#172B4D",
    activebackground="#9AEAFF",
    relief="flat",
    cursor="hand2",
    command=complete_task
)
complete_button.grid(
    row=0,
    column=0,
    padx=5,
    ipadx=10,
    ipady=6
)


delete_button = tk.Button(
    button_frame,
    text="Delete",
    font=("Arial", 10, "bold"),
    bg="#FF8FB1",
    fg="#172B4D",
    activebackground="#FFB6C9",
    relief="flat",
    cursor="hand2",
    command=delete_task
)
delete_button.grid(
    row=0,
    column=1,
    padx=5,
    ipadx=10,
    ipady=6
)


clear_button = tk.Button(
    button_frame,
    text="Clear All",
    font=("Arial", 10, "bold"),
    bg="#4E6FA8",
    fg="#FFFFFF",
    activebackground="#6388C5",
    relief="flat",
    cursor="hand2",
    command=clear_tasks
)
clear_button.grid(
    row=0,
    column=2,
    padx=5,
    ipadx=10,
    ipady=6
)


status_label = tk.Label(
    main_frame,
    text="Ready",
    font=("Arial", 10),
    bg="#243B63",
    fg="#E0E0E0"
)
status_label.pack(pady=(5, 15))


update_list()

root.mainloop()