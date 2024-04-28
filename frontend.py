import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel
import database

class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x1000")

        self.label = tk.Label(self.root, text="Welcome to Library Management System", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.add_book_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_book_button.pack(pady=5)

        self.borrow_book_button = tk.Button(self.root, text="Borrow Book", command=self.borrow_book)
        self.borrow_book_button.pack(pady=5)

        self.return_book_button = tk.Button(self.root, text="Return Book", command=self.return_book)
        self.return_book_button.pack(pady=5)

        self.display_all_books_button = tk.Button(self.root, text="Display All Books", command=self.display_all_books)
        self.display_all_books_button.pack(pady=5)

        self.user_sign_in()

    def user_sign_in(self):
        self.member_id = None
        self.member_role = None

        self.member_id_entry = tk.Entry(self.root)
        self.member_id_entry.pack(pady=5)
        self.member_id_entry.insert(0, "Member ID")

        self.member_role_var = tk.StringVar(self.root)
        self.member_role_var.set("Select Role")
        self.member_role_menu = tk.OptionMenu(self.root, self.member_role_var, "Author", "Reader")
        self.member_role_menu.pack(pady=5)

        self.sign_in_button = tk.Button(self.root, text="Sign In", command=self.sign_in)
        self.sign_in_button.pack(pady=5)

    def sign_in(self):
        member_id = self.member_id_entry.get()
        if member_id.isdigit() and self.member_role_var.get() in ["Author", "Reader"]:
            self.member_id = int(member_id)
            self.member_role = self.member_role_var.get()
            messagebox.showinfo("Success", f"Welcome, Member ID: {self.member_id}, Role: {self.member_role}")
        else:
            messagebox.showerror("Error", "Invalid Member ID or Role")

    def add_book(self):
        book_id = simpledialog.askinteger("Add Book", "Enter book ID:")
        title = simpledialog.askstring("Add Book", "Enter title:")
        author = simpledialog.askstring("Add Book", "Enter author:")
        genre = simpledialog.askstring("Add Book", "Enter genre:")
        available_copies = simpledialog.askinteger("Add Book", "Enter available copies:")

        if book_id is not None and title and author and genre and available_copies is not None:
            database.add_book(book_id, title, author, genre, available_copies)
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showerror("Error", "Please provide all information including book ID.")

    def borrow_book(self):
        if self.member_id is None or self.member_role is None:
            messagebox.showerror("Error", "Please sign in first.")
            return

        book_id = simpledialog.askinteger("Borrow Book", "Enter book ID:")
        if book_id is not None:
            if database.borrow_book(book_id, self.member_id, self.member_role):
                messagebox.showinfo("Success", "Book borrowed successfully!")
                self.update_displayed_books()
            else:
                messagebox.showerror("Error", "Failed to borrow book. Please check availability.")
        else:
            messagebox.showerror("Error", "Please provide book ID.")

    def return_book(self):
        if self.member_id is None or self.member_role is None:
            messagebox.showerror("Error", "Please sign in first.")
            return

        book_id = simpledialog.askinteger("Return Book", "Enter book ID:")
        if book_id is not None:
            if database.return_book(book_id, self.member_id, self.member_role):
                messagebox.showinfo("Success", "Book returned successfully!")
                self.update_displayed_books()
            else:
                messagebox.showerror("Error", "Failed to return book.")
        else:
            messagebox.showerror("Error", "Please provide book ID.")

    def display_all_books(self):
        all_books = database.get_available_books()
        if all_books:
            popup_window = Toplevel(self.root)
            popup_window.title("All Books")
            popup_window.geometry("400x300")

            book_text = "All Books:\n\n"
            for book in all_books:
                book_text += f"Title: {book[1]}\nAuthor: {book[2]}\nGenre: {book[3]}\nAvailable Copies: {book[4]}\n\n"
            all_books_label = tk.Label(popup_window, text=book_text, justify="left")
            all_books_label.pack(pady=10)
        else:
            messagebox.showinfo("Information", "No books found.")

    def update_displayed_books(self):
        self.display_all_books()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()


