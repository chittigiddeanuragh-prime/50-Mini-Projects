import tkinter as tk
from tkinter import messagebox


class BankAccount:
    def __init__(self):
        self.balance = 0.0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount <= 0:
            return "invalid"

        if amount > self.balance:
            return "insufficient"

        self.balance -= amount
        return "success"


account = BankAccount()


def update_balance():
    balance_label.config(
        text=f"₹ {account.balance:,.2f}"
    )


def deposit_money():
    try:
        amount = float(amount_entry.get())

        if account.deposit(amount):
            update_balance()
            amount_entry.delete(0, tk.END)

            status_label.config(
                text="Amount deposited successfully.",
                fg="#00A9E0"
            )

        else:
            status_label.config(
                text="Enter a valid amount.",
                fg="#E63946"
            )

    except ValueError:
        status_label.config(
            text="Please enter a valid number.",
            fg="#E63946"
        )


def withdraw_money():
    try:
        amount = float(amount_entry.get())
        result = account.withdraw(amount)

        if result == "success":
            update_balance()
            amount_entry.delete(0, tk.END)

            status_label.config(
                text="Amount withdrawn successfully.",
                fg="#00A9E0"
            )

        elif result == "insufficient":
            status_label.config(
                text="Insufficient balance.",
                fg="#E63946"
            )

        else:
            status_label.config(
                text="Enter a valid amount.",
                fg="#E63946"
            )

    except ValueError:
        status_label.config(
            text="Please enter a valid number.",
            fg="#E63946"
        )


def check_balance():
    messagebox.showinfo(
        "Account Balance",
        f"Your current balance is:\n\n₹ {account.balance:,.2f}"
    )


def clear_amount():
    amount_entry.delete(0, tk.END)

    status_label.config(
        text="Ready",
        fg="#FFFFFF"
    )


root = tk.Tk()
root.title("SBI Bank Account Simulator")
root.geometry("900x800")
root.minsize(700, 650)
root.resizable(True, True)
root.configure(bg="#00529B")


header = tk.Frame(
    root,
    bg="#003F7D",
    height=120
)

header.pack(
    fill="x"
)


bank_name = tk.Label(
    header,
    text="STATE BANK",
    font=("Arial", 28, "bold"),
    bg="#003F7D",
    fg="#FFFFFF"
)

bank_name.pack(
    pady=(25, 0)
)


bank_subtitle = tk.Label(
    header,
    text="Bank Account Simulator",
    font=("Arial", 12),
    bg="#003F7D",
    fg="#9DDAF5"
)

bank_subtitle.pack(
    pady=(2, 20)
)


main_frame = tk.Frame(
    root,
    bg="#F4F8FC",
    bd=0
)

main_frame.pack(
    padx=55,
    pady=35,
    fill="both",
    expand=True
)


welcome_label = tk.Label(
    main_frame,
    text="Welcome to Your Account",
    font=("Arial", 24, "bold"),
    bg="#F4F8FC",
    fg="#003F7D"
)

welcome_label.pack(
    pady=(35, 5)
)


account_label = tk.Label(
    main_frame,
    text="Savings Account • Account Simulator",
    font=("Arial", 11),
    bg="#F4F8FC",
    fg="#52718B"
)

account_label.pack(
    pady=(0, 25)
)


balance_frame = tk.Frame(
    main_frame,
    bg="#0072BC",
    highlightbackground="#00A9E0",
    highlightthickness=2
)

balance_frame.pack(
    padx=80,
    fill="x"
)


balance_title = tk.Label(
    balance_frame,
    text="AVAILABLE BALANCE",
    font=("Arial", 11, "bold"),
    bg="#0072BC",
    fg="#D8F3FF"
)

balance_title.pack(
    pady=(20, 5)
)


balance_label = tk.Label(
    balance_frame,
    text="₹ 0.00",
    font=("Arial", 32, "bold"),
    bg="#0072BC",
    fg="#FFFFFF"
)

balance_label.pack(
    pady=(0, 20)
)


amount_label = tk.Label(
    main_frame,
    text="Enter Amount",
    font=("Arial", 13, "bold"),
    bg="#F4F8FC",
    fg="#003F7D"
)

amount_label.pack(
    pady=(30, 8)
)


amount_entry = tk.Entry(
    main_frame,
    font=("Arial", 17),
    justify="center",
    bg="#FFFFFF",
    fg="#003F7D",
    insertbackground="#003F7D",
    relief="solid",
    bd=1,
    width=25
)

amount_entry.pack(
    ipady=10
)


button_frame = tk.Frame(
    main_frame,
    bg="#F4F8FC"
)

button_frame.pack(
    pady=25
)


deposit_button = tk.Button(
    button_frame,
    text="Deposit",
    font=("Arial", 12, "bold"),
    bg="#00A9E0",
    fg="#FFFFFF",
    activebackground="#008FC0",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=deposit_money
)

deposit_button.grid(
    row=0,
    column=0,
    padx=8,
    ipadx=30,
    ipady=10
)


withdraw_button = tk.Button(
    button_frame,
    text="Withdraw",
    font=("Arial", 12, "bold"),
    bg="#00529B",
    fg="#FFFFFF",
    activebackground="#003F7D",
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=withdraw_money
)

withdraw_button.grid(
    row=0,
    column=1,
    padx=8,
    ipadx=30,
    ipady=10
)


balance_button = tk.Button(
    button_frame,
    text="Check Balance",
    font=("Arial", 12, "bold"),
    bg="#F4C430",
    fg="#003F7D",
    activebackground="#DDB020",
    activeforeground="#003F7D",
    relief="flat",
    cursor="hand2",
    command=check_balance
)

balance_button.grid(
    row=0,
    column=2,
    padx=8,
    ipadx=25,
    ipady=10
)


clear_button = tk.Button(
    main_frame,
    text="Clear Amount",
    font=("Arial", 10, "bold"),
    bg="#DCEAF5",
    fg="#003F7D",
    activebackground="#C5DCEB",
    activeforeground="#003F7D",
    relief="flat",
    cursor="hand2",
    command=clear_amount
)

clear_button.pack(
    ipadx=20,
    ipady=7
)


status_label = tk.Label(
    main_frame,
    text="Ready",
    font=("Arial", 11),
    bg="#F4F8FC",
    fg="#FFFFFF"
)

status_label.pack(
    pady=20
)


info_frame = tk.Frame(
    main_frame,
    bg="#E6F3FA"
)

info_frame.pack(
    padx=80,
    pady=(5, 30),
    fill="x"
)


info_label = tk.Label(
    info_frame,
    text="Deposit money to increase your balance.\n"
         "Withdraw money only when sufficient balance is available.",
    font=("Arial", 10),
    bg="#E6F3FA",
    fg="#36566D",
    justify="center"
)

info_label.pack(
    pady=15
)


root.mainloop()