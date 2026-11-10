from tkinter import *
from tkinter import messagebox


# Library management
books = {}


# Add book
def add_book():

    isbn = isbn_input_txt.get()
    title = title_input_txt.get()
    author = author_input_txt.get()
    quantity = quantity_input_txt.get()

    if isbn == "" or title == "" or author == "" or quantity == "":
        messagebox.showerror("Error", "Please fill in all boxes.")
        return

    try:
        quantity = int(quantity)

        if quantity < 0:
            messagebox.showerror("Error", "Quantity cannot be negative.")
            return

    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number.")
        return

    if isbn in books:
        messagebox.showerror("Error", "This ISBN already exists.")
        return

    books[isbn] = {
        "title": title,
        "author": author,
        "quantity": quantity
    }

    messagebox.showinfo("Success", "Book added!")

    clear_boxes()
    display_books()


# Display book
def display_books():

    output.delete("1.0", END)

    if len(books) == 0:
        output.insert(END, "No books in the library.")
        return

    for isbn in books:

        output.insert(END, "ISBN: " + isbn + "\n")
        output.insert(END, "Title: " + books[isbn]["title"] + "\n")
        output.insert(END, "Author: " + books[isbn]["author"] + "\n")
        output.insert(END, "Quantity: " +
                      str(books[isbn]["quantity"]) + "\n")
        output.insert(END, "----------------------\n")


# Search
def search_book():

    search = search_input_txt.get().lower()

    output.delete("1.0", END)

    found = False

    for isbn in books:

        title = books[isbn]["title"]
        author = books[isbn]["author"]

        if (search in isbn.lower() or
            search in title.lower() or
            search in author.lower()):

            output.insert(END, "ISBN: " + isbn + "\n")
            output.insert(END, "Title: " + title + "\n")
            output.insert(END, "Author: " + author + "\n")
            output.insert(END, "Quantity: " +
                          str(books[isbn]["quantity"]) + "\n")
            output.insert(END, "----------------------\n")

            found = True

    if found == False:
        output.insert(END, "Book not found.")


# Borrow book
def borrow_book():

    isbn = isbn_input_txt.get()

    if isbn not in books:
        messagebox.showerror("Error", "Book not found.")
        return

    if books[isbn]["quantity"] == 0:
        messagebox.showerror("Error", "No copies available.")
        return

    books[isbn]["quantity"] -= 1

    messagebox.showinfo("Success", "Book borrowed!")

    display_books()


# Return book
def return_book():

    isbn = isbn_input_txt.get()

    if isbn not in books:
        messagebox.showerror("Error", "Book not found.")
        return

    books[isbn]["quantity"] += 1

    messagebox.showinfo("Success", "Book returned!")

    display_books()


# Low stock
def low_stock():

    output.delete("1.0", END)

    found = False

    for isbn in books:

        if books[isbn]["quantity"] < 3:

            output.insert(END, "ISBN: " + isbn + "\n")
            output.insert(END, "Title: " +
                          books[isbn]["title"] + "\n")
            output.insert(END, "Quantity: " +
                          str(books[isbn]["quantity"]) + "\n")
            output.insert(END, "----------------------\n")

            found = True

    if found == False:
        output.insert(END, "No low-stock books.")


# Clear
def clear_boxes():

    isbn_input_txt.delete(0, END)
    title_input_txt.delete(0, END)
    author_input_txt.delete(0, END)
    quantity_input_txt.delete(0, END)
    search_input_txt.delete(0, END)


# GUI
window = Tk()
window.geometry("650x650")
window.title("Library Management System")


# Heading
lbl0 = Label(window,text="Library Management System",font=("Arial Bold", 20))
lbl0.grid(column=0, row=0, sticky="W")


# ISBN
isbn_lbl = Label(window,text="ISBN:",font=("Arial Bold", 12))
isbn_lbl.grid(column=0, row=1, sticky="W")
isbn_input_txt = Entry(window,width=30,font=("Arial", 12))
isbn_input_txt.grid(column=0,row=2,sticky="W",padx=5,pady=5)


# Title
title_lbl = Label(window,text="Book Title:",font=("Arial Bold", 12))
title_lbl.grid(column=0, row=3, sticky="W")
title_input_txt = Entry(window,width=30,font=("Arial", 12))
title_input_txt.grid(column=0,row=4,sticky="W",padx=5,pady=5)


# Author
author_lbl = Label(window,text="Author:",font=("Arial Bold", 12))
author_lbl.grid(column=0, row=5, sticky="W")
author_input_txt = Entry(window,width=30,font=("Arial", 12))
author_input_txt.grid(column=0,row=6,sticky="W",padx=5,pady=5)


# Quantity
quantity_lbl = Label(window,text="Quantity:",font=("Arial Bold", 12))
quantity_lbl.grid(column=0, row=7, sticky="W")
quantity_input_txt = Entry(window,width=30,font=("Arial", 12))
quantity_input_txt.grid(column=0,row=8,sticky="W",padx=5,pady=5)


# Checkbox
available_state = BooleanVar()
available_chk = Checkbutton(window,text="Book is available",font=("Arial Bold", 12),var=available_state)
available_chk.grid(column=0,row=9,sticky="W")


# Radio buttons
action_lbl = Label(window,text="Action:",font=("Arial Bold", 12))
action_lbl.grid(column=0,row=10,sticky="W")

selected = IntVar()
selected.set(0)

borrow_rad = Radiobutton(window,text="Borrow",value=0,variable=selected)
borrow_rad.grid(column=0,row=11,sticky="W")

return_rad = Radiobutton(window,text="Return",value=1,variable=selected)
return_rad.grid(column=0,row=12,sticky="W")


# Buttons
add_btn = Button(window,text="Add Book",command=add_book)
add_btn.grid(column=0,row=13,sticky="W",padx=5,pady=5)

borrow_btn = Button(window,text="Borrow Book",command=borrow_book)
borrow_btn.grid(column=0,row=14,sticky="W",padx=5,pady=5)

return_btn = Button(window,text="Return Book",command=return_book)
return_btn.grid(column=0,row=15,sticky="W",padx=5,pady=5)

display_btn = Button(window,text="Display Books",command=display_books)
display_btn.grid(column=0,row=16,sticky="W",padx=5,pady=5)

low_stock_btn = Button(window,text="Low Stock",command=low_stock)
low_stock_btn.grid(column=0,row=17,sticky="W",padx=5,pady=5)

clear_btn = Button(window,text="Clear",command=clear_boxes)
clear_btn.grid(column=0,row=18,sticky="W",padx=5,pady=5)


# Search
search_lbl = Label(window,text="Search:",font=("Arial Bold", 12))
search_lbl.grid(column=1,row=1,sticky="W")
search_input_txt = Entry(window,width=30,font=("Arial", 12))
search_input_txt.grid(column=1,row=2,sticky="W",padx=5,pady=5)
search_btn = Button(window,text="Search",command=search_book)
search_btn.grid(column=1,row=3,sticky="W",padx=5,pady=5)


# Output
output = Text(window,width=50,height=20)
output.grid(column=1, row=4, rowspan=15, padx=10, pady=5)

window.mainloop()