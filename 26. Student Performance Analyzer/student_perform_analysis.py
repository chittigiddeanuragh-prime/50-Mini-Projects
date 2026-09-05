import tkinter as tk
from tkinter import messagebox, filedialog
import json


SUBJECTS = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Computer Science",
    "English"
]

BG = "#111827"
PANEL = "#1F2937"
CARD = "#273449"
INPUT = "#0F172A"
TEXT = "#F9FAFB"
MUTED = "#9CA3AF"
TEAL = "#2DD4BF"
BLUE = "#60A5FA"
PURPLE = "#A78BFA"
ORANGE = "#FB923C"
GREEN = "#4ADE80"
RED = "#F87171"
YELLOW = "#FACC15"
BORDER = "#374151"


class StudentPerformanceAnalyzer:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Analyzer")
        self.root.geometry("1150x850")
        self.root.minsize(900, 700)
        self.root.configure(bg=BG)

        self.entries = {}
        self.result_data = {}

        self.create_header()
        self.create_bottom_bar()
        self.create_main_area()

    def create_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=25, pady=(18, 8))

        tk.Label(
            header,
            text="STUDENT PERFORMANCE ANALYZER",
            font=("Arial", 23, "bold"),
            fg=TEXT,
            bg=BG
        ).pack()

        tk.Label(
            header,
            text="Enter your marks and analyze your academic performance",
            font=("Arial", 10),
            fg=MUTED,
            bg=BG
        ).pack(pady=(4, 0))

    def create_bottom_bar(self):
        bottom_bar = tk.Frame(
            self.root,
            bg=PANEL,
            height=70,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        bottom_bar.pack(side="bottom", fill="x", padx=25, pady=(8, 18))
        bottom_bar.pack_propagate(False)

        tk.Button(
            bottom_bar,
            text="SAVE RESULTS",
            command=self.save_data,
            font=("Arial", 10, "bold"),
            bg=BLUE,
            fg=BG,
            activebackground="#3B82F6",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 5),
            pady=15
        )

        tk.Button(
            bottom_bar,
            text="LOAD RESULTS",
            command=self.load_data,
            font=("Arial", 10, "bold"),
            bg=ORANGE,
            fg=BG,
            activebackground="#F97316",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=15
        )

        tk.Button(
            bottom_bar,
            text="RESET",
            command=self.reset,
            font=("Arial", 10, "bold"),
            bg=RED,
            fg=TEXT,
            activebackground="#EF4444",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 15),
            pady=15
        )

    def create_main_area(self):
        container = tk.Frame(self.root, bg=BG)
        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=5
        )

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)

        self.create_input_panel(container)
        self.create_analysis_panel(container)

    def create_input_panel(self, parent):
        panel = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        tk.Label(
            panel,
            text="ENTER MARKS",
            font=("Arial", 16, "bold"),
            fg=TEAL,
            bg=PANEL
        ).pack(pady=(18, 3))

        tk.Label(
            panel,
            text="Enter marks between 0 and 100",
            font=("Arial", 9),
            fg=MUTED,
            bg=PANEL
        ).pack(pady=(0, 12))

        for subject in SUBJECTS:

            row = tk.Frame(panel, bg=PANEL)
            row.pack(
                fill="x",
                padx=22,
                pady=5
            )

            tk.Label(
                row,
                text=subject,
                font=("Arial", 10, "bold"),
                fg=TEXT,
                bg=PANEL,
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

            entry = tk.Entry(
                row,
                font=("Arial", 11, "bold"),
                width=7,
                justify="center",
                bg=INPUT,
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )

            entry.pack(
                side="right",
                ipady=5
            )

            self.entries[subject] = entry

        tk.Label(
            panel,
            text="TARGET PERCENTAGE",
            font=("Arial", 12, "bold"),
            fg=PURPLE,
            bg=PANEL
        ).pack(pady=(15, 5))

        self.target_entry = tk.Entry(
            panel,
            font=("Arial", 11, "bold"),
            justify="center",
            bg=INPUT,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )

        self.target_entry.pack(
            fill="x",
            padx=45,
            ipady=6
        )

        self.target_entry.insert(0, "90")

        tk.Button(
            panel,
            text="CALCULATE PERFORMANCE",
            command=self.calculate,
            font=("Arial", 10, "bold"),
            bg=TEAL,
            fg=BG,
            activebackground="#14B8A6",
            relief="flat",
            cursor="hand2"
        ).pack(
            fill="x",
            padx=22,
            pady=(15, 5),
            ipady=8
        )

        tk.Button(
            panel,
            text="CALCULATE TARGET",
            command=self.calculate_target,
            font=("Arial", 10, "bold"),
            bg=PURPLE,
            fg=TEXT,
            activebackground="#8B5CF6",
            relief="flat",
            cursor="hand2"
        ).pack(
            fill="x",
            padx=22,
            pady=5,
            ipady=8
        )

    def create_analysis_panel(self, parent):

        panel = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        tk.Label(
            panel,
            text="PERFORMANCE ANALYSIS",
            font=("Arial", 16, "bold"),
            fg=BLUE,
            bg=PANEL
        ).pack(pady=(18, 10))

        cards = tk.Frame(panel, bg=PANEL)
        cards.pack(
            fill="x",
            padx=18
        )

        self.total_value = self.create_card(
            cards,
            "TOTAL",
            "0 / 500",
            TEAL
        )

        self.percentage_value = self.create_card(
            cards,
            "PERCENTAGE",
            "0%",
            BLUE
        )

        self.grade_value = self.create_card(
            cards,
            "GRADE",
            "-",
            PURPLE
        )

        self.status_value = self.create_card(
            cards,
            "STATUS",
            "-",
            GREEN
        )

        tk.Label(
            panel,
            text="SUBJECT PERFORMANCE",
            font=("Arial", 12, "bold"),
            fg=TEXT,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=22,
            pady=(15, 6)
        )

        self.performance_frame = tk.Frame(
            panel,
            bg=PANEL
        )

        self.performance_frame.pack(
            fill="x",
            padx=22
        )

        tk.Label(
            panel,
            text="INSIGHTS",
            font=("Arial", 12, "bold"),
            fg=YELLOW,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=22,
            pady=(15, 5)
        )

        self.insights_text = tk.Text(
            panel,
            height=7,
            font=("Arial", 9),
            bg=INPUT,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            wrap="word"
        )

        self.insights_text.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 8)
        )

        self.insights_text.insert(
            "1.0",
            "Enter your marks and click 'CALCULATE PERFORMANCE' "
            "to see your analysis."
        )

        self.insights_text.config(
            state="disabled"
        )

        self.target_result = tk.Label(
            panel,
            text="Target analysis will appear here.",
            font=("Arial", 9, "bold"),
            fg=MUTED,
            bg=PANEL
        )

        self.target_result.pack(
            pady=(0, 12)
        )

    def create_card(self, parent, title, value, color):

        card = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=3
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 8, "bold"),
            fg=MUTED,
            bg=CARD
        ).pack(
            pady=(8, 2)
        )

        label = tk.Label(
            card,
            text=value,
            font=("Arial", 13, "bold"),
            fg=color,
            bg=CARD
        )

        label.pack(
            pady=(0, 8)
        )

        return label

    def get_marks(self):

        marks = {}

        for subject, entry in self.entries.items():

            value = entry.get().strip()

            if not value:
                raise ValueError(
                    f"Please enter marks for {subject}."
                )

            try:
                mark = float(value)
            except ValueError:
                raise ValueError(
                    f"Marks for {subject} must be a number."
                )

            if mark < 0 or mark > 100:
                raise ValueError(
                    f"Marks for {subject} must be between 0 and 100."
                )

            marks[subject] = mark

        return marks

    def calculate(self):

        try:
            marks = self.get_marks()
        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error)
            )
            return

        total = sum(marks.values())
        percentage = total / len(SUBJECTS)

        grade = self.get_grade(percentage)

        passed = all(
            mark >= 35
            for mark in marks.values()
        )

        status = "PASS" if passed else "FAIL"

        self.total_value.config(
            text=f"{total:g} / 500"
        )

        self.percentage_value.config(
            text=f"{percentage:.1f}%"
        )

        self.grade_value.config(
            text=grade
        )

        self.status_value.config(
            text=status,
            fg=GREEN if passed else RED
        )

        self.update_subject_bars(marks)

        self.generate_insights(
            marks,
            percentage,
            grade,
            passed
        )

        self.result_data = {
            "marks": marks,
            "total": total,
            "percentage": percentage,
            "grade": grade,
            "status": status
        }

        self.calculate_target()

    def get_grade(self, percentage):

        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        else:
            return "F"

    def update_subject_bars(self, marks):

        for widget in self.performance_frame.winfo_children():
            widget.destroy()

        for subject, mark in sorted(
            marks.items(),
            key=lambda item: item[1],
            reverse=True
        ):

            row = tk.Frame(
                self.performance_frame,
                bg=PANEL
            )

            row.pack(
                fill="x",
                pady=3
            )

            tk.Label(
                row,
                text=subject,
                font=("Arial", 8, "bold"),
                fg=TEXT,
                bg=PANEL,
                width=17,
                anchor="w"
            ).pack(side="left")

            bar_background = tk.Frame(
                row,
                bg=INPUT,
                height=13
            )

            bar_background.pack(
                side="left",
                fill="x",
                expand=True,
                padx=6
            )

            bar_background.pack_propagate(False)

            if mark >= 75:
                bar_color = GREEN
            elif mark >= 50:
                bar_color = YELLOW
            else:
                bar_color = RED

            bar = tk.Frame(
                bar_background,
                bg=bar_color
            )

            bar.place(
                relx=0,
                rely=0,
                relheight=1,
                relwidth=mark / 100
            )

            tk.Label(
                row,
                text=f"{mark:g}%",
                font=("Arial", 8, "bold"),
                fg=TEXT,
                bg=PANEL,
                width=6
            ).pack(side="right")

    def generate_insights(
        self,
        marks,
        percentage,
        grade,
        passed
    ):

        strongest = max(
            marks,
            key=marks.get
        )

        weakest = min(
            marks,
            key=marks.get
        )

        excellent = [
            subject
            for subject, mark in marks.items()
            if mark >= 90
        ]

        weak = [
            subject
            for subject, mark in marks.items()
            if mark < 50
        ]

        failed = [
            subject
            for subject, mark in marks.items()
            if mark < 35
        ]

        recommendations = []

        for subject, mark in marks.items():

            if mark < 35:
                recommendations.append(
                    f"{subject}: Immediate attention required. "
                    f"Revise the basics and practice daily."
                )

            elif mark < 50:
                recommendations.append(
                    f"{subject}: Needs improvement. "
                    f"Spend extra study time and solve practice questions."
                )

            elif mark < 75:
                recommendations.append(
                    f"{subject}: Good foundation. "
                    f"Practice more to move toward 75+."
                )

            else:
                recommendations.append(
                    f"{subject}: Strong performance. "
                    f"Continue regular revision."
                )

        lines = [
            f"Overall Performance: {percentage:.1f}% ({grade})",
            f"Status: {'PASS' if passed else 'FAIL'}",
            "",
            f"Strongest Subject: {strongest} "
            f"({marks[strongest]:g}%)",
            f"Needs Most Attention: {weakest} "
            f"({marks[weakest]:g}%)",
            ""
        ]

        if excellent:
            lines.append(
                "Excellent Subjects: "
                + ", ".join(excellent)
            )

        if weak:
            lines.append(
                "Subjects Below 50%: "
                + ", ".join(weak)
            )

        if failed:
            lines.append(
                "Subjects Below Passing: "
                + ", ".join(failed)
            )

        lines.extend([
            "",
            "STUDY RECOMMENDATIONS",
            "----------------------"
        ])

        lines.extend(
            recommendations
        )

        lines.append("")

        if percentage >= 90:

            lines.append(
                "Overall Advice: Excellent work! "
                "Focus on maintaining consistency."
            )

        elif percentage >= 75:

            lines.append(
                "Overall Advice: Very good performance. "
                "Focus on weaker subjects to improve further."
            )

        elif percentage >= 50:

            lines.append(
                "Overall Advice: Your foundation is developing. "
                "Create a daily study schedule."
            )

        else:

            lines.append(
                "Overall Advice: Start with the basics, "
                "revise regularly, and practice every day."
            )

        self.insights_text.config(
            state="normal"
        )

        self.insights_text.delete(
            "1.0",
            tk.END
        )

        self.insights_text.insert(
            "1.0",
            "\n".join(lines)
        )

        self.insights_text.config(
            state="disabled"
        )

    def calculate_target(self):

        try:
            marks = self.get_marks()
        except ValueError:
            return

        try:
            target = float(
                self.target_entry.get()
            )
        except ValueError:

            messagebox.showerror(
                "Invalid Target",
                "Please enter a valid target percentage."
            )

            return

        if target < 0 or target > 100:

            messagebox.showerror(
                "Invalid Target",
                "Target percentage must be between 0 and 100."
            )

            return

        current_total = sum(
            marks.values()
        )

        required_total = (
            target * len(SUBJECTS)
        )

        difference = (
            required_total - current_total
        )

        if difference <= 0:

            self.target_result.config(
                text=(
                    f"Target {target:g}% achieved! "
                    f"You are {abs(difference):.1f} "
                    f"marks above the target."
                ),
                fg=GREEN
            )

        else:

            self.target_result.config(
                text=(
                    f"To reach {target:g}%, you need "
                    f"{difference:.1f} more total marks."
                ),
                fg=YELLOW
            )

    def save_data(self):

        try:
            marks = self.get_marks()
        except ValueError as error:

            messagebox.showerror(
                "Cannot Save",
                str(error)
            )

            return

        data = {
            "marks": marks,
            "target_percentage":
                self.target_entry.get()
        }

        filename = filedialog.asksaveasfilename(
            title="Save Student Results",
            defaultextension=".json",
            filetypes=[
                ("JSON Files", "*.json")
            ]
        )

        if not filename:
            return

        try:

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            messagebox.showinfo(
                "Saved",
                "Student results saved successfully."
            )

        except OSError as error:

            messagebox.showerror(
                "Save Error",
                f"Could not save the file.\n{error}"
            )

    def load_data(self):

        filename = filedialog.askopenfilename(
            title="Load Student Results",
            filetypes=[
                ("JSON Files", "*.json")
            ]
        )

        if not filename:
            return

        try:

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            marks = data.get(
                "marks",
                {}
            )

            for subject in SUBJECTS:

                if subject not in marks:
                    raise ValueError(
                        "Invalid student result file."
                    )

                self.entries[subject].delete(
                    0,
                    tk.END
                )

                self.entries[subject].insert(
                    0,
                    str(marks[subject])
                )

            target = data.get(
                "target_percentage",
                "90"
            )

            self.target_entry.delete(
                0,
                tk.END
            )

            self.target_entry.insert(
                0,
                str(target)
            )

            self.calculate()

            messagebox.showinfo(
                "Loaded",
                "Student results loaded successfully."
            )

        except (
            OSError,
            json.JSONDecodeError,
            ValueError
        ) as error:

            messagebox.showerror(
                "Load Error",
                f"Could not load the file.\n{error}"
            )

    def reset(self):

        for entry in self.entries.values():
            entry.delete(
                0,
                tk.END
            )

        self.target_entry.delete(
            0,
            tk.END
        )

        self.target_entry.insert(
            0,
            "90"
        )

        self.total_value.config(
            text="0 / 500"
        )

        self.percentage_value.config(
            text="0%"
        )

        self.grade_value.config(
            text="-"
        )

        self.status_value.config(
            text="-",
            fg=GREEN
        )

        for widget in self.performance_frame.winfo_children():
            widget.destroy()

        self.insights_text.config(
            state="normal"
        )

        self.insights_text.delete(
            "1.0",
            tk.END
        )

        self.insights_text.insert(
            "1.0",
            "Enter your marks and click "
            "'CALCULATE PERFORMANCE' "
            "to see your analysis."
        )

        self.insights_text.config(
            state="disabled"
        )

        self.target_result.config(
            text="Target analysis will appear here.",
            fg=MUTED
        )

        self.result_data = {}


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentPerformanceAnalyzer(root)
    root.mainloop()