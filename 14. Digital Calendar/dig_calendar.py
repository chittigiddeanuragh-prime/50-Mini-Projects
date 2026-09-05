import tkinter as tk
import calendar
from datetime import datetime


class DigitalCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Calendar")
        self.root.geometry("900x800")
        self.root.minsize(750, 650)
        self.root.resizable(True, True)
        self.root.configure(bg="#0B0F0C")

        self.current_date = datetime.now()
        self.year = self.current_date.year
        self.month = self.current_date.month

        self.create_interface()
        self.show_calendar()

    def create_interface(self):
        self.title_label = tk.Label(
            self.root,
            text="Digital Calendar",
            font=("Arial", 32, "bold"),
            bg="#0B0F0C",
            fg="#B7FF9A"
        )
        self.title_label.pack(pady=(30, 5))

        self.today_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            bg="#0B0F0C",
            fg="#8EDC76"
        )
        self.today_label.pack(pady=(0, 20))

        top_frame = tk.Frame(
            self.root,
            bg="#172019"
        )
        top_frame.pack(
            padx=45,
            fill="x"
        )

        previous_button = tk.Button(
            top_frame,
            text="← Previous",
            font=("Arial", 12, "bold"),
            bg="#29452C",
            fg="#B7FF9A",
            activebackground="#3B633F",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.previous_month
        )
        previous_button.pack(
            side="left",
            padx=15,
            pady=15,
            ipadx=15,
            ipady=8
        )

        self.month_label = tk.Label(
            top_frame,
            text="",
            font=("Arial", 22, "bold"),
            bg="#172019",
            fg="#FFFFFF"
        )
        self.month_label.pack(
            side="left",
            expand=True
        )

        next_button = tk.Button(
            top_frame,
            text="Next →",
            font=("Arial", 12, "bold"),
            bg="#29452C",
            fg="#B7FF9A",
            activebackground="#3B633F",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.next_month
        )
        next_button.pack(
            side="right",
            padx=15,
            pady=15,
            ipadx=15,
            ipady=8
        )

        today_button = tk.Button(
            self.root,
            text="Go to Today",
            font=("Arial", 11, "bold"),
            bg="#B7FF9A",
            fg="#0B0F0C",
            activebackground="#D0FFBC",
            activeforeground="#0B0F0C",
            relief="flat",
            cursor="hand2",
            command=self.go_to_today
        )
        today_button.pack(
            pady=18,
            ipadx=25,
            ipady=8
        )

        self.calendar_frame = tk.Frame(
            self.root,
            bg="#172019",
            bd=2,
            relief="solid",
            highlightbackground="#6EA85D",
            highlightthickness=1
        )
        self.calendar_frame.pack(
            padx=45,
            pady=(0, 30),
            fill="both",
            expand=True
        )

    def show_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        month_name = calendar.month_name[self.month]

        self.month_label.config(
            text=f"{month_name} {self.year}"
        )

        today = datetime.now()

        self.today_label.config(
            text=f"Today: {today.strftime('%A, %d %B %Y')}"
        )

        weekdays = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]

        for column, day in enumerate(weekdays):
            label = tk.Label(
                self.calendar_frame,
                text=day,
                font=("Arial", 12, "bold"),
                bg="#29452C",
                fg="#B7FF9A",
                relief="solid",
                bd=1
            )
            label.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=1,
                pady=1,
                ipady=12
            )

        month_days = calendar.monthcalendar(
            self.year,
            self.month
        )

        for row, week in enumerate(month_days, start=1):
            for column, day in enumerate(week):
                if day == 0:
                    day_text = ""
                    background = "#111711"
                    foreground = "#111711"

                else:
                    day_text = str(day)
                    background = "#111711"
                    foreground = "#FFFFFF"

                    if (
                        day == today.day
                        and self.month == today.month
                        and self.year == today.year
                    ):
                        background = "#B7FF9A"
                        foreground = "#0B0F0C"

                label = tk.Label(
                    self.calendar_frame,
                    text=day_text,
                    font=("Arial", 16, "bold"),
                    bg=background,
                    fg=foreground,
                    relief="solid",
                    bd=1
                )

                label.grid(
                    row=row,
                    column=column,
                    sticky="nsew",
                    padx=1,
                    pady=1
                )

        for column in range(7):
            self.calendar_frame.columnconfigure(
                column,
                weight=1
            )

        for row in range(len(month_days) + 1):
            self.calendar_frame.rowconfigure(
                row,
                weight=1
            )

    def previous_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1

        self.show_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1

        self.show_calendar()

    def go_to_today(self):
        today = datetime.now()
        self.year = today.year
        self.month = today.month
        self.show_calendar()


root = tk.Tk()
app = DigitalCalendar(root)
root.mainloop()