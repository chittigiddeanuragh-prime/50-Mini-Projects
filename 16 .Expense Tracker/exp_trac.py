import tkinter as tk
import json
import os
from datetime import datetime


FILE_NAME = "expenses.json"

BG_COLOR = "#0F172A"
PANEL_COLOR = "#1E293B"
INPUT_COLOR = "#0B1220"
PRIMARY_COLOR = "#14B8A6"
PRIMARY_HOVER = "#0D9488"
SECONDARY_COLOR = "#38BDF8"
TEXT_COLOR = "#F8FAFC"
MUTED_COLOR = "#94A3B8"
SUCCESS_COLOR = "#22C55E"
ERROR_COLOR = "#EF4444"
BORDER_COLOR = "#334155"


def load_expenses():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    return []


def save_expenses():
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


def update_summary():
    total = sum(item["amount"] for item in expenses)

    if expenses:
        average = total / len(expenses)
    else:
        average = 0

    total_label.config(text=f"₹{total:,.2f}")
    average_label.config(text=f"₹{average:,.2f}")
    count_label.config(text=str(len(expenses)))


def update_list():
    expense_list.delete(0, tk.END)

    for item in expenses:
        text = (
            f"{item['date']}   |   "
            f"{item['category']:<15}   |   "
            f"{item['description']:<25}   |   "
            f"₹{item['amount']:,.2f}"
        )

        expense_list.insert(tk.END, text)


def add_expense():
    description = description_entry.get().strip()
    amount_text = amount_entry.get().strip()
    category = category_var.get()

    if not description:
        status_label.config(
            text="Please enter an expense description.",
            fg=ERROR_COLOR
        )
        return

    try:
        amount = float(amount_text)

        if amount <= 0:
            raise ValueError

    except ValueError:
        status_label.config(
            text="Please enter a valid positive amount.",
            fg=ERROR_COLOR
        )
        return

    expense = {
        "date": datetime.now().strftime("%d-%m-%Y"),
        "description": description,
        "category": category,
        "amount": amount
    }

    expenses.append(expense)

    save_expenses()
    update_list()
    update_summary()

    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    status_label.config(
        text="Expense added successfully.",
        fg=SUCCESS_COLOR
    )


def delete_expense():
    selected = expense_list.curselection()

    if not selected:
        status_label.config(
            text="Select an expense to delete.",
            fg=ERROR_COLOR
        )
        return

    index = selected[0]

    expenses.pop(index)

    save_expenses()
    update_list()
    update_summary()

    status_label.config(
        text="Expense deleted.",
        fg=SUCCESS_COLOR
    )


def clear_expenses():
    if not expenses:
        status_label.config(
            text="There are no expenses to clear.",
            fg=MUTED_COLOR
        )
        return

    expenses.clear()

    save_expenses()
    update_list()
    update_summary()

    status_label.config(
        text="All expenses cleared.",
        fg=SUCCESS_COLOR
    )


def add_with_enter(event):
    add_expense()


expenses = load_expenses()


root = tk.Tk()
root.title("Expense Tracker")
root.geometry("900x800")
root.minsize(750, 650)
root.resizable(True, True)
root.configure(bg=BG_COLOR)


title = tk.Label(
    root,
    text="Expense Tracker",
    font=("Arial", 32, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title.pack(pady=(30, 5))


subtitle = tk.Label(
    root,
    text="Track your spending and manage your expenses",
    font=("Arial", 13),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)
subtitle.pack(pady=(0, 25))


summary_frame = tk.Frame(
    root,
    bg=BG_COLOR
)
summary_frame.pack(
    padx=50,
    fill="x"
)


def create_summary_card(parent, title_text, variable_label, accent):
    card = tk.Frame(
        parent,
        bg=PANEL_COLOR,
        bd=1,
        relief="solid",
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    card.pack(
        side="left",
        expand=True,
        fill="x",
        padx=6
    )

    title = tk.Label(
        card,
        text=title_text,
        font=("Arial", 11, "bold"),
        bg=PANEL_COLOR,
        fg=MUTED_COLOR
    )
    title.pack(pady=(18, 5))

    value = tk.Label(
        card,
        text="₹0.00",
        font=("Arial", 20, "bold"),
        bg=PANEL_COLOR,
        fg=accent
    )
    value.pack(pady=(0, 18))

    return value


total_label = create_summary_card(
    summary_frame,
    "TOTAL SPENDING",
    "total",
    PRIMARY_COLOR
)

average_label = create_summary_card(
    summary_frame,
    "AVERAGE EXPENSE",
    "average",
    SECONDARY_COLOR
)

count_label = create_summary_card(
    summary_frame,
    "NUMBER OF EXPENSES",
    "count",
    SUCCESS_COLOR
)


main_frame = tk.Frame(
    root,
    bg=PANEL_COLOR,
    bd=1,
    relief="solid",
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

main_frame.pack(
    padx=50,
    pady=25,
    fill="both",
    expand=True
)


input_frame = tk.Frame(
    main_frame,
    bg=PANEL_COLOR
)

input_frame.pack(
    padx=30,
    pady=25,
    fill="x"
)


description_label = tk.Label(
    input_frame,
    text="Description",
    font=("Arial", 11, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

description_label.grid(
    row=0,
    column=0,
    sticky="w",
    padx=8,
    pady=(0, 7)
)


amount_label = tk.Label(
    input_frame,
    text="Amount",
    font=("Arial", 11, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

amount_label.grid(
    row=0,
    column=1,
    sticky="w",
    padx=8,
    pady=(0, 7)
)


category_label = tk.Label(
    input_frame,
    text="Category",
    font=("Arial", 11, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

category_label.grid(
    row=0,
    column=2,
    sticky="w",
    padx=8,
    pady=(0, 7)
)


description_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="solid",
    bd=1
)

description_entry.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=8,
    ipady=9
)


amount_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="solid",
    bd=1
)

amount_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=8,
    ipady=9
)


category_var = tk.StringVar()
category_var.set("Food")


category_menu = tk.OptionMenu(
    input_frame,
    category_var,
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Education",
    "Other"
)

category_menu.config(
    font=("Arial", 11),
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    activebackground=PRIMARY_COLOR,
    activeforeground=TEXT_COLOR,
    relief="solid",
    bd=1
)

category_menu["menu"].config(
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    activebackground=PRIMARY_COLOR,
    activeforeground=TEXT_COLOR
)

category_menu.grid(
    row=1,
    column=2,
    sticky="ew",
    padx=8,
    ipady=6
)


input_frame.columnconfigure(0, weight=3)
input_frame.columnconfigure(1, weight=2)
input_frame.columnconfigure(2, weight=2)


description_entry.bind("<Return>", add_with_enter)
amount_entry.bind("<Return>", add_with_enter)


add_button = tk.Button(
    input_frame,
    text="Add Expense",
    font=("Arial", 11, "bold"),
    bg=PRIMARY_COLOR,
    fg=TEXT_COLOR,
    activebackground=PRIMARY_HOVER,
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    command=add_expense
)

add_button.grid(
    row=1,
    column=3,
    padx=8,
    ipadx=18,
    ipady=8
)


list_label = tk.Label(
    main_frame,
    text="Expense History",
    font=("Arial", 14, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

list_label.pack(
    anchor="w",
    padx=38,
    pady=(5, 10)
)


list_frame = tk.Frame(
    main_frame,
    bg=INPUT_COLOR
)

list_frame.pack(
    padx=35,
    fill="both",
    expand=True
)


scrollbar = tk.Scrollbar(
    list_frame,
    orient="vertical"
)

scrollbar.pack(
    side="right",
    fill="y"
)


expense_list = tk.Listbox(
    list_frame,
    font=("Consolas", 11),
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    selectbackground=PRIMARY_COLOR,
    selectforeground=TEXT_COLOR,
    relief="flat",
    bd=0,
    yscrollcommand=scrollbar.set
)

expense_list.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

scrollbar.config(
    command=expense_list.yview
)


button_frame = tk.Frame(
    main_frame,
    bg=PANEL_COLOR
)

button_frame.pack(
    pady=20
)


delete_button = tk.Button(
    button_frame,
    text="Delete Selected",
    font=("Arial", 10, "bold"),
    bg="#334155",
    fg=TEXT_COLOR,
    activebackground="#475569",
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    command=delete_expense
)

delete_button.grid(
    row=0,
    column=0,
    padx=6,
    ipadx=18,
    ipady=8
)


clear_button = tk.Button(
    button_frame,
    text="Clear All",
    font=("Arial", 10, "bold"),
    bg=ERROR_COLOR,
    fg=TEXT_COLOR,
    activebackground="#DC2626",
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    command=clear_expenses
)

clear_button.grid(
    row=0,
    column=1,
    padx=6,
    ipadx=25,
    ipady=8
)


status_label = tk.Label(
    main_frame,
    text="Ready",
    font=("Arial", 10),
    bg=PANEL_COLOR,
    fg=MUTED_COLOR
)

status_label.pack(
    pady=(0, 18)
)


update_list()
update_summary()

root.mainloop()