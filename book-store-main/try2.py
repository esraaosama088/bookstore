import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Sample categories and books with additional details
categories = {
    "Fiction": [
        {"title": "Book 1", "author": "Author A", "rating": 4, "image": "books-piled-.png", "description": "A thrilling fiction book.", "price": "$15"},
        {"title": "Book 2", "author": "Author B", "rating": 5, "image": "books-piled-.png", "description": "An adventurous journey.", "price": "$20"},
        {"title": "Book 3", "author": "Author C", "rating": 3, "image": "books-piled-.png", "description": "A classic novel.", "price": "$12"},
        {"title": "Book 4", "author": "Author D", "rating": 5, "image": "books-piled-.png", "description": "A romantic fiction.", "price": "$18"},
        {"title": "Book 4", "author": "Author D", "rating": 5, "image": "books-piled-.png", "description": "A romantic fiction.", "price": "$18"},
        {"title": "Book 4", "author": "Author D", "rating": 5, "image": "books-piled-.png", "description": "A romantic fiction.", "price": "$18"},
        {"title": "Book 4", "author": "Author D", "rating": 5, "image": "books-piled-.png", "description": "A romantic fiction.", "price": "$18"},
        {"title": "Book 4", "author": "Author D", "rating": 5, "image": "books-piled-.png", "description": "A romantic fiction.", "price": "$18"},
        {"title": "Book 4", "author": "Author D", "rating": 5, "image": "books-piled-.png", "description": "A romantic fiction.", "price": "$18"},

    ],
    "Non-Fiction": [
        {"title": "Book 5", "author": "Author E", "rating": 4, "image": "books-piled-.png", "description": "An insightful non-fiction book.", "price": "$25"},
        {"title": "Book 6", "author": "Author F", "rating": 5, "image": "books-piled-.png", "description": "A deep dive into history.", "price": "$30"},
        {"title": "Book 7", "author": "Author G", "rating": 4, "image": "books-piled-.png", "description": "A biography worth reading.", "price": "$22"},
    ],
    "Science": [
        {"title": "Book 8", "author": "Author H", "rating": 3, "image": "books-piled-.png", "description": "A science exploration book.", "price": "$28"},
        {"title": "Book 9", "author": "Author I", "rating": 5, "image": "books-piled-.png", "description": "A scientific breakthrough.", "price": "$35"},
    ],
    "History": [
        {"title": "Book 10", "author": "Author J", "rating": 4, "image": "books-piled-.png", "description": "A historical memoir.", "price": "$27"},
        {"title": "Book 11", "author": "Author K", "rating": 5, "image": "books-piled-.png", "description": "A timeline of world history.", "price": "$32"},
        {"title": "Book 12", "author": "Author L", "rating": 4, "image": "books-piled-.png", "description": "A deep history book.", "price": "$24"},
    ],
}

def open_category_window(category_name):
    category_window = tk.Toplevel()
    # category_window = tk()
    category_window.geometry('800x600')
    category_window.title(f"{category_name} - Books")
    
    canvas = tk.Canvas(category_window, bg="#FAF9F6")
    scrollbar = ttk.Scrollbar(category_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for book in categories[category_name]:
        book_frame = ttk.Frame(scrollable_frame, borderwidth=1, relief="solid")
        book_frame.pack(pady=5, padx=5, fill="x")
        ttk.Label(book_frame, text=book["title"]).pack(padx=10, pady=10)
        ttk.Label(book_frame, text=f"Author: {book['author']}").pack(padx=10, pady=5)
        ttk.Label(book_frame, text=f"Rating: {'★' * book['rating']}").pack(padx=10, pady=5)
        ttk.Label(book_frame, text=f"Description: {book['description']}").pack(padx=10, pady=5)
        ttk.Label(book_frame, text=f"Price: {book['price']}").pack(padx=10, pady=5)

def populate_books(container, books, row_start, section_title):
    title_label = tk.Label(container, text=section_title, font=("Merriweather-Black", 18, "bold"), bg="#FAF9F6")
    title_label.grid(row=row_start, column=0, sticky="w", padx=20, pady=10)

    # Create a canvas for horizontal scrolling
    canvas = tk.Canvas(container, bg="#FAF9F6", width=700)  # Fixed width of 700px
    scroll_frame = tk.Frame(canvas, bg="#FAF9F6")
    
    # Create a window in the canvas
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Populate the scroll frame with book frames
    for idx, book in enumerate(books):
        frame = tk.Frame(scroll_frame, bg="#FFFFFF", relief="raised", padx=10, pady=10, width=150)  # Fixed width for each book
        frame.grid(row=0, column=idx, padx=10, pady=10)

        # Prevent resizing
        frame.grid_propagate(False)

        # Book image
        image = Image.open(book["image"]).resize((100, 150))
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(frame, image=img, bg="#FFFFFF")
        img_label.image = img  # Keep a reference
        img_label.pack()

        # Book title
        tk.Label(frame, text=book["title"], font=("Merriweather-Black", 12, "bold"), bg="#FFFFFF").pack(pady=5)
        # Author
        tk.Label(frame, text=f'by {book["author"]}', font=("Merriweather-Black", 10), fg="gray", bg="#FFFFFF").pack()
        # Rating
        tk.Label(frame, text="★" * book["rating"], font=("Merriweather-Black", 10), fg="gold", bg="#FFFFFF").pack()

    # Update the scroll region
    scroll_frame.update_idletasks()  # Refresh the frame
    canvas.config(scrollregion=canvas.bbox("all"))  # Set the scroll region to encompass the scroll frame

    # Create arrow buttons for horizontal scrolling
    def scroll_left():
        canvas.xview_scroll(-1, "units")  # Scroll left
        update_scroll_buttons()

    def scroll_right():
        canvas.xview_scroll(1, "units")  # Scroll right
        update_scroll_buttons()

    left_button = tk.Button(container, text="←", command=scroll_left, font=("Merriweather-Black", 14), bg="#FCE6C9")
    right_button = tk.Button(container, text="→", command=scroll_right, font=("Merriweather-Black", 14), bg="#FCE6C9")

    left_button.grid(row=row_start + 1, column=0, sticky="w", padx=(20, 0), pady=(5, 10))
    right_button.grid(row=row_start + 1, column=0, sticky="e", padx=(0, 20), pady=(5, 10))

    # Function to update button states based on scroll position
    def update_scroll_buttons():
        xview = canvas.xview()
        left_button['state'] = 'normal' if xview[0] > 0 else 'disabled'
        right_button['state'] = 'normal' if xview[1] < 1 else 'disabled'

    # Initial button state update
    update_scroll_buttons()

    # Pack the canvas
    canvas.grid(row=row_start + 1, column=0, sticky="ew", padx=20, pady=(0, 10))
    container.grid_columnconfigure(0, weight=1)  # Allow the column to expand
    
    # "Read More" button to open the category window
    read_more_button = tk.Button(container, text="Read More", command=lambda: open_category_window(section_title), font=("Merriweather-Black", 12), bg="#FCE6C9")
    read_more_button.grid(row=row_start + 2, column=0, pady=(5, 10))


def show_page(page_function, main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()  # Remove existing widgets
    page_function(main_frame)

def category(main_frame):

    # global root
    # root = tk.Tk()
    # root.title("Book Store App")
    
    # root.geometry("700x600")
    # root.config(bg="#FAF9F6")

    for widget in main_frame.winfo_children():
        widget.destroy()

    # Settings Page Frame
    cat_frame = tk.Frame(main_frame, bg="#FAF9F6")
    cat_frame.pack(fill="both", expand=True, padx=20, pady=20)
    tk.Label(cat_frame, text="Categories", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))


    # Main content frame with scrolling
    # main_frame = tk.Frame(root, bg="#FAF9F6")
    # main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    main_canvas = tk.Canvas(cat_frame, bg="#FAF9F6")
    main_scrollable_frame = ttk.Frame(main_canvas)

    # Create a window in the canvasettings
    main_canvas.create_window((0, 0), window=main_scrollable_frame, anchor="nw")

    # Vertical scrollbar
    vertical_scrollbar = ttk.Scrollbar(cat_frame, orient="vertical", command=main_canvas.yview)
    main_canvas.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side="right", fill="y")

    main_canvas.pack(side="left", fill="both", expand=True)

    # Bind the configure event to update the scroll region
    main_scrollable_frame.bind(
        "<Configure>",
        lambda e: main_canvas.configure(
            scrollregion=main_canvas.bbox("all")
        )
    )
    
    # Section for each category
    row_start = 0
    for category, books in categories.items():
        populate_books(main_scrollable_frame, books, row_start, category)
        row_start += 3  # Adjust row start for the next category

    # root.mainloop()

# if __name__ == "__main__":
#     create_main_app()
