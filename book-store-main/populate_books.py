import tkinter as tk
from PIL import Image, ImageTk

def populate_books(container, books, row_start, section_title):
    title_label = tk.Label(container, text=section_title, font=("Merriweather-Black", 18, "bold"), bg="#FAF9F6")
    title_label.grid(row=row_start, column=0, sticky="w", padx=20, pady=10)

    # Create a canvas for scrolling
    canvas = tk.Canvas(container, bg="#FAF9F6")
    scroll_frame = tk.Frame(canvas, bg="#FAF9F6")

    # Create window in the canvas
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Populate the scroll frame with book frames
    for idx, book in enumerate(books):
        frame = tk.Frame(scroll_frame, bg="#FFFFFF", relief="raised", padx=10, pady=10)
        frame.grid(row=0, column=idx, padx=10, pady=10)

        # Prevent resizing
        frame.grid_propagate(False)

        # Set the frame's width explicitly
        frame_label = tk.Label(frame, bg="#FFFFFF", width=30)  # Adjust width
        frame_label.pack(fill='both', expand=True)

        # Book image
        image = Image.open(book["image"]).resize((100, 150))
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(frame, image=img, bg="#FFFFFF")
        img_label.image = img
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

    # Create arrow buttons
    def scroll_left():
        canvas.xview_scroll(-1, "units")  # Scroll left
        update_scroll_buttons()

    def scroll_right():
        canvas.xview_scroll(1, "units")  # Scroll right
        update_scroll_buttons()

    left_button = tk.Button(container, text="←", command=scroll_left, font=("Merriweather-Black", 14), bg="#656D71",fg='white')
    right_button = tk.Button(container, text="→", command=scroll_right, font=("Merriweather-Black", 14), bg="#656D71",fg='white')

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