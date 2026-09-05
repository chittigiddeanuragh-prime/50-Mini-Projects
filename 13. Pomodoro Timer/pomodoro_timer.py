import tkinter as tk


WORK_TIME = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60


class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("750x850")
        self.root.minsize(650, 750)
        self.root.resizable(True, True)
        self.root.configure(bg="#241238")

        self.time_left = WORK_TIME
        self.running = False
        self.timer_id = None
        self.sessions = 0
        self.mode = "Work"

        title = tk.Label(
            root,
            text="Pomodoro Timer",
            font=("Arial", 32, "bold"),
            bg="#241238",
            fg="#FFB347"
        )
        title.pack(pady=(45, 5))

        subtitle = tk.Label(
            root,
            text="Work with focus. Take breaks. Get things done.",
            font=("Arial", 13),
            bg="#241238",
            fg="#D8B4FE"
        )
        subtitle.pack(pady=(0, 30))

        self.main_frame = tk.Frame(
            root,
            bg="#3A1D55",
            bd=2,
            relief="solid",
            highlightbackground="#FF8C42",
            highlightthickness=2
        )
        self.main_frame.pack(
            padx=50,
            pady=10,
            fill="both",
            expand=True
        )

        self.mode_label = tk.Label(
            self.main_frame,
            text="WORK SESSION",
            font=("Arial", 18, "bold"),
            bg="#3A1D55",
            fg="#FFB347"
        )
        self.mode_label.pack(pady=(50, 15))

        self.timer_label = tk.Label(
            self.main_frame,
            text="25:00",
            font=("Arial", 90, "bold"),
            bg="#3A1D55",
            fg="#FFFFFF"
        )
        self.timer_label.pack(pady=25)

        self.session_label = tk.Label(
            self.main_frame,
            text="Sessions completed: 0",
            font=("Arial", 14),
            bg="#3A1D55",
            fg="#D8B4FE"
        )
        self.session_label.pack(pady=10)

        self.start_button = tk.Button(
            self.main_frame,
            text="Start",
            font=("Arial", 14, "bold"),
            bg="#FF8C42",
            fg="#241238",
            activebackground="#FFB347",
            activeforeground="#241238",
            relief="flat",
            cursor="hand2",
            command=self.start_timer
        )
        self.start_button.pack(
            pady=30,
            ipadx=50,
            ipady=12
        )

        button_frame = tk.Frame(
            self.main_frame,
            bg="#3A1D55"
        )
        button_frame.pack(pady=10)

        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            font=("Arial", 12, "bold"),
            bg="#6D3FA3",
            fg="#FFFFFF",
            activebackground="#8756C4",
            relief="flat",
            cursor="hand2",
            command=self.pause_timer
        )
        self.pause_button.grid(
            row=0,
            column=0,
            padx=8,
            ipadx=25,
            ipady=9
        )

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            font=("Arial", 12, "bold"),
            bg="#B85C00",
            fg="#FFFFFF",
            activebackground="#D96F00",
            relief="flat",
            cursor="hand2",
            command=self.reset_timer
        )
        self.reset_button.grid(
            row=0,
            column=1,
            padx=8,
            ipadx=25,
            ipady=9
        )

        self.status_label = tk.Label(
            self.main_frame,
            text="Ready to focus",
            font=("Arial", 12),
            bg="#3A1D55",
            fg="#E5E5E5"
        )
        self.status_label.pack(pady=25)

        self.info_label = tk.Label(
            self.main_frame,
            text="25 min work  •  5 min short break  •  15 min long break",
            font=("Arial", 11),
            bg="#3A1D55",
            fg="#C4A7E7"
        )
        self.info_label.pack(pady=(5, 30))

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_button.config(text="Running...")
            self.status_label.config(text="Stay focused!")
            self.countdown()

    def countdown(self):
        if self.running and self.time_left > 0:
            minutes = self.time_left // 60
            seconds = self.time_left % 60

            self.timer_label.config(
                text=f"{minutes:02d}:{seconds:02d}"
            )

            self.time_left -= 1

            self.timer_id = self.root.after(
                1000,
                self.countdown
            )

        elif self.running and self.time_left == 0:
            self.running = False
            self.session_finished()

    def session_finished(self):
        if self.mode == "Work":
            self.sessions += 1

            self.session_label.config(
                text=f"Sessions completed: {self.sessions}"
            )

            if self.sessions % 4 == 0:
                self.mode = "Long Break"
                self.time_left = LONG_BREAK

                self.mode_label.config(
                    text="LONG BREAK",
                    fg="#D8B4FE"
                )

                self.status_label.config(
                    text="Great work! Take a longer break."
                )

            else:
                self.mode = "Short Break"
                self.time_left = SHORT_BREAK

                self.mode_label.config(
                    text="SHORT BREAK",
                    fg="#D8B4FE"
                )

                self.status_label.config(
                    text="Good job! Take a short break."
                )

        else:
            self.mode = "Work"
            self.time_left = WORK_TIME

            self.mode_label.config(
                text="WORK SESSION",
                fg="#FFB347"
            )

            self.status_label.config(
                text="Break finished. Time to focus!"
            )

        self.update_display()
        self.start_button.config(text="Start")

    def update_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60

        self.timer_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

    def pause_timer(self):
        if self.running:
            self.running = False

            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

            self.start_button.config(text="Start")
            self.status_label.config(text="Timer paused")

    def reset_timer(self):
        self.running = False

        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.mode = "Work"
        self.time_left = WORK_TIME
        self.sessions = 0

        self.mode_label.config(
            text="WORK SESSION",
            fg="#FFB347"
        )

        self.session_label.config(
            text="Sessions completed: 0"
        )

        self.status_label.config(
            text="Ready to focus"
        )

        self.start_button.config(
            text="Start"
        )

        self.update_display()


root = tk.Tk()
app = PomodoroTimer(root)
root.mainloop()