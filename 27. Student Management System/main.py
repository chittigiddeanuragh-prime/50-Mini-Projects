import tkinter as tk
import json
import re
from pathlib import Path
from tkinter import ttk, messagebox


# ============================================================
# STUDENT MANAGEMENT SYSTEM
# Modern, colorful, interactive Tkinter dashboard
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "students.json"

students = []
selected_student_id = None


# ============================================================
# COLOR PALETTE
# ============================================================

COLORS = {
    "navy": "#172033",
    "navy_2": "#202b42",
    "blue": "#2563eb",
    "blue_dark": "#1d4ed8",
    "cyan": "#0891b2",
    "green": "#16a34a",
    "green_dark": "#15803d",
    "orange": "#f59e0b",
    "orange_dark": "#d97706",
    "red": "#dc2626",
    "red_dark": "#b91c1c",
    "purple": "#7c3aed",
    "purple_dark": "#6d28d9",
    "bg": "#eef2f7",
    "card": "#ffffff",
    "text": "#172033",
    "muted": "#667085",
    "border": "#d9e0ea",
    "input": "#f8fafc",
    "white": "#ffffff",
    "success_bg": "#ecfdf3",
    "warning_bg": "#fffbeb",
    "danger_bg": "#fef2f2",
}


# ============================================================
# DATA / JSON DATABASE
# ============================================================

def load_students():
    """Load student records from the JSON database."""
    global students

    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not DATA_FILE.exists():
            DATA_FILE.write_text("[]", encoding="utf-8")
            students = []
            return

        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Keep only valid student dictionaries.
        if isinstance(data, list):
            students = [item for item in data if isinstance(item, dict)]
        else:
            students = []

    except (json.JSONDecodeError, OSError):
        students = []


def save_students():
    """Save all student records to the JSON database."""
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)

        return True

    except OSError:
        messagebox.showerror(
            "Database Error",
            "Could not save student records to the JSON database."
        )
        return False


load_students()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Student Management System")
root.geometry("1400x850")
root.minsize(1200, 760)
root.configure(bg=COLORS["bg"])


# ============================================================
# GLOBAL STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Treeview",
    rowheight=34,
    font=("Segoe UI", 9),
    background=COLORS["card"],
    fieldbackground=COLORS["card"],
    borderwidth=0,
    relief="flat",
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 9, "bold"),
    foreground=COLORS["white"],
    background=COLORS["navy_2"],
    padding=(8, 10),
    relief="flat",
)

style.map(
    "Treeview.Heading",
    background=[("active", COLORS["navy"])]
)

style.map(
    "Treeview",
    background=[("selected", "#dbeafe")],
    foreground=[("selected", COLORS["text"])]
)

style.configure(
    "Vertical.TScrollbar",
    troughcolor="#e5eaf1",
    background="#aab4c3",
    bordercolor="#e5eaf1",
    arrowcolor=COLORS["navy"],
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_hover_effect(button, normal_color, hover_color):
    """Add a smooth-looking color change when the mouse enters/leaves."""
    button.bind(
        "<Enter>",
        lambda event: button.config(bg=hover_color)
    )
    button.bind(
        "<Leave>",
        lambda event: button.config(bg=normal_color)
    )


def create_section_title(parent, icon, title_text, color):
    """Create a small colorful section heading."""
    frame = tk.Frame(parent, bg=COLORS["white"])
    frame.pack(fill="x", padx=18, pady=(16, 8))

    icon_label = tk.Label(
        frame,
        text=icon,
        font=("Segoe UI Emoji", 13),
        fg=color,
        bg=COLORS["white"],
    )
    icon_label.pack(side="left", padx=(0, 7))

    label = tk.Label(
        frame,
        text=title_text,
        font=("Segoe UI", 12, "bold"),
        fg=COLORS["text"],
        bg=COLORS["white"],
    )
    label.pack(side="left")

    return frame


def set_status(message, kind="info"):
    """Update the small status message at the bottom."""
    status_colors = {
        "info": ("#dbeafe", "#1d4ed8"),
        "success": ("#dcfce7", "#15803d"),
        "warning": ("#fef3c7", "#b45309"),
        "error": ("#fee2e2", "#b91c1c"),
    }

    bg, fg = status_colors.get(kind, status_colors["info"])
    status_message.config(text=message, bg=bg, fg=fg)


def update_record_count():
    records_status.config(text=f"Records: {len(students)}")


def refresh_department_filter():
    """Build the department filter from the departments in the database."""
    menu = department_menu["menu"]
    menu.delete(0, "end")

    departments = sorted(
        {
            str(student.get("department", "")).strip()
            for student in students
            if str(student.get("department", "")).strip()
        }
    )

    menu.add_command(
        label="All Departments",
        command=lambda: change_department_filter("All Departments")
    )

    for department in departments:
        menu.add_command(
            label=department,
            command=lambda value=department: change_department_filter(value)
        )


def change_department_filter(value):
    department_search_var.set(value)
    search_students(show_message=False)


def validate_student_data(
    student_id, name, age, gender, department, course, marks
):
    """Validate student form data before ADD or UPDATE."""

    if not all([student_id, name, age, gender, department, course, marks]):
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all student details."
        )
        return None

    if gender == "Select Gender":
        messagebox.showwarning(
            "Invalid Gender",
            "Please select a valid gender."
        )
        return None

    if not re.fullmatch(r"[A-Za-z0-9_-]+", student_id):
        messagebox.showerror(
            "Invalid Student ID",
            "Student ID can contain only letters, numbers, hyphens, and underscores."
        )
        return None

    if not re.fullmatch(r"[A-Za-z .'-]+", name):
        messagebox.showerror(
            "Invalid Name",
            "Name should contain letters, spaces, apostrophes, dots, or hyphens only."
        )
        return None

    try:
        age_value = int(age)
        if not 1 <= age_value <= 120:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Age",
            "Age must be a whole number between 1 and 120."
        )
        return None

    try:
        marks_value = float(marks)
        if not 0 <= marks_value <= 100:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Marks",
            "Marks must be a number between 0 and 100."
        )
        return None

    return age_value, marks_value


def student_id_exists(student_id, exclude_id=None):
    """Check whether a student ID already exists."""
    for student in students:
        current_id = str(student.get("id", ""))
        if exclude_id and current_id.lower() == exclude_id.lower():
            continue
        if current_id.lower() == student_id.lower():
            return True
    return False


# ============================================================
# FORM HELPERS
# ============================================================

student_id_var = tk.StringVar()
name_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar(value="Select Gender")
department_var = tk.StringVar()
course_var = tk.StringVar()
marks_var = tk.StringVar()


def create_field(parent, label_text, variable):
    """Create a clean input field with a focus effect."""

    wrapper = tk.Frame(parent, bg=COLORS["white"])
    wrapper.pack(fill="x", padx=18, pady=(0, 7))

    label = tk.Label(
        wrapper,
        text=label_text,
        font=("Segoe UI", 9, "bold"),
        fg=COLORS["text"],
        bg=COLORS["white"],
    )
    label.pack(anchor="w", pady=(0, 3))

    entry = tk.Entry(
        wrapper,
        textvariable=variable,
        font=("Segoe UI", 9),
        fg=COLORS["text"],
        bg=COLORS["input"],
        insertbackground=COLORS["blue"],
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["blue"],
    )
    entry.pack(fill="x", ipady=7)

    return entry


# ============================================================
# MAIN CONTENT
# ============================================================

main_frame = tk.Frame(root, bg=COLORS["bg"])
main_frame.pack(fill="both", expand=True, padx=18, pady=16)


# ============================================================
# LEFT PANEL
# ============================================================

left_panel = tk.Frame(
    main_frame,
    bg=COLORS["white"],
    width=310,
    highlightbackground=COLORS["border"],
    highlightthickness=1,
)
left_panel.pack(side="left", fill="y")
left_panel.pack_propagate(False)


# Colorful left-panel header
form_header = tk.Frame(left_panel, bg=COLORS["blue"], height=72)
form_header.pack(fill="x")
form_header.pack_propagate(False)

tk.Label(
    form_header,
    text="👨‍🎓  STUDENT FORM",
    font=("Segoe UI Emoji", 14, "bold"),
    fg=COLORS["white"],
    bg=COLORS["blue"],
).pack(anchor="w", padx=20, pady=(14, 2))

tk.Label(
    form_header,
    text="Add or edit academic records",
    font=("Segoe UI", 8),
    fg="#dbeafe",
    bg=COLORS["blue"],
).pack(anchor="w", padx=20)


# Form fields
create_field(left_panel, "Student ID", student_id_var)
create_field(left_panel, "Name", name_var)
create_field(left_panel, "Age", age_var)


# Gender dropdown
gender_wrapper = tk.Frame(left_panel, bg=COLORS["white"])
gender_wrapper.pack(fill="x", padx=18, pady=(0, 7))

tk.Label(
    gender_wrapper,
    text="Gender",
    font=("Segoe UI", 9, "bold"),
    fg=COLORS["text"],
    bg=COLORS["white"],
).pack(anchor="w", pady=(0, 3))

gender_menu = tk.OptionMenu(
    gender_wrapper,
    gender_var,
    "Male",
    "Female",
    "Other",
)
gender_menu.config(
    font=("Segoe UI", 9),
    fg=COLORS["text"],
    bg=COLORS["input"],
    activebackground="#dbeafe",
    activeforeground=COLORS["text"],
    anchor="w",
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COLORS["border"],
    padx=8,
    pady=5,
)
gender_menu["menu"].config(
    font=("Segoe UI", 9),
    bg=COLORS["white"],
    activebackground="#dbeafe",
)
gender_menu.pack(fill="x")


create_field(left_panel, "Department", department_var)
create_field(left_panel, "Course", course_var)
create_field(left_panel, "Marks (0 - 100)", marks_var)


# ============================================================
# ACTION BUTTONS
# ============================================================

button_frame = tk.Frame(left_panel, bg=COLORS["white"])
button_frame.pack(fill="x", padx=18, pady=(2, 12))

tk.Label(
    button_frame,
    text="ACTIONS",
    font=("Segoe UI", 8, "bold"),
    fg=COLORS["muted"],
    bg=COLORS["white"],
).pack(anchor="w", pady=(0, 5))


def make_action_button(parent, text, bg, hover, command):
    button = tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 9, "bold"),
        bg=bg,
        fg=COLORS["white"],
        activebackground=hover,
        activeforeground=COLORS["white"],
        relief="flat",
        bd=0,
        cursor="hand2",
        pady=7,
        command=command,
    )
    button.pack(fill="x", pady=2)
    add_hover_effect(button, bg, hover)
    return button


# Functions are defined below before user can click the buttons.


# ============================================================
# RIGHT PANEL
# ============================================================

right_panel = tk.Frame(main_frame, bg=COLORS["bg"])
right_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(18, 0),
)


# ============================================================
# DASHBOARD HEADER
# ============================================================

dashboard_top = tk.Frame(right_panel, bg=COLORS["bg"])
dashboard_top.pack(fill="x", pady=(0, 10))

tk.Label(
    dashboard_top,
    text="📊  DASHBOARD",
    font=("Segoe UI Emoji", 18, "bold"),
    fg=COLORS["text"],
    bg=COLORS["bg"],
).pack(side="left")

tk.Label(
    dashboard_top,
    text="  Manage and monitor student performance",
    font=("Segoe UI", 9),
    fg=COLORS["muted"],
    bg=COLORS["bg"],
).pack(side="left", pady=(5, 0))


# ============================================================
# STAT CARDS
# ============================================================

stats_frame = tk.Frame(right_panel, bg=COLORS["bg"])
stats_frame.pack(fill="x")


def create_stat_card(parent, icon, title_text, value_text, accent):
    card = tk.Frame(
        parent,
        bg=COLORS["white"],
        highlightbackground=COLORS["border"],
        highlightthickness=1,
    )
    card.pack(side="left", fill="both", expand=True, padx=(0, 8))

    accent_bar = tk.Frame(card, bg=accent, height=5)
    accent_bar.pack(fill="x")
    accent_bar.pack_propagate(False)

    content = tk.Frame(card, bg=COLORS["white"])
    content.pack(fill="both", expand=True, padx=16, pady=12)

    icon_label = tk.Label(
        content,
        text=icon,
        font=("Segoe UI Emoji", 18),
        fg=accent,
        bg=COLORS["white"],
    )
    icon_label.pack(side="left", padx=(0, 12))

    text_frame = tk.Frame(content, bg=COLORS["white"])
    text_frame.pack(side="left", fill="both", expand=True)

    tk.Label(
        text_frame,
        text=title_text,
        font=("Segoe UI", 8, "bold"),
        fg=COLORS["muted"],
        bg=COLORS["white"],
    ).pack(anchor="w")

    value_label = tk.Label(
        text_frame,
        text=value_text,
        font=("Segoe UI", 21, "bold"),
        fg=COLORS["text"],
        bg=COLORS["white"],
    )
    value_label.pack(anchor="w", pady=(2, 0))

    return value_label


total_students_label = create_stat_card(
    stats_frame, "👥", "TOTAL STUDENTS", "0", COLORS["blue"]
)

departments_label = create_stat_card(
    stats_frame, "🏢", "DEPARTMENTS", "0", COLORS["purple"]
)

average_marks_label = create_stat_card(
    stats_frame, "📈", "AVG. MARKS", "0%", COLORS["green"]
)

# Remove right padding from last card
stats_frame.winfo_children()[-1].pack_configure(padx=(0, 0))


def update_dashboard_stats():
    """Update dashboard statistics using the current student records."""
    total = len(students)

    departments = {
        str(student.get("department", "")).strip()
        for student in students
        if str(student.get("department", "")).strip()
    }

    marks = []
    for student in students:
        try:
            marks.append(float(student.get("marks", 0)))
        except (TypeError, ValueError):
            pass

    average = sum(marks) / len(marks) if marks else 0

    total_students_label.config(text=str(total))
    departments_label.config(text=str(len(departments)))
    average_marks_label.config(text=f"{average:.1f}%")


# ============================================================
# SEARCH SECTION
# ============================================================

search_section = tk.Frame(
    right_panel,
    bg=COLORS["white"],
    highlightbackground=COLORS["border"],
    highlightthickness=1,
)
search_section.pack(fill="x", pady=14)

create_section_title(search_section, "🔎", "SEARCH & FILTER", COLORS["blue"])

search_controls = tk.Frame(search_section, bg=COLORS["white"])
search_controls.pack(fill="x", padx=18, pady=(0, 8))

search_var = tk.StringVar()
department_search_var = tk.StringVar(value="All Departments")


def clear_search_placeholder():
    if search_entry.get() == "Search by ID, name, course...":
        search_entry.delete(0, tk.END)
        search_entry.config(fg=COLORS["text"])


def restore_search_placeholder():
    if not search_entry.get():
        search_entry.insert(0, "Search by ID, name, course...")
        search_entry.config(fg="#98a2b3")


search_entry = tk.Entry(
    search_controls,
    textvariable=search_var,
    font=("Segoe UI", 10),
    fg="#98a2b3",
    bg=COLORS["input"],
    insertbackground=COLORS["blue"],
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COLORS["border"],
    highlightcolor=COLORS["blue"],
)
search_entry.insert(0, "Search by ID, name, course...")
search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

search_entry.bind("<FocusIn>", lambda event: clear_search_placeholder())
search_entry.bind("<FocusOut>", lambda event: restore_search_placeholder())


# Department filter
department_menu = tk.OptionMenu(
    search_controls,
    department_search_var,
    "All Departments",
)
department_menu.config(
    font=("Segoe UI", 9),
    fg=COLORS["text"],
    bg=COLORS["input"],
    activebackground="#ede9fe",
    activeforeground=COLORS["text"],
    anchor="w",
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=COLORS["border"],
    width=18,
    padx=8,
    pady=5,
)
department_menu["menu"].config(
    font=("Segoe UI", 9),
    bg=COLORS["white"],
    activebackground="#ede9fe",
)
department_menu.pack(side="left", padx=4)


# Search functions are defined below before user can click buttons.


def search_students(show_message=True):
    """Search students using text and department filter."""
    raw_text = search_var.get().strip()

    if raw_text == "Search by ID, name, course...":
        raw_text = ""

    search_text = raw_text.lower()
    selected_department = department_search_var.get().strip()

    clear_table()

    matches = []

    for student in students:
        text_match = (
            not search_text
            or search_text in str(student.get("id", "")).lower()
            or search_text in str(student.get("name", "")).lower()
            or search_text in str(student.get("course", "")).lower()
            or search_text in str(student.get("department", "")).lower()
        )

        department_match = (
            selected_department == "All Departments"
            or str(student.get("department", "")) == selected_department
        )

        if text_match and department_match:
            matches.append(student)

    for student in matches:
        insert_student_row(student)

    global selected_student_id
    selected_student_id = None

    result_count_label.config(
        text=f"Showing {len(matches)} of {len(students)} students"
    )

    if matches:
        set_status(
            f"Found {len(matches)} matching student record(s).",
            "success"
        )
    elif show_message:
        set_status("No students matched your search.", "warning")
        messagebox.showinfo(
            "Search Results",
            "No students found matching your search."
        )
    else:
        set_status("No students matched the current filter.", "warning")


def reset_search():
    """Reset search and display all students."""
    search_var.set("")
    search_entry.delete(0, tk.END)
    search_entry.insert(0, "Search by ID, name, course...")
    search_entry.config(fg="#98a2b3")

    department_search_var.set("All Departments")

    clear_table()

    for student in students:
        insert_student_row(student)

    global selected_student_id
    selected_student_id = None

    result_count_label.config(
        text=f"Showing {len(students)} of {len(students)} students"
    )
    set_status("Search reset. Showing all student records.", "info")


search_button = make_action_button(
    search_controls,
    "SEARCH",
    COLORS["blue"],
    COLORS["blue_dark"],
    lambda: search_students(show_message=True),
)
search_button.pack_configure(
    side="left",
    fill=None,
    padx=4,
    pady=0,
    ipadx=10,
    ipady=2,
)

reset_button = make_action_button(
    search_controls,
    "RESET",
    COLORS["muted"],
    "#475467",
    reset_search,
)
reset_button.pack_configure(
    side="left",
    fill=None,
    padx=4,
    pady=0,
    ipadx=10,
    ipady=2,
)

search_hint_frame = tk.Frame(search_section, bg=COLORS["white"])
search_hint_frame.pack(fill="x", padx=18, pady=(0, 12))

tk.Label(
    search_hint_frame,
    text="💡 Tip: Ctrl+F focuses search  •  Enter searches  •  Esc clears the form",
    font=("Segoe UI Emoji", 8),
    fg=COLORS["muted"],
    bg=COLORS["white"],
).pack(side="left")


# ============================================================
# RECORDS SECTION
# ============================================================

records_section = tk.Frame(
    right_panel,
    bg=COLORS["white"],
    highlightbackground=COLORS["border"],
    highlightthickness=1,
)
records_section.pack(fill="both", expand=True)

records_heading = tk.Frame(records_section, bg=COLORS["white"])
records_heading.pack(fill="x", padx=18, pady=(13, 7))

tk.Label(
    records_heading,
    text="📋  STUDENT RECORDS",
    font=("Segoe UI Emoji", 12, "bold"),
    fg=COLORS["text"],
    bg=COLORS["white"],
).pack(side="left")

result_count_label = tk.Label(
    records_heading,
    text="Showing 0 of 0 students",
    font=("Segoe UI", 8, "bold"),
    fg=COLORS["muted"],
    bg=COLORS["white"],
)
result_count_label.pack(side="right")


table_container = tk.Frame(records_section, bg=COLORS["white"])
table_container.pack(fill="both", expand=True, padx=18, pady=(0, 15))

columns = (
    "ID",
    "NAME",
    "AGE",
    "GENDER",
    "DEPARTMENT",
    "COURSE",
    "MARKS",
)

tree = ttk.Treeview(
    table_container,
    columns=columns,
    show="headings",
    selectmode="browse",
)

column_widths = {
    "ID": 75,
    "NAME": 140,
    "AGE": 60,
    "GENDER": 85,
    "DEPARTMENT": 175,
    "COURSE": 160,
    "MARKS": 80,
}

for column in columns:
    tree.heading(column, text=column)
    tree.column(
        column,
        width=column_widths[column],
        anchor="center",
        stretch=True,
    )

tree.column("NAME", anchor="w")
tree.column("DEPARTMENT", anchor="w")
tree.column("COURSE", anchor="w")

table_scrollbar = ttk.Scrollbar(
    table_container,
    orient="vertical",
    command=tree.yview,
    style="Vertical.TScrollbar",
)
tree.configure(yscrollcommand=table_scrollbar.set)

tree.tag_configure("excellent", background="#ecfdf3")
tree.tag_configure("good", background="#eff6ff")
tree.tag_configure("average", background="#fffbeb")
tree.tag_configure("needs_attention", background="#fef2f2")

tree.pack(side="left", fill="both", expand=True)
table_scrollbar.pack(side="right", fill="y")

tree.bind("<<TreeviewSelect>>", lambda event: select_student(event))


def clear_table():
    """Remove all visible rows from the table."""
    for item in tree.get_children():
        tree.delete(item)


def insert_student_row(student):
    """Insert a student with a subtle performance-based row color."""
    try:
        marks = float(student.get("marks", 0))
    except (TypeError, ValueError):
        marks = 0

    if marks >= 90:
        tag = "excellent"
    elif marks >= 75:
        tag = "good"
    elif marks >= 50:
        tag = "average"
    else:
        tag = "needs_attention"

    return tree.insert(
        "",
        "end",
        values=(
            student.get("id", ""),
            student.get("name", ""),
            student.get("age", ""),
            student.get("gender", ""),
            student.get("department", ""),
            student.get("course", ""),
            student.get("marks", ""),
        ),
        tags=(tag,),
    )


# ============================================================
# STUDENT FUNCTIONS
# ============================================================

def clear_form():
    """Clear the student form."""
    global selected_student_id

    selected_student_id = None

    student_id_var.set("")
    name_var.set("")
    age_var.set("")
    gender_var.set("Select Gender")
    department_var.set("")
    course_var.set("")
    marks_var.set("")

    for item in tree.selection():
        tree.selection_remove(item)

    set_status("Form cleared. Ready for a new student.", "info")


def add_student():
    """Add a new student."""
    student_id = student_id_var.get().strip()
    name = name_var.get().strip()
    age = age_var.get().strip()
    gender = gender_var.get().strip()
    department = department_var.get().strip()
    course = course_var.get().strip()
    marks = marks_var.get().strip()

    validated = validate_student_data(
        student_id, name, age, gender, department, course, marks
    )

    if validated is None:
        return

    age_value, marks_value = validated

    if student_id_exists(student_id):
        messagebox.showerror(
            "Duplicate Student ID",
            f"Student ID '{student_id}' already exists."
        )
        return

    student = {
        "id": student_id,
        "name": name,
        "age": age_value,
        "gender": gender,
        "department": department,
        "course": course,
        "marks": marks_value,
    }

    students.append(student)

    if not save_students():
        students.pop()
        return

    refresh_department_filter()
    update_record_count()
    update_dashboard_stats()
    reset_search()
    clear_form()

    messagebox.showinfo(
        "Student Added",
        f"Student '{name}' was added successfully."
    )
    set_status(f"Student '{name}' added successfully.", "success")


def select_student(event=None):
    """Load the selected table row into the form."""
    global selected_student_id

    selected_items = tree.selection()

    if not selected_items:
        return

    values = tree.item(selected_items[0], "values")

    if not values:
        return

    selected_student_id = str(values[0])

    student_id_var.set(values[0])
    name_var.set(values[1])
    age_var.set(values[2])
    gender_var.set(values[3])
    department_var.set(values[4])
    course_var.set(values[5])
    marks_var.set(values[6])

    set_status(
        f"Selected {values[1]} ({values[0]}). Edit the form and press UPDATE.",
        "info"
    )


def update_student():
    """Update the selected student."""
    global selected_student_id

    if selected_student_id is None:
        messagebox.showwarning(
            "No Student Selected",
            "Please select a student record from the table first."
        )
        return

    student_id = student_id_var.get().strip()
    name = name_var.get().strip()
    age = age_var.get().strip()
    gender = gender_var.get().strip()
    department = department_var.get().strip()
    course = course_var.get().strip()
    marks = marks_var.get().strip()

    validated = validate_student_data(
        student_id, name, age, gender, department, course, marks
    )

    if validated is None:
        return

    age_value, marks_value = validated

    if student_id_exists(student_id, exclude_id=selected_student_id):
        messagebox.showerror(
            "Duplicate Student ID",
            f"Student ID '{student_id}' already exists."
        )
        return

    target_student = None

    for student in students:
        if str(student.get("id", "")).lower() == selected_student_id.lower():
            target_student = student
            break

    if target_student is None:
        messagebox.showerror(
            "Update Error",
            "The selected student record could not be found."
        )
        clear_form()
        return

    old_values = target_student.copy()

    target_student.update(
        {
            "id": student_id,
            "name": name,
            "age": age_value,
            "gender": gender,
            "department": department,
            "course": course,
            "marks": marks_value,
        }
    )

    if not save_students():
        target_student.clear()
        target_student.update(old_values)
        return

    selected_student_id = student_id

    refresh_department_filter()
    update_record_count()
    update_dashboard_stats()

    # Preserve the current search/filter view if possible.
    search_students(show_message=False)

    # Select the updated student if it is visible.
    for item in tree.get_children():
        values = tree.item(item, "values")
        if values and str(values[0]).lower() == student_id.lower():
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
            break

    messagebox.showinfo(
        "Student Updated",
        f"Student '{name}' was updated successfully."
    )
    set_status(f"Student '{name}' updated successfully.", "success")


def delete_student():
    """Delete the selected student after confirmation."""
    global selected_student_id

    if selected_student_id is None:
        messagebox.showwarning(
            "No Student Selected",
            "Please select a student record from the table first."
        )
        return

    student_name = selected_student_id
    target_student = None

    for student in students:
        if str(student.get("id", "")).lower() == selected_student_id.lower():
            target_student = student
            student_name = student.get("name", selected_student_id)
            break

    if target_student is None:
        messagebox.showerror(
            "Delete Error",
            "The selected student record could not be found."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{student_name}'?\n\n"
        "This action cannot be undone."
    )

    if not confirm:
        return

    original_students = students.copy()

    students[:] = [
        student
        for student in students
        if str(student.get("id", "")).lower() != selected_student_id.lower()
    ]

    if not save_students():
        students[:] = original_students
        return

    refresh_department_filter()
    update_record_count()
    update_dashboard_stats()
    reset_search()
    clear_form()

    messagebox.showinfo(
        "Student Deleted",
        f"Student '{student_name}' was deleted successfully."
    )
    set_status(f"Student '{student_name}' deleted successfully.", "success")


# ============================================================
# CREATE FORM BUTTONS
# ============================================================

add_button = make_action_button(
    button_frame,
    "➕  ADD STUDENT",
    COLORS["blue"],
    COLORS["blue_dark"],
    add_student,
)

update_button = make_action_button(
    button_frame,
    "✏️  UPDATE SELECTED",
    COLORS["purple"],
    COLORS["purple_dark"],
    update_student,
)

delete_button = make_action_button(
    button_frame,
    "🗑️  DELETE SELECTED",
    COLORS["red"],
    COLORS["red_dark"],
    delete_student,
)

clear_button = make_action_button(
    button_frame,
    "↻  CLEAR FORM",
    COLORS["muted"],
    "#475467",
    clear_form,
)


# ============================================================
# FOOTER / STATUS BAR
# ============================================================

footer = tk.Frame(root, bg=COLORS["navy"], height=42)
footer.pack(fill="x")
footer.pack_propagate(False)

database_status = tk.Label(
    footer,
    text="●  JSON Database Connected",
    font=("Segoe UI", 8, "bold"),
    fg="#86efac",
    bg=COLORS["navy"],
)
database_status.pack(side="left", padx=18)

status_message = tk.Label(
    footer,
    text="Ready — select a student or add a new record.",
    font=("Segoe UI", 8, "bold"),
    fg="#1d4ed8",
    bg="#dbeafe",
    padx=10,
    pady=4,
)
status_message.pack(side="left", padx=10, pady=5)

records_status = tk.Label(
    footer,
    text="Records: 0",
    font=("Segoe UI", 8, "bold"),
    fg=COLORS["white"],
    bg=COLORS["navy"],
)
records_status.pack(side="right", padx=18)


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

def focus_search(event=None):
    clear_search_placeholder()
    search_entry.focus_set()
    search_entry.select_range(0, tk.END)


def handle_enter(event=None):
    if search_entry.focus_get() == search_entry:
        search_students(show_message=True)
    elif tree.focus():
        update_student()


root.bind("<Control-f>", focus_search)
root.bind("<Escape>", lambda event: clear_form())
root.bind("<Return>", handle_enter)


# ============================================================
# WINDOW CLOSE
# ============================================================

def on_closing():
    """Close the application safely."""
    if messagebox.askokcancel(
        "Exit Application",
        "Are you sure you want to close the Student Management System?"
    ):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)


# ============================================================
# INITIAL DISPLAY
# ============================================================

refresh_department_filter()

for student in students:
    insert_student_row(student)

update_record_count()
update_dashboard_stats()

result_count_label.config(
    text=f"Showing {len(students)} of {len(students)} students"
)

set_status(
    f"Ready — {len(students)} student record(s) loaded.",
    "success" if students else "info"
)

root.mainloop()