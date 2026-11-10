from tkinter import *
from tkinter import ttk, messagebox
import csv
import os

# Store books in memory
books = {}

# File used to save book records
BOOK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.txt")

# Remember the ISBN of the book selected for editing
selected_isbn = None


# Save all book records to a text file
def save_books():
    try:
        with open(BOOK_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="\t")

            for isbn, book in books.items():
                writer.writerow([
                    isbn,
                    book["title"],
                    book["author"],
                    book["quantity"]
                ])

        return True

    except OSError:
        messagebox.showerror("File Error", "Could not save the book records.")
        return False


# Load book records from the text file
def load_books():
    if not os.path.exists(BOOK_FILE):
        return

    try:
        with open(BOOK_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="\t")

            for row in reader:
                if len(row) == 4:
                    isbn, title, author, quantity = row

                    try:
                        quantity = int(quantity)

                        if quantity >= 0:
                            books[isbn] = {
                                "title": title,
                                "author": author,
                                "quantity": quantity
                            }
                    except ValueError:
                        continue

    except OSError:
        messagebox.showerror("File Error", "Could not load the saved book records.")


# Clear input boxes
def clear_boxes():
    global selected_isbn
    isbn_input_txt.delete(0, END)
    title_input_txt.delete(0, END)
    author_input_txt.delete(0, END)
    quantity_input_txt.delete(0, END)
    search_input_txt.delete(0, END)
    selected_isbn = None


# Update the table with book records
def display_books():
    for item in book_table.get_children():
        book_table.delete(item)

    for isbn, book in books.items():
        if book["quantity"] > 0:
            status = "Available"
        else:
            status = "Out of stock"

        book_table.insert(
            "", END,
            values=(isbn, book["title"], book["author"],
                    book["quantity"], status)
        )


# Add a new book
def add_book():
    isbn = isbn_input_txt.get().strip()
    title = title_input_txt.get().strip()
    author = author_input_txt.get().strip()
    quantity = quantity_input_txt.get().strip()

    if isbn == "" or title == "" or author == "" or quantity == "":
        messagebox.showerror("Error", "Please fill in all boxes.")
        return

    try:
        quantity = int(quantity)
        if quantity < 0:
            messagebox.showerror("Error", "Quantity cannot be negative.")
            return
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a whole number.")
        return

    if isbn in books:
        messagebox.showerror("Error", "This ISBN already exists.")
        return

    books[isbn] = {
        "title": title,
        "author": author,
        "quantity": quantity
    }

    if not save_books():
        del books[isbn]
        return

    messagebox.showinfo("Success", "Book added successfully!")
    clear_boxes()
    display_books()


# Search by ISBN, title, or author
def search_book():
    search = search_input_txt.get().strip().lower()

    for item in book_table.get_children():
        book_table.delete(item)

    found = False

    for isbn, book in books.items():
        if (search in isbn.lower()
                or search in book["title"].lower()
                or search in book["author"].lower()):

            if book["quantity"] > 0:
                status = "Available"
            else:
                status = "Out of stock"

            book_table.insert(
                "", END,
                values=(isbn, book["title"], book["author"],
                        book["quantity"], status)
            )
            found = True

    if not found:
        messagebox.showinfo("Search", "No matching book was found.")


# Put the selected book's details into the input boxes
def select_book(event):
    global selected_isbn

    selected_item = book_table.focus()

    if selected_item:
        details = book_table.item(selected_item, "values")

        selected_isbn = details[0]

        isbn_input_txt.delete(0, END)
        isbn_input_txt.insert(0, details[0])

        title_input_txt.delete(0, END)
        title_input_txt.insert(0, details[1])

        author_input_txt.delete(0, END)
        author_input_txt.insert(0, details[2])

        quantity_input_txt.delete(0, END)
        quantity_input_txt.insert(0, details[3])


# Edit the selected book
def edit_book():
    global selected_isbn

    if selected_isbn is None or selected_isbn not in books:
        messagebox.showerror("Error", "Please select a book from the table first.")
        return

    new_isbn = isbn_input_txt.get().strip()
    title = title_input_txt.get().strip()
    author = author_input_txt.get().strip()
    quantity = quantity_input_txt.get().strip()

    if new_isbn == "" or title == "" or author == "" or quantity == "":
        messagebox.showerror("Error", "Please fill in all boxes.")
        return

    try:
        quantity = int(quantity)
        if quantity < 0:
            messagebox.showerror("Error", "Quantity cannot be negative.")
            return
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a whole number.")
        return

    if new_isbn != selected_isbn and new_isbn in books:
        messagebox.showerror("Error", "This ISBN already exists.")
        return

    old_book = books[selected_isbn].copy()

    if new_isbn != selected_isbn:
        del books[selected_isbn]

    books[new_isbn] = {
        "title": title,
        "author": author,
        "quantity": quantity
    }

    if not save_books():
        if new_isbn != selected_isbn:
            del books[new_isbn]
        books[selected_isbn] = old_book
        return

    messagebox.showinfo("Success", "Book details updated successfully!")
    clear_boxes()
    display_books()


# Borrow one copy of a book
def borrow_book():
    isbn = isbn_input_txt.get().strip()

    if isbn not in books:
        messagebox.showerror("Error", "Enter or select a valid ISBN.")
        return

    if books[isbn]["quantity"] == 0:
        messagebox.showerror("Error", "No copies are available.")
        return

    books[isbn]["quantity"] -= 1

    if not save_books():
        books[isbn]["quantity"] += 1
        return

    messagebox.showinfo("Success", "Book borrowed successfully!")
    display_books()


# Return one copy of a book
def return_book():
    isbn = isbn_input_txt.get().strip()

    if isbn not in books:
        messagebox.showerror("Error", "Enter or select a valid ISBN.")
        return

    books[isbn]["quantity"] += 1

    if not save_books():
        books[isbn]["quantity"] -= 1
        return

    messagebox.showinfo("Success", "Book returned successfully!")
    display_books()


# Show books with fewer than 3 copies
def low_stock():
    for item in book_table.get_children():
        book_table.delete(item)

    for isbn, book in books.items():
        if book["quantity"] < 3:
            if book["quantity"] > 0:
                status = "Available"
            else:
                status = "Out of stock"

            book_table.insert(
                "", END,
                values=(isbn, book["title"], book["author"],
                        book["quantity"], status)
            )


# Save records and close the program
def close_program():
    if save_books():
        window.destroy()


# Main window
window = Tk()
window.title("Library Management System")
window.geometry("1000x700")
window.minsize(850, 620)
window.configure(bg="#F3F6FB")

# Colours
blue = "#2457A7"
dark_blue = "#183B70"
white = "#FFFFFF"
grey = "#64748B"

# Heading
heading = Label(
    window,
    text="Library Management System",
    font=("Arial", 22, "bold"),
    bg=blue,
    fg=white,
    padx=15,
    pady=15
)
heading.pack(fill=X)

# Main area
main_frame = Frame(window, bg="#F3F6FB", padx=18, pady=18)
main_frame.pack(fill=BOTH, expand=True)

# Left side: book details
details_frame = LabelFrame(
    main_frame,
    text="Book Details",
    font=("Arial", 12, "bold"),
    bg=white,
    fg=dark_blue,
    padx=15,
    pady=12
)
details_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

Label(details_frame, text="ISBN", bg=white, font=("Arial", 10, "bold")).grid(
    row=0, column=0, sticky="w", pady=(4, 2)
)
isbn_input_txt = Entry(details_frame, font=("Arial", 11), width=28)
isbn_input_txt.grid(row=1, column=0, sticky="ew", pady=(0, 10))

Label(details_frame, text="Book Title", bg=white, font=("Arial", 10, "bold")).grid(
    row=2, column=0, sticky="w", pady=(4, 2)
)
title_input_txt = Entry(details_frame, font=("Arial", 11), width=28)
title_input_txt.grid(row=3, column=0, sticky="ew", pady=(0, 10))

Label(details_frame, text="Author", bg=white, font=("Arial", 10, "bold")).grid(
    row=4, column=0, sticky="w", pady=(4, 2)
)
author_input_txt = Entry(details_frame, font=("Arial", 11), width=28)
author_input_txt.grid(row=5, column=0, sticky="ew", pady=(0, 10))

Label(details_frame, text="Quantity", bg=white, font=("Arial", 10, "bold")).grid(
    row=6, column=0, sticky="w", pady=(4, 2)
)
quantity_input_txt = Entry(details_frame, font=("Arial", 11), width=28)
quantity_input_txt.grid(row=7, column=0, sticky="ew", pady=(0, 14))

add_btn = Button(
    details_frame, text="Add Book", command=add_book,
    bg=blue, fg=white, activebackground=dark_blue,
    activeforeground=white, font=("Arial", 10, "bold"),
    relief=FLAT, padx=10, pady=7, cursor="hand2"
)
add_btn.grid(row=8, column=0, sticky="ew", pady=(0, 7))

edit_btn = Button(
    details_frame, text="Edit Book", command=edit_book,
    bg="#7656C9", fg=white, activebackground="#5E43A5",
    activeforeground=white, font=("Arial", 10, "bold"),
    relief=FLAT, padx=10, pady=7, cursor="hand2"
)
edit_btn.grid(row=9, column=0, sticky="ew", pady=(0, 7))

clear_btn = Button(
    details_frame, text="Clear Form", command=clear_boxes,
    font=("Arial", 10), relief=GROOVE, padx=10, pady=6, cursor="hand2"
)
clear_btn.grid(row=10, column=0, sticky="ew", pady=(0, 14))

# Borrow and return actions
Label(
    details_frame, text="Book Actions",
    font=("Arial", 12, "bold"), bg=white, fg=dark_blue
).grid(row=11, column=0, sticky="w", pady=(2, 8))

borrow_btn = Button(
    details_frame, text="Borrow Book", command=borrow_book,
    bg="#237A4B", fg=white, activebackground="#195D38",
    activeforeground=white, font=("Arial", 10, "bold"),
    relief=FLAT, padx=10, pady=7, cursor="hand2"
)
borrow_btn.grid(row=12, column=0, sticky="ew", pady=(0, 7))

return_btn = Button(
    details_frame, text="Return Book", command=return_book,
    bg="#E8EEF8", fg=dark_blue, font=("Arial", 10, "bold"),
    relief=FLAT, padx=10, pady=7, cursor="hand2"
)
return_btn.grid(row=13, column=0, sticky="ew", pady=(0, 12))

exit_btn = Button(
    details_frame, text="Exit Program", command=close_program,
    bg="#C94C4C", fg=white, activebackground="#A93636",
    activeforeground=white, font=("Arial", 10, "bold"),
    relief=FLAT, padx=10, pady=7, cursor="hand2"
)
exit_btn.grid(row=14, column=0, sticky="ew")

# Right side: search and book records
records_frame = LabelFrame(
    main_frame,
    text="Find and View Books",
    font=("Arial", 12, "bold"),
    bg=white,
    fg=dark_blue,
    padx=12,
    pady=12
)
records_frame.grid(row=0, column=1, sticky="nsew")

Label(
    records_frame, text="Search by ISBN, title, or author",
    bg=white, font=("Arial", 10)
).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

search_input_txt = Entry(records_frame, font=("Arial", 11))
search_input_txt.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(0, 12))

search_btn = Button(
    records_frame, text="Search", command=search_book,
    bg=blue, fg=white, activebackground=dark_blue,
    activeforeground=white, font=("Arial", 10, "bold"),
    relief=FLAT, padx=14, pady=5, cursor="hand2"
)
search_btn.grid(row=1, column=1, sticky="ew", pady=(0, 12))

# Table of books
columns = ("ISBN", "Title", "Author", "Quantity", "Status")
book_table = ttk.Treeview(
    records_frame, columns=columns, show="headings", height=16
)

for column in columns:
    book_table.heading(column, text=column)
    book_table.column(column, width=100, anchor="w")

book_table.column("ISBN", width=115)
book_table.column("Title", width=150)
book_table.column("Author", width=120)
book_table.column("Quantity", width=70, anchor="center")
book_table.column("Status", width=100, anchor="center")

book_table.grid(row=2, column=0, columnspan=2, sticky="nsew")

# Scroll bar for the table
scrollbar = ttk.Scrollbar(
    records_frame, orient=VERTICAL, command=book_table.yview
)
scrollbar.grid(row=2, column=2, sticky="ns")
book_table.configure(yscrollcommand=scrollbar.set)

book_table.bind("<<TreeviewSelect>>", select_book)

# Other display options
bottom_buttons = Frame(records_frame, bg=white)
bottom_buttons.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))

display_btn = Button(
    bottom_buttons, text="Display All Books", command=display_books,
    font=("Arial", 9, "bold"), relief=GROOVE, padx=8, pady=6, cursor="hand2"
)
display_btn.pack(side=LEFT, padx=(0, 8))

low_stock_btn = Button(
    bottom_buttons, text="Low Stock (Below 3)", command=low_stock,
    font=("Arial", 9, "bold"), relief=GROOVE, padx=8, pady=6, cursor="hand2"
)
low_stock_btn.pack(side=LEFT)

# Allow the two main sections to resize
main_frame.grid_columnconfigure(0, weight=0, minsize=250)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
details_frame.grid_columnconfigure(0, weight=1)
records_frame.grid_columnconfigure(0, weight=1)
records_frame.grid_rowconfigure(2, weight=1)

# Load saved books when the program starts
load_books()
display_books()

# Save records when the window's X button is clicked
window.protocol("WM_DELETE_WINDOW", close_program)

window.mainloop()
