
import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
from pathlib import Path
from datetime import datetime, timedelta


# ============================================================
# LIBRARY MANAGEMENT SYSTEM
# DARK MODERN INTERFACE
# ============================================================

# ------------------------------------------------------------
# COLORS
# ------------------------------------------------------------

COLORS = {
    "background": "#0b1120",
    "surface": "#111827",
    "surface2": "#172033",
    "surface3": "#1e293b",
    "border": "#263449",

    "text": "#f8fafc",
    "muted": "#94a3b8",

    "cyan": "#22d3ee",
    "cyan_dark": "#0891b2",

    "blue": "#3b82f6",
    "blue_dark": "#2563eb",

    "green": "#22c55e",
    "green_dark": "#16a34a",

    "orange": "#f59e0b",
    "orange_dark": "#d97706",

    "red": "#ef4444",
    "red_dark": "#dc2626",

    "purple": "#a855f7",
    "white": "#ffffff",
}


# ------------------------------------------------------------
# DATA
# ------------------------------------------------------------

DATA_FILE = Path(__file__).resolve().parent / "data" / "books.json"

books = []
selected_book_id = None


# ============================================================
# DATABASE
# ============================================================

def load_books():
    global books

    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not DATA_FILE.exists():
            DATA_FILE.write_text("[]", encoding="utf-8")
            books = []
            return

        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        books = data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        books = []


def save_books():
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(books, file, indent=4)

        return True

    except OSError:
        messagebox.showerror(
            "Database Error",
            "Could not save the library records."
        )
        return False


# ============================================================
# MAIN WINDOW
# ============================================================

load_books()

root = tk.Tk()

root.title("Library Management System")
root.geometry("1500x900")
root.minsize(1250, 780)
root.configure(bg=COLORS["background"])


# ============================================================
# TKINTER STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass


style.configure(
    "Treeview",
    background=COLORS["surface"],
    fieldbackground=COLORS["surface"],
    foreground=COLORS["text"],
    rowheight=38,
    borderwidth=0,
    font=("Segoe UI", 9)
)

style.configure(
    "Treeview.Heading",
    background=COLORS["surface3"],
    foreground=COLORS["cyan"],
    font=("Segoe UI", 9, "bold"),
    padding=10,
    relief="flat"
)

style.map(
    "Treeview",
    background=[
        ("selected", "#164e63")
    ],
    foreground=[
        ("selected", COLORS["white"])
    ]
)

style.configure(
    "Vertical.TScrollbar",
    background=COLORS["surface3"],
    troughcolor=COLORS["background"],
    bordercolor=COLORS["background"],
    arrowcolor=COLORS["muted"]
)


# ============================================================
# HEADER / TOP NAVIGATION
# ============================================================

header = tk.Frame(
    root,
    bg=COLORS["surface"],
    height=82
)

header.pack(fill="x")
header.pack_propagate(False)


# Logo

logo_frame = tk.Frame(
    header,
    bg=COLORS["surface"]
)

logo_frame.pack(
    side="left",
    padx=28
)


logo = tk.Label(
    logo_frame,
    text="▣",
    font=("Segoe UI", 30, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["cyan"]
)

logo.pack(side="left")


title_frame = tk.Frame(
    logo_frame,
    bg=COLORS["surface"]
)

title_frame.pack(
    side="left",
    padx=(12, 0)
)


title = tk.Label(
    title_frame,
    text="LIBRARY HUB",
    font=("Segoe UI", 18, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["text"]
)

title.pack(anchor="w")


subtitle = tk.Label(
    title_frame,
    text="Digital Library Control Center",
    font=("Segoe UI", 9),
    bg=COLORS["surface"],
    fg=COLORS["muted"]
)

subtitle.pack(anchor="w")


# Header right

header_right = tk.Frame(
    header,
    bg=COLORS["surface"]
)

header_right.pack(
    side="right",
    padx=28
)


date_label = tk.Label(
    header_right,
    text=datetime.now().strftime("%d %b %Y"),
    font=("Segoe UI", 10, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["text"]
)

date_label.pack(side="left", padx=15)


system_label = tk.Label(
    header_right,
    text="● SYSTEM ONLINE",
    font=("Segoe UI", 9, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["green"]
)

system_label.pack(side="left")


# ============================================================
# MAIN CONTAINER
# ============================================================

main = tk.Frame(
    root,
    bg=COLORS["background"]
)

main.pack(
    fill="both",
    expand=True,
    padx=24,
    pady=20
)


# ============================================================
# PAGE TITLE
# ============================================================

page_header = tk.Frame(
    main,
    bg=COLORS["background"]
)

page_header.pack(
    fill="x",
    pady=(0, 15)
)


page_title = tk.Label(
    page_header,
    text="Library Overview",
    font=("Segoe UI", 22, "bold"),
    bg=COLORS["background"],
    fg=COLORS["text"]
)

page_title.pack(side="left")


page_description = tk.Label(
    page_header,
    text="Manage books, borrowing activity and library records",
    font=("Segoe UI", 9),
    bg=COLORS["background"],
    fg=COLORS["muted"]
)

page_description.pack(
    side="left",
    padx=18,
    pady=(8, 0)
)


# ============================================================
# STATISTICS
# ============================================================

stats_frame = tk.Frame(
    main,
    bg=COLORS["background"]
)

stats_frame.pack(
    fill="x",
    pady=(0, 18)
)


def create_stat_card(parent, icon, title_text, color):
    card = tk.Frame(
        parent,
        bg=COLORS["surface"],
        highlightbackground=COLORS["border"],
        highlightthickness=1,
        height=105
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    card.pack_propagate(False)

    icon_label = tk.Label(
        card,
        text=icon,
        font=("Segoe UI Emoji", 20),
        bg=COLORS["surface"],
        fg=color
    )

    icon_label.pack(
        anchor="w",
        padx=18,
        pady=(14, 0)
    )

    label = tk.Label(
        card,
        text=title_text,
        font=("Segoe UI", 8, "bold"),
        bg=COLORS["surface"],
        fg=COLORS["muted"]
    )

    label.pack(
        anchor="w",
        padx=18
    )

    value = tk.Label(
        card,
        text="0",
        font=("Segoe UI", 20, "bold"),
        bg=COLORS["surface"],
        fg=COLORS["text"]
    )

    value.place(
        relx=1.0,
        x=-20,
        y=35,
        anchor="ne"
    )

    return value


total_label = create_stat_card(
    stats_frame,
    "▣",
    "TOTAL COLLECTION",
    COLORS["cyan"]
)

available_label = create_stat_card(
    stats_frame,
    "✓",
    "AVAILABLE",
    COLORS["green"]
)

borrowed_label = create_stat_card(
    stats_frame,
    "↗",
    "CURRENTLY BORROWED",
    COLORS["orange"]
)

borrower_label = create_stat_card(
    stats_frame,
    "●",
    "ACTIVE BORROWERS",
    COLORS["purple"]
)


# ============================================================
# SEARCH / ACTION BAR
# ============================================================

toolbar = tk.Frame(
    main,
    bg=COLORS["surface"],
    highlightbackground=COLORS["border"],
    highlightthickness=1
)

toolbar.pack(
    fill="x",
    pady=(0, 15)
)


search_area = tk.Frame(
    toolbar,
    bg=COLORS["surface"]
)

search_area.pack(
    side="left",
    fill="x",
    expand=True,
    padx=16,
    pady=14
)


search_icon = tk.Label(
    search_area,
    text="⌕",
    font=("Segoe UI", 20, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["cyan"]
)

search_icon.pack(side="left")


search_var = tk.StringVar()

search_entry = tk.Entry(
    search_area,
    textvariable=search_var,
    font=("Segoe UI", 10),
    bg=COLORS["surface2"],
    fg=COLORS["text"],
    insertbackground=COLORS["cyan"],
    relief="flat",
    bd=0
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10,
    ipady=8
)


filter_var = tk.StringVar(value="All Status")


filter_menu = tk.OptionMenu(
    search_area,
    filter_var,
    "All Status",
    "Available",
    "Borrowed"
)

filter_menu.config(
    font=("Segoe UI", 9),
    bg=COLORS["surface3"],
    fg=COLORS["text"],
    activebackground=COLORS["border"],
    activeforeground=COLORS["cyan"],
    relief="flat",
    bd=0,
    width=13
)

filter_menu["menu"].config(
    bg=COLORS["surface3"],
    fg=COLORS["text"],
    activebackground=COLORS["cyan"],
    activeforeground=COLORS["background"]
)

filter_menu.pack(
    side="left",
    padx=5
)


def make_button(parent, text, bg, command, width=12):
    button = tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 9, "bold"),
        bg=bg,
        fg=COLORS["white"],
        activebackground=bg,
        activeforeground=COLORS["white"],
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=8,
        width=width,
        command=command
    )

    def enter(event):
        button.config(
            bg=COLORS["cyan_dark"] if bg == COLORS["cyan"] else
               COLORS["blue_dark"] if bg == COLORS["blue"] else
               COLORS["green_dark"] if bg == COLORS["green"] else
               COLORS["orange_dark"] if bg == COLORS["orange"] else
               COLORS["red_dark"] if bg == COLORS["red"] else
               "#334155"
        )

    def leave(event):
        button.config(bg=bg)

    button.bind("<Enter>", enter)
    button.bind("<Leave>", leave)

    return button


# ============================================================
# FORM FUNCTIONS
# ============================================================

book_id_var = tk.StringVar()
title_var = tk.StringVar()
author_var = tk.StringVar()
category_var = tk.StringVar(value="Select Category")
year_var = tk.StringVar()
isbn_var = tk.StringVar()

status_var = tk.StringVar(value="Available")
borrower_var = tk.StringVar()
phone_var = tk.StringVar()

issue_date_var = tk.StringVar()
due_date_var = tk.StringVar()


def clear_form():
    global selected_book_id

    selected_book_id = None

    book_id_var.set("")
    title_var.set("")
    author_var.set("")
    category_var.set("Select Category")
    year_var.set("")
    isbn_var.set("")
    status_var.set("Available")
    borrower_var.set("")
    phone_var.set("")
    issue_date_var.set("")
    due_date_var.set("")

    for item in tree.selection():
        tree.selection_remove(item)

    form_mode_label.config(text="NEW BOOK")


def validate_book_data():
    book_id = book_id_var.get().strip()
    book_title = title_var.get().strip()
    author = author_var.get().strip()
    category = category_var.get().strip()
    year = year_var.get().strip()
    isbn = isbn_var.get().strip()
    status = status_var.get().strip()
    borrower = borrower_var.get().strip()
    phone = phone_var.get().strip()

    if not all([
        book_id,
        book_title,
        author,
        category,
        year,
        isbn
    ]):
        messagebox.showwarning(
            "Missing Information",
            "Please complete all book details."
        )
        return None

    if category == "Select Category":
        messagebox.showwarning(
            "Category Required",
            "Please select a book category."
        )
        return None

    if not re.fullmatch(
        r"[A-Za-z0-9_-]+",
        book_id
    ):
        messagebox.showerror(
            "Invalid Book ID",
            "Book ID can contain letters, numbers, hyphens and underscores only."
        )
        return None

    if not re.fullmatch(
        r"[A-Za-z0-9 .,'&:!?()\-]+",
        book_title
    ):
        messagebox.showerror(
            "Invalid Title",
            "Please enter a valid book title."
        )
        return None

    if not re.fullmatch(
        r"[A-Za-z .,'&\-]+",
        author
    ):
        messagebox.showerror(
            "Invalid Author",
            "Please enter a valid author name."
        )
        return None

    try:
        year_value = int(year)

        if not 1000 <= year_value <= datetime.now().year:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Year",
            f"Publication year must be between 1000 and {datetime.now().year}."
        )
        return None

    if not re.fullmatch(
        r"[0-9Xx\- ]+",
        isbn
    ):
        messagebox.showerror(
            "Invalid ISBN",
            "ISBN can contain numbers, spaces, hyphens and X."
        )
        return None

    if status == "Borrowed":

        if not borrower:
            messagebox.showwarning(
                "Borrower Required",
                "Enter the borrower's name."
            )
            return None

        if not phone:
            messagebox.showwarning(
                "Phone Required",
                "Enter the borrower's phone number."
            )
            return None

        if not re.fullmatch(
            r"[A-Za-z .'-]+",
            borrower
        ):
            messagebox.showerror(
                "Invalid Borrower",
                "Borrower name should contain letters only."
            )
            return None

        if not phone.isdigit() or not 7 <= len(phone) <= 15:
            messagebox.showerror(
                "Invalid Phone",
                "Please enter a valid phone number."
            )
            return None

    return {
        "id": book_id,
        "title": book_title,
        "author": author,
        "category": category,
        "year": year_value,
        "isbn": isbn,
        "status": status,
        "borrower": borrower if status == "Borrowed" else "",
        "phone": phone if status == "Borrowed" else ""
    }


# ============================================================
# ADD BOOK
# ============================================================

def add_book():
    data = validate_book_data()

    if data is None:
        return

    for book in books:
        if book.get("id", "").lower() == data["id"].lower():
            messagebox.showerror(
                "Duplicate Book ID",
                f"Book ID '{data['id']}' already exists."
            )
            return

    if data["status"] == "Borrowed":
        today = datetime.now()

        data["issue_date"] = today.strftime("%Y-%m-%d")
        data["due_date"] = (
            today + timedelta(days=14)
        ).strftime("%Y-%m-%d")

    else:
        data["issue_date"] = ""
        data["due_date"] = ""

    books.append(data)

    if not save_books():
        books.pop()
        return

    refresh_table()
    update_dashboard()
    clear_form()

    show_status(
        "Book added successfully.",
        COLORS["green"]
    )


# ============================================================
# SELECT BOOK
# ============================================================

def select_book(event=None):
    global selected_book_id

    selected = tree.selection()

    if not selected:
        return

    values = tree.item(
        selected[0],
        "values"
    )

    if not values:
        return

    selected_book_id = str(values[0])

    for book in books:

        if str(book.get("id")) == selected_book_id:

            book_id_var.set(book.get("id", ""))
            title_var.set(book.get("title", ""))
            author_var.set(book.get("author", ""))
            category_var.set(
                book.get(
                    "category",
                    "Select Category"
                )
            )

            year_var.set(
                str(book.get("year", ""))
            )

            isbn_var.set(
                book.get("isbn", "")
            )

            status_var.set(
                book.get(
                    "status",
                    "Available"
                )
            )

            borrower_var.set(
                book.get(
                    "borrower",
                    ""
                )
            )

            phone_var.set(
                book.get(
                    "phone",
                    ""
                )
            )

            issue_date_var.set(
                book.get(
                    "issue_date",
                    ""
                )
            )

            due_date_var.set(
                book.get(
                    "due_date",
                    ""
                )
            )

            form_mode_label.config(
                text="EDITING BOOK"
            )

            break


# ============================================================
# UPDATE BOOK
# ============================================================

def update_book():
    global selected_book_id

    if selected_book_id is None:
        messagebox.showwarning(
            "No Selection",
            "Select a book from the records table first."
        )
        return

    data = validate_book_data()

    if data is None:
        return

    old_id = selected_book_id

    if data["id"].lower() != old_id.lower():

        for book in books:
            if book.get("id", "").lower() == data["id"].lower():
                messagebox.showerror(
                    "Duplicate Book ID",
                    "Another book already uses this ID."
                )
                return

    target = None

    for book in books:
        if str(book.get("id", "")).lower() == old_id.lower():
            target = book
            break

    if target is None:
        messagebox.showerror(
            "Update Error",
            "Selected book could not be found."
        )
        return

    original = target.copy()

    target.update(data)

    if target["status"] == "Borrowed":

        if not target.get("issue_date"):
            today = datetime.now()

            target["issue_date"] = today.strftime(
                "%Y-%m-%d"
            )

            target["due_date"] = (
                today + timedelta(days=14)
            ).strftime("%Y-%m-%d")

    else:
        target["issue_date"] = ""
        target["due_date"] = ""

    if not save_books():
        target.clear()
        target.update(original)
        return

    selected_book_id = data["id"]

    refresh_table()
    update_dashboard()

    show_status(
        "Book updated successfully.",
        COLORS["cyan"]
    )


# ============================================================
# DELETE BOOK
# ============================================================

def delete_book():
    global selected_book_id

    if selected_book_id is None:
        messagebox.showwarning(
            "No Selection",
            "Select a book to delete."
        )
        return

    target = None

    for book in books:

        if str(book.get("id", "")).lower() == selected_book_id.lower():
            target = book
            break

    if target is None:
        return

    confirm = messagebox.askyesno(
        "Delete Book",
        f"Delete '{target.get('title', 'this book')}'?\n\n"
        "This action cannot be undone."
    )

    if not confirm:
        return

    original = books.copy()

    books.remove(target)

    if not save_books():
        books[:] = original
        return

    refresh_table()
    update_dashboard()
    clear_form()

    show_status(
        "Book deleted successfully.",
        COLORS["red"]
    )


# ============================================================
# BORROW BOOK
# ============================================================

def borrow_book():
    global selected_book_id

    if selected_book_id is None:
        messagebox.showwarning(
            "No Selection",
            "Select a book from the table first."
        )
        return

    target = None

    for book in books:
        if str(book.get("id", "")).lower() == selected_book_id.lower():
            target = book
            break

    if target is None:
        return

    if target.get("status") == "Borrowed":
        messagebox.showwarning(
            "Already Borrowed",
            "This book is already borrowed."
        )
        return

    borrower = borrower_var.get().strip()
    phone = phone_var.get().strip()

    if not borrower:
        messagebox.showwarning(
            "Borrower Required",
            "Enter the borrower's name in the form below."
        )
        borrower_entry.focus_set()
        return

    if not phone:
        messagebox.showwarning(
            "Phone Required",
            "Enter the borrower's phone number."
        )
        phone_entry.focus_set()
        return

    if not re.fullmatch(
        r"[A-Za-z .'-]+",
        borrower
    ):
        messagebox.showerror(
            "Invalid Borrower",
            "Borrower name should contain letters only."
        )
        return

    if not phone.isdigit() or not 7 <= len(phone) <= 15:
        messagebox.showerror(
            "Invalid Phone",
            "Please enter a valid phone number."
        )
        return

    today = datetime.now()

    target["status"] = "Borrowed"
    target["borrower"] = borrower
    target["phone"] = phone

    target["issue_date"] = today.strftime(
        "%Y-%m-%d"
    )

    target["due_date"] = (
        today + timedelta(days=14)
    ).strftime("%Y-%m-%d")

    if not save_books():
        return

    refresh_table()
    update_dashboard()

    show_status(
        f"'{target['title']}' borrowed successfully.",
        COLORS["orange"]
    )


# ============================================================
# RETURN BOOK
# ============================================================

def return_book():
    global selected_book_id

    if selected_book_id is None:
        messagebox.showwarning(
            "No Selection",
            "Select a book from the table first."
        )
        return

    target = None

    for book in books:
        if str(book.get("id", "")).lower() == selected_book_id.lower():
            target = book
            break

    if target is None:
        return

    if target.get("status") != "Borrowed":
        messagebox.showwarning(
            "Already Available",
            "This book is already available."
        )
        return

    confirm = messagebox.askyesno(
        "Return Book",
        f"Mark '{target.get('title')}' as returned?"
    )

    if not confirm:
        return

    target["status"] = "Available"
    target["borrower"] = ""
    target["phone"] = ""
    target["issue_date"] = ""
    target["due_date"] = ""

    if not save_books():
        return

    refresh_table()
    update_dashboard()
    clear_form()

    show_status(
        "Book returned successfully.",
        COLORS["green"]
    )


# ============================================================
# SEARCH
# ============================================================

def search_books():
    text = search_var.get().strip().lower()
    selected_status = filter_var.get()

    for item in tree.get_children():
        tree.delete(item)

    matches = []

    for book in books:

        text_match = (
            not text
            or text in str(book.get("id", "")).lower()
            or text in str(book.get("title", "")).lower()
            or text in str(book.get("author", "")).lower()
            or text in str(book.get("category", "")).lower()
            or text in str(book.get("isbn", "")).lower()
            or text in str(book.get("borrower", "")).lower()
        )

        status_match = (
            selected_status == "All Status"
            or book.get("status") == selected_status
        )

        if text_match and status_match:
            matches.append(book)

    for book in matches:
        insert_book_row(book)

    if not matches:
        show_status(
            "No matching books found.",
            COLORS["orange"]
        )


def reset_search():
    search_var.set("")
    filter_var.set("All Status")

    refresh_table()

    show_status(
        "All library records restored.",
        COLORS["cyan"]
    )


# ============================================================
# TOOLBAR BUTTONS
# ============================================================

button_area = tk.Frame(
    toolbar,
    bg=COLORS["surface"]
)

button_area.pack(
    side="right",
    padx=12
)


search_button = make_button(
    button_area,
    "SEARCH",
    COLORS["cyan"],
    search_books,
    9
)

search_button.pack(
    side="left",
    padx=3
)


reset_button = make_button(
    button_area,
    "RESET",
    COLORS["surface3"],
    reset_search,
    8
)

reset_button.pack(
    side="left",
    padx=3
)


borrow_button = make_button(
    button_area,
    "BORROW",
    COLORS["orange"],
    borrow_book,
    9
)

borrow_button.pack(
    side="left",
    padx=3
)


return_button = make_button(
    button_area,
    "RETURN",
    COLORS["green"],
    return_book,
    9
)

return_button.pack(
    side="left",
    padx=3
)


# ============================================================
# RECORDS PANEL
# ============================================================

records_panel = tk.Frame(
    main,
    bg=COLORS["surface"],
    highlightbackground=COLORS["border"],
    highlightthickness=1
)

records_panel.pack(
    fill="both",
    expand=True
)


# Records heading

records_top = tk.Frame(
    records_panel,
    bg=COLORS["surface"],
    height=55
)

records_top.pack(fill="x")
records_top.pack_propagate(False)


records_title = tk.Label(
    records_top,
    text="BOOK CATALOG",
    font=("Segoe UI", 12, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["text"]
)

records_title.pack(
    side="left",
    padx=18
)


records_hint = tk.Label(
    records_top,
    text="Select a record to manage its details",
    font=("Segoe UI", 8),
    bg=COLORS["surface"],
    fg=COLORS["muted"]
)

records_hint.pack(
    side="right",
    padx=18
)


# ============================================================
# TABLE
# ============================================================

table_container = tk.Frame(
    records_panel,
    bg=COLORS["surface"]
)

table_container.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(0, 15)
)


columns = (
    "ID",
    "TITLE",
    "AUTHOR",
    "CATEGORY",
    "YEAR",
    "STATUS",
    "BORROWER",
    "ISSUED",
    "DUE"
)


tree = ttk.Treeview(
    table_container,
    columns=columns,
    show="headings",
    selectmode="browse"
)


column_widths = {
    "ID": 75,
    "TITLE": 210,
    "AUTHOR": 150,
    "CATEGORY": 125,
    "YEAR": 65,
    "STATUS": 95,
    "BORROWER": 145,
    "ISSUED": 100,
    "DUE": 100
}


for column in columns:

    tree.heading(
        column,
        text=column
    )

    tree.column(
        column,
        width=column_widths[column],
        anchor="center"
    )


tree.column(
    "TITLE",
    anchor="w"
)

tree.column(
    "AUTHOR",
    anchor="w"
)

tree.column(
    "BORROWER",
    anchor="w"
)


scrollbar = ttk.Scrollbar(
    table_container,
    orient="vertical",
    command=tree.yview
)

tree.configure(
    yscrollcommand=scrollbar.set
)


tree.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


tree.tag_configure(
    "available",
    foreground=COLORS["green"]
)

tree.tag_configure(
    "borrowed",
    foreground=COLORS["orange"]
)


# ============================================================
# BOOK DETAILS DRAWER
# ============================================================

details_panel = tk.Frame(
    main,
    bg=COLORS["surface2"],
    highlightbackground=COLORS["border"],
    highlightthickness=1
)

details_panel.pack(
    fill="x",
    pady=(15, 0)
)


details_header = tk.Frame(
    details_panel,
    bg=COLORS["surface2"]
)

details_header.pack(
    fill="x"
)


details_title = tk.Label(
    details_header,
    text="MANAGE BOOK",
    font=("Segoe UI", 11, "bold"),
    bg=COLORS["surface2"],
    fg=COLORS["cyan"]
)

details_title.pack(
    side="left",
    padx=18,
    pady=12
)


form_mode_label = tk.Label(
    details_header,
    text="NEW BOOK",
    font=("Segoe UI", 8, "bold"),
    bg=COLORS["surface2"],
    fg=COLORS["muted"]
)

form_mode_label.pack(
    side="right",
    padx=18
)


# ============================================================
# FORM
# ============================================================

form = tk.Frame(
    details_panel,
    bg=COLORS["surface2"]
)

form.pack(
    fill="x",
    padx=18,
    pady=(0, 14)
)


def form_label(parent, text):
    label = tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 8, "bold"),
        bg=COLORS["surface2"],
        fg=COLORS["muted"]
    )

    label.pack(
        anchor="w",
        pady=(0, 3)
    )

    return label


def form_entry(parent, variable):
    entry = tk.Entry(
        parent,
        textvariable=variable,
        font=("Segoe UI", 9),
        bg=COLORS["surface"],
        fg=COLORS["text"],
        insertbackground=COLORS["cyan"],
        relief="flat",
        bd=0
    )

    entry.pack(
        fill="x",
        ipady=6
    )

    return entry


# Columns

field1 = tk.Frame(form, bg=COLORS["surface2"])
field1.pack(side="left", fill="x", expand=True, padx=(0, 8))

form_label(field1, "BOOK ID")
book_id_entry = form_entry(field1, book_id_var)


field2 = tk.Frame(form, bg=COLORS["surface2"])
field2.pack(side="left", fill="x", expand=True, padx=8)

form_label(field2, "TITLE")
title_entry = form_entry(field2, title_var)


field3 = tk.Frame(form, bg=COLORS["surface2"])
field3.pack(side="left", fill="x", expand=True, padx=8)

form_label(field3, "AUTHOR")
author_entry = form_entry(field3, author_var)


field4 = tk.Frame(form, bg=COLORS["surface2"])
field4.pack(side="left", fill="x", expand=True, padx=8)

form_label(field4, "CATEGORY")


category_menu = tk.OptionMenu(
    field4,
    category_var,
    "Programming",
    "Science",
    "Mathematics",
    "Physics",
    "Literature",
    "History",
    "Engineering",
    "Biography",
    "Other"
)

category_menu.config(
    font=("Segoe UI", 9),
    bg=COLORS["surface"],
    fg=COLORS["text"],
    activebackground=COLORS["surface3"],
    activeforeground=COLORS["cyan"],
    relief="flat",
    bd=0,
    anchor="w"
)

category_menu["menu"].config(
    bg=COLORS["surface3"],
    fg=COLORS["text"],
    activebackground=COLORS["cyan"],
    activeforeground=COLORS["background"]
)

category_menu.pack(
    fill="x",
    ipady=3
)


field5 = tk.Frame(form, bg=COLORS["surface2"])
field5.pack(side="left", fill="x", expand=True, padx=8)

form_label(field5, "YEAR")
year_entry = form_entry(field5, year_var)


field6 = tk.Frame(form, bg=COLORS["surface2"])
field6.pack(side="left", fill="x", expand=True, padx=8)

form_label(field6, "ISBN")
isbn_entry = form_entry(field6, isbn_var)


field7 = tk.Frame(form, bg=COLORS["surface2"])
field7.pack(side="left", fill="x", expand=True, padx=(8, 0))

form_label(field7, "STATUS")


status_menu = tk.OptionMenu(
    field7,
    status_var,
    "Available",
    "Borrowed"
)

status_menu.config(
    font=("Segoe UI", 9),
    bg=COLORS["surface"],
    fg=COLORS["text"],
    activebackground=COLORS["surface3"],
    activeforeground=COLORS["cyan"],
    relief="flat",
    bd=0,
    anchor="w"
)

status_menu["menu"].config(
    bg=COLORS["surface3"],
    fg=COLORS["text"],
    activebackground=COLORS["cyan"],
    activeforeground=COLORS["background"]
)

status_menu.pack(
    fill="x",
    ipady=3
)


# ============================================================
# SECOND FORM ROW
# ============================================================

form2 = tk.Frame(
    details_panel,
    bg=COLORS["surface2"]
)

form2.pack(
    fill="x",
    padx=18,
    pady=(0, 14)
)


borrower_field = tk.Frame(
    form2,
    bg=COLORS["surface2"]
)

borrower_field.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 8)
)

form_label(
    borrower_field,
    "BORROWER NAME"
)

borrower_entry = form_entry(
    borrower_field,
    borrower_var
)


phone_field = tk.Frame(
    form2,
    bg=COLORS["surface2"]
)

phone_field.pack(
    side="left",
    fill="x",
    expand=True,
    padx=8
)

form_label(
    phone_field,
    "BORROWER PHONE"
)

phone_entry = form_entry(
    phone_field,
    phone_var
)


issue_field = tk.Frame(
    form2,
    bg=COLORS["surface2"]
)

issue_field.pack(
    side="left",
    fill="x",
    expand=True,
    padx=8
)

form_label(
    issue_field,
    "ISSUE DATE"
)

issue_entry = form_entry(
    issue_field,
    issue_date_var
)

issue_entry.config(
    state="readonly"
)


due_field = tk.Frame(
    form2,
    bg=COLORS["surface2"]
)

due_field.pack(
    side="left",
    fill="x",
    expand=True,
    padx=8
)

form_label(
    due_field,
    "DUE DATE"
)

due_entry = form_entry(
    due_field,
    due_date_var
)

due_entry.config(
    state="readonly"
)


# ============================================================
# CRUD BUTTONS
# ============================================================

form_buttons = tk.Frame(
    form2,
    bg=COLORS["surface2"]
)

form_buttons.pack(
    side="left",
    padx=(8, 0)
)


form_label(
    form_buttons,
    "ACTIONS"
)


actions = tk.Frame(
    form_buttons,
    bg=COLORS["surface2"]
)

actions.pack()


add_button = make_button(
    actions,
    "ADD",
    COLORS["blue"],
    add_book,
    7
)

add_button.pack(
    side="left",
    padx=2
)


update_button = make_button(
    actions,
    "UPDATE",
    COLORS["cyan_dark"],
    update_book,
    7
)

update_button.pack(
    side="left",
    padx=2
)


delete_button = make_button(
    actions,
    "DELETE",
    COLORS["red"],
    delete_book,
    7
)

delete_button.pack(
    side="left",
    padx=2
)


clear_button = make_button(
    actions,
    "CLEAR",
    COLORS["surface3"],
    clear_form,
    7
)

clear_button.pack(
    side="left",
    padx=2
)


# ============================================================
# TABLE FUNCTIONS
# ============================================================

def insert_book_row(book):

    status = book.get(
        "status",
        "Available"
    )

    tags = (
        "available"
        if status == "Available"
        else "borrowed"
    )

    tree.insert(
        "",
        "end",
        values=(
            book.get("id", ""),
            book.get("title", ""),
            book.get("author", ""),
            book.get("category", ""),
            book.get("year", ""),
            status,
            book.get("borrower", ""),
            book.get("issue_date", ""),
            book.get("due_date", "")
        ),
        tags=(tags,)
    )


def refresh_table():

    for item in tree.get_children():
        tree.delete(item)

    for book in books:
        insert_book_row(book)


# ============================================================
# DASHBOARD
# ============================================================

def update_dashboard():

    total = len(books)

    available = sum(
        1
        for book in books
        if book.get("status") == "Available"
    )

    borrowed = sum(
        1
        for book in books
        if book.get("status") == "Borrowed"
    )

    borrowers = {
        book.get("borrower", "").strip()
        for book in books
        if book.get("borrower", "").strip()
    }

    total_label.config(
        text=str(total)
    )

    available_label.config(
        text=str(available)
    )

    borrowed_label.config(
        text=str(borrowed)
    )

    borrower_label.config(
        text=str(len(borrowers))
    )


# ============================================================
# STATUS BAR
# ============================================================

footer = tk.Frame(
    root,
    bg="#080d18",
    height=34
)

footer.pack(
    fill="x"
)

footer.pack_propagate(False)


footer_left = tk.Label(
    footer,
    text="●  JSON DATABASE CONNECTED",
    font=("Segoe UI", 8, "bold"),
    bg="#080d18",
    fg=COLORS["green"]
)

footer_left.pack(
    side="left",
    padx=20
)


status_message = tk.Label(
    footer,
    text="Ready",
    font=("Segoe UI", 8),
    bg="#080d18",
    fg=COLORS["muted"]
)

status_message.pack(
    side="left",
    padx=25
)


records_status = tk.Label(
    footer,
    text="BOOKS: 0",
    font=("Segoe UI", 8, "bold"),
    bg="#080d18",
    fg=COLORS["text"]
)

records_status.pack(
    side="right",
    padx=20
)


def show_status(message, color):

    status_message.config(
        text=message,
        fg=color
    )

    root.after(
        5000,
        lambda: status_message.config(
            text="Ready",
            fg=COLORS["muted"]
        )
    )


def update_record_count():

    records_status.config(
        text=f"BOOKS: {len(books)}"
    )


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

def focus_search(event=None):

    search_entry.focus_set()

    search_entry.select_range(
        0,
        tk.END
    )


root.bind(
    "<Control-f>",
    focus_search
)

root.bind(
    "<Escape>",
    lambda event: clear_form()
)

search_entry.bind(
    "<Return>",
    lambda event: search_books()
)

tree.bind(
    "<<TreeviewSelect>>",
    select_book
)


# ============================================================
# CLOSE
# ============================================================

def on_closing():

    confirm = messagebox.askokcancel(
        "Exit Library Hub",
        "Are you sure you want to close the Library Management System?"
    )

    if confirm:
        root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    on_closing
)


# ============================================================
# START
# ============================================================

refresh_table()
update_dashboard()
update_record_count()
clear_form()

root.mainloop()

