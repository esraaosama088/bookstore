import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from setting import show_page, show_settings_page
from cart_page import *
from create_management_page import create_management_page
from try2 import category
# Function to center the window
from center_window import center_window

# Function to create the SQLite database and table
from create_database import create_database

# Assuming `get_balance` is already defined
from get_balance import get_balance

# Function to check if a user already exists in the database
from user_exists import user_exists

# Function to show profile page
from show_profile_page import show_profile_page

# Function to insert user data into the database
from insert_user import insert_user

# Function to check user credentials during sign-in
from check_user_credentials import check_user_credentials, check_admin_credentials

from show_home_page import show_home_page
from populate_books import populate_books
from global_var import user_instance

# Global variable to track the current window
current_window = None

def handle_profile_click():
    global user_instance
    for widget in main_frames.winfo_children():
        widget.destroy()

    show_profile_page(main_frames,user_instance)

def create_main_app(user_id):
    global main_frames
    global root

    root = tk.Tk()
    root.title("Book Store App")
    main_frames = tk.Frame(root)
    main_frames.pack(fill="both", expand=True)
    root.geometry("1200x800")
    root.configure(bg="#FAF9F6")

    # Sidebar
    sidebar = tk.Frame(root, bg="#656D71", width=250)
    sidebar.pack(side="left", fill="y")

    # User Info
    user_img = Image.open("icons/user.png").resize((50, 50))
    user_img_tk = ImageTk.PhotoImage(user_img)
    user_img_label = tk.Label(sidebar, image=user_img_tk, bg="#656D71")
    user_img_label.pack(pady=20)
    
    print(user_instance)
    tk.Label(sidebar, text=user_instance, font=("Merriweather-Black", 14, "bold"), bg="#656D71",fg='white').pack()
    logout_btn = tk.Button(sidebar, text="LOG OUT", font=("Merriweather-Black", 10), bg="black", fg="white", relief="flat", command=log_out)
    logout_btn.pack(pady=10)

    # Sidebar Menu
    menu_items = [
        {"name": "Home", "icon": "icons/home.png"},
        {"name": "Categories", "icon": "icons/options-lines.png"},
        {"name": "Saved", "icon": "icons/bookmark.png"},
        {"name": "Recommendations", "icon": "icons/advice.png"},
        {"name": "Reviews", "icon": "icons/positive-review.png"},
        {"name": "Settings", "icon": "icons/settings.png"},
        {"name": "Profile", "icon": "icons/user.png", "command": lambda: print("Profile button clicked")},
        {"name": "Cart", "icon": "grocery-store.png"},
    ]

    for item in menu_items:
        icon = Image.open(item["icon"]).resize((20, 20))
        icon_tk = ImageTk.PhotoImage(icon)
        
        btn = tk.Button(
            sidebar,
            text=item["name"],
            image=icon_tk,
            compound="left",  # Icon on the left of the text
            font=("Merriweather-Black", 12),
            bg="#656D71",
            fg='#FAF9F6',
            anchor="w",
            relief="flat",
            padx=20,
            activebackground='#656D71',
            command= lambda name = item['name']:show_profile_page(main_frame,user_instance) if name=='Profile' else(
                show_home_page(main_frame) if name == 'Home' else(
                    show_page(show_settings_page,main_frame, user_id) if name=='Settings' else(
                        show_cart_page(main_frame)if name=='Cart' else(
                            category(main_frame) if name== 'Categories' else None
                        )
                    )
                )
            )
        )
        btn.image = icon_tk  # Keep a reference to prevent garbage collection
        btn.pack(fill="x", pady=5)
        

    # Main Content
    main_frame = tk.Frame(root, bg="#FAF9F6")
    main_frame.pack(side="right", fill="both", expand=True)

    # Sample Book Data
    popular_books = [
        {"title": "It Starts with Us", "author": "Colleen Hoover", "rating": 4, "image": "books-piled-.png"},
        {"title": "Fairy Tale", "author": "Stephen King", "rating": 5, "image": "books-piled-.png"},
        {"title": "The Thursday Murder Club", "author": "Richard Osman", "rating": 4, "image": "books-piled-.png"},
        {"title": "Normal People", "author": "Sally Rooney", "rating": 3, "image": "books-piled-.png"},
        {"title": "Atomic Habits", "author": "James Clear", "rating": 5, "image": "books-piled-.png"},
    ]
    
    recommended_books = [
        {"title": "Book A", "author": "Author A", "rating": 5, "image": "books-piled-.png"},
        {"title": "Book B", "author": "Author B", "rating": 4, "image": "books-piled-.png"},
    ]

    # Content Section
    content_frame = tk.Frame(main_frame, bg="#FAF9F6")
    content_frame.pack(fill="both", expand=True)
    populate_books(content_frame, popular_books, row_start=0, section_title="Popular")
    populate_books(content_frame, recommended_books, row_start=3, section_title="We Recommend")

    root.mainloop()


# def populate_books(container, books, row_start, section_title):
#     title_label = tk.Label(container, text=section_title, font=("Merriweather-Black", 18, "bold"), bg="#FAF9F6")
#     title_label.grid(row=row_start, column=0, sticky="w", padx=20, pady=10)

#     # Create a canvas for scrolling
#     canvas = tk.Canvas(container, bg="#FAF9F6")
#     scroll_frame = tk.Frame(canvas, bg="#FAF9F6")

#     # Create window in the canvas
#     canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

#     # Populate the scroll frame with book frames
#     for idx, book in enumerate(books):
#         frame = tk.Frame(scroll_frame, bg="#FFFFFF", relief="raised", padx=10, pady=10)
#         frame.grid(row=0, column=idx, padx=10, pady=10)

#         # Prevent resizing
#         frame.grid_propagate(False)

#         # Set the frame's width explicitly
#         frame_label = tk.Label(frame, bg="#FFFFFF", width=30)  # Adjust width
#         frame_label.pack(fill='both', expand=True)

#         # Book image
#         image = Image.open(book["image"]).resize((100, 150))
#         img = ImageTk.PhotoImage(image)
#         img_label = tk.Label(frame, image=img, bg="#FFFFFF")
#         img_label.image = img
#         img_label.pack()

#         # Book title
#         tk.Label(frame, text=book["title"], font=("Merriweather-Black", 12, "bold"), bg="#FFFFFF").pack(pady=5)
#         # Author
#         tk.Label(frame, text=f'by {book["author"]}', font=("Merriweather-Black", 10), fg="gray", bg="#FFFFFF").packf()
#         # Rating
#         tk.Label(frame, text="★" * book["rating"], font=("Merriweather-Black", 10), fg="gold", bg="#FFFFFF").pack()

#     # Update the scroll region
#     scroll_frame.update_idletasks()  # Refresh the frame
#     canvas.config(scrollregion=canvas.bbox("all"))  # Set the scroll region to encompass the scroll frame

#     # Create arrow buttons
#     def scroll_left():
#         canvas.xview_scroll(-1, "units")  # Scroll left
#         update_scroll_buttons()

#     def scroll_right():
#         canvas.xview_scroll(1, "units")  # Scroll right
#         update_scroll_buttons()

#     left_button = tk.Button(container, text="←", command=scroll_left, font=("Merriweather-Black", 14), bg="#656D71")
#     right_button = tk.Button(container, text="→", command=scroll_right, font=("Merriweather-Black", 14), bg="#656D71")

#     left_button.grid(row=row_start + 1, column=0, sticky="w", padx=(20, 0), pady=(5, 10))
#     right_button.grid(row=row_start + 1, column=0, sticky="e", padx=(0, 20), pady=(5, 10))

#     # Function to update button states based on scroll position
#     def update_scroll_buttons():
#         xview = canvas.xview()
#         left_button['state'] = 'normal' if xview[0] > 0 else 'disabled'
#         right_button['state'] = 'normal' if xview[1] < 1 else 'disabled'

#     # Initial button state update
#     update_scroll_buttons()

#     # Pack the canvas
#     canvas.grid(row=row_start + 1, column=0, sticky="ew", padx=20, pady=(0, 10))
#     container.grid_columnconfigure(0, weight=1)  # Allow the column to expand

def log_out():
    root.destroy()  # Close the main app window
    # from registration import create_registration_screen
    create_sign_in_window()  # Open the registration screen

# Function to update the visibility of the Admin Key field
def update_admin_key_field():
    global admin_key_entry_label, admin_key_entry
    role = role_var.get()

    # If the role is Admin, show the Admin Key field
    if role == "Admin":
        admin_key_entry_label.pack(pady=5)
        admin_key_entry.pack(pady=5)
    else:
        admin_key_entry_label.pack_forget()  # Hide the Admin Key label
        admin_key_entry.pack_forget()  # Hide the Admin Key entry field

# Function to navigate to the main app
def open_main_app(user_id):
    global current_window
    if current_window:
        current_window.destroy()
    create_main_app(user_id)  # Open the main app

# Function to handle sign-in
# For Sign In


def handle_sign_in():
    global user_instance
    username = username_entry.get()
    user_instance= username
    
    password = password_entry.get()
    admin_key = admin_key_entry.get() if admin_key_entry.winfo_ismapped() else ""  # Check if the admin key is visible
    role = role_var.get()
    
    if role == 'Admin':
        admin_id = check_admin_credentials(username, password, admin_key)
        if admin_id is not None:
            print("Admin Sign In successful")
            # we should pass the admin_id to this function
            create_management_page()
        else:
            print("Invalid username or password. Try again.")
            messagebox.showerror("error", "Invalid credentials. Try again.")
    else:
        user_id = check_user_credentials(username, password)
        if user_id is not None:
            print("User Sign In successful")
            open_main_app(user_id)
        else:
            print("Invalid username or password. Try again.")
            messagebox.showerror("error", "Invalid credentials. Try again.")

# For Sign Up
def handle_sign_up():
            global user_instance
            new_username = username_entry.get()
            user_instance = new_username
            new_password = password_entry.get()
            if(len(new_username)<6):
                if(new_username==""):
                    messagebox.showerror("error","username can't be empty")
                else:
                    messagebox.showerror("error","username can't be less than 6 characters")
            elif(len(new_password)<6):
                if(new_password==""):
                    messagebox.showerror("error","password can't be empty")
                else :
                    messagebox.showerror("error","password can't be less than 6 characters")
            else:
                if user_exists(new_username):
                    print("Username already exists. Please choose a different username.")
                else:
                # Insert the new user data into the database
                    insert_user(new_username, new_password)
                    open_main_app()

# def handle_sign_in():
#     username = username_entry.get()
#     password = password_entry.get()
#     admin_key = admin_key_entry.get()
#     role = role_var.get()
    
#     if role == 'Admin':
#         if check_admin_credentials(username, password, admin_key):
#             print("Admin Sign In successful")
#             create_management_page()
#         else:
#             print("Invalid username or password. Try again.")
#             messagebox.showerror("error", "Invalid credentials. Try again.")
#     else:
#         if check_user_credentials(username, password):
#             print("User Sign In successful")
#             open_main_app()
#         else:
#             print("Invalid username or password. Try again.")
#             messagebox.showerror("error", "Invalid credentials. Try again.")



# Function to create the sign-in window
def create_sign_in_window():
    global current_window, username_entry, password_entry, admin_key_entry, role_var,admin_key_entry_label
    if current_window:
        current_window.destroy()
    current_window = tk.Tk()
    current_window.title("Book Store - Sign In")
    current_window.configure(bg="#392F25")  # Set the background color here

    # Create frames for the layout
    main_frame = tk.Frame(current_window, bg="#392F25")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Load and display an image
    background_image = Image.open('bookstore.png').resize((400, 600))
    bg_img = ImageTk.PhotoImage(background_image)

    img_label = tk.Label(main_frame, image=bg_img, bg="#392F25")
    img_label.image = bg_img  # Keep a reference to prevent garbage collection
    img_label.pack(side="left", fill="both", expand=True)

    # Overlay text and input fields on the image
    text_frame = tk.Frame(main_frame, bg="#392F25")
    text_frame.pack(side="right", fill="both", expand=True, padx=20)

    tk.Label(text_frame, text="Sign In", font=("Merriweather-Black", 18, "bold"), bg="#392F25", fg="white").pack(pady=20)

    # Username input
    tk.Label(text_frame, text="Username", font=("Merriweather-Black", 12), bg="#392F25", fg="white").pack(pady=5)
    username_entry = tk.Entry(text_frame, font=("Merriweather-Black", 12), width=30)
    username_entry.pack(pady=5)

    # Password input
    tk.Label(text_frame, text="Password", font=("Merriweather-Black", 12), bg="#392F25", fg="white").pack(pady=5)
    password_entry = tk.Entry(text_frame, font=("Merriweather-Black", 12), show='*', width=30)
    password_entry.pack(pady=5)
    
    # # Admin Key input (only relevant for admin)
    # tk.Label(text_frame, text="Admin Key", font=("Merriweather-Black", 12), bg="#392F25", fg="white").pack(pady=5)
    # admin_key_entry = tk.Entry(text_frame, font=(#392F25"Merriweather-Black", 12), show='*', width=30)
    # admin_key_entry.pack(pady=5)
# Inside create_sign_in_window or create_sign_up_window

# In create_sign_in_window or create_sign_up_window
    admin_key_entry_label = tk.Label(text_frame, text="Admin Key", font=("Merriweather-Black", 12), bg="#392F25", fg="white")
    admin_key_entry = tk.Entry(text_frame, font=("Merriweather-Black", 12), show='*', width=30)

    # Initially hide the Admin Key field
    admin_key_entry_label.pack_forget()
    admin_key_entry.pack_forget()



    role_var = tk.StringVar(value="User")  # Default role is "User"

    # Add radio buttons for selecting the role
    tk.Radiobutton(text_frame, text="User", variable=role_var, value="User", font=("Merriweather-Black", 12), bg="#392F25", fg="white", selectcolor="#392F25", command=update_admin_key_field).pack(anchor="w")
    tk.Radiobutton(text_frame, text="Admin", variable=role_var, value="Admin", font=("Merriweather-Black", 12), bg="#392F25", fg="white", selectcolor="#392F25", command=update_admin_key_field).pack(anchor="w")


    # Role selection
    # role_var = tk.StringVar(value="User")  # Default role is "User"
    # tk.Label(text_frame, text="Select Role", font=("Merriweather-Black", 12), bg="#392F25", fg="white").pack(pady=5)
    # tk.Radiobutton(text_frame, text="User", variable=role_var, value="User", font=("Merriweather-Black", 12), bg="#392F25", fg="white", selectcolor="#392F25").pack(anchor="w")
    # tk.Radiobutton(text_frame, text="Admin", variable=role_var, value="Admin", font=("Merriweather-Black", 12), bg="#392F25", fg="white", selectcolor="#392F25").pack(anchor="w")

    # Sign In button
    # tk.Button(text_frame, text="Sign In", font=("Merriweather-Black", 14, "bold"), bg="#656D71", fg="black", command=handle_sign_in).pack(pady=20)
    sign_in_btn = tk.Button(text_frame, text="Sign In", font=("Merriweather-Black", 12), bg="#656D71", fg="white", width=20, command=handle_sign_in)
    sign_in_btn.pack(pady=20)
    # Switch to sign-up
    # switch_to_sign_up_label = tk.Label(text_frame, text="Don't have an account? Sign Up", font=("Merriweather-Black", 10), bg="#656D71", fg="white", cursor="hand2")
    # switch_to_sign_up_label.pack(pady=10)
    # switch_to_sign_up_label.bind("<Button-1>", lambda e: create_sign_up_window())
    sign_up_nav_btn = tk.Button(text_frame, text="Don't have an account? Sign Up", font=("Merriweather-Black", 10), bg="#656D71", fg="white", command=create_sign_up_window)
    sign_up_nav_btn.pack(pady=10)

    current_window.mainloop()

# Function to create the sign-up window
def create_sign_up_window():
    global current_window, username_entry, password_entry, email_entry, role_var
    if current_window:
        current_window.destroy()
    current_window = tk.Tk()
    current_window.title("Book Store - Sign Up")
    current_window.configure(bg="#392F25")  # Set the background color here

    # Create frames for the layout
    main_frame = tk.Frame(current_window, bg="#392F25")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Load and display an image
    background_image = Image.open('bookstore.png').resize((400, 600))
    bg_img = ImageTk.PhotoImage(background_image)

    img_label = tk.Label(main_frame, image=bg_img, bg="#392F25")
    img_label.image = bg_img  # Keep a reference to prevent garbage collection
    img_label.pack(side="left", fill="both", expand=True)

    # Overlay text and input fields on the image
    text_frame = tk.Frame(main_frame, bg="#392F25")
    text_frame.pack(side="right", fill="both", expand=True, padx=20)

    tk.Label(text_frame, text="Sign Up", font=("Merriweather-Black", 18, "bold"), bg="#392F25", fg="white").pack(pady=20)

    # Username input
    tk.Label(text_frame, text="Username", font=("Merriweather-Black", 12), bg="#392F25", fg="white").pack(pady=5)
    username_entry = tk.Entry(text_frame, font=("Merriweather-Black", 12), width=30)
    username_entry.pack(pady=5)
    # # Email input
    # tk.Label(text_frame, text="Email", font=("Merriweather-Black", 12), bg="#392F25", fg="white").pack(pady=5)
    # email_entry = tk.Entry(text_frame, font=("Merriweather-Black", 12), width=30)
    # email_entry.pack(pady=5)

    # Password input
    tk.Label(text_frame, text="Password", font=("Merriweather-Black", 12), bg="#392F25", fg="white").pack(pady=5)
    password_entry = tk.Entry(text_frame, font=("Merriweather-Black", 12), show='*', width=30)
    password_entry.pack(pady=5)
    


    # # Role selection
    # role_var = tk.StringVar(value="User")  # Default role is "User"
    # tk.Label(text_frame, text="Select Role", font=("Merriweather-Black", 12), bg="#392F25", fg="white").pack(pady=5)
    # tk.Radiobutton(text_frame, text="User", variable=role_var, value="User", font=("Merriweather-Black", 12), bg="#392F25", fg="white", selectcolor="#392F25").pack(anchor="w")
    # tk.Radiobutton(text_frame, text="Admin", variable=role_var, value="Admin", font=("Merriweather-Black", 12), bg="#392F25", fg="white", selectcolor="#392F25").pack(anchor="w")

    # Sign Up button
    # tk.Button(text_frame, text="Sign Up", font=("Merriweather-Black", 14, "bold"), bg="#656D71", fg="black", command=handle_sign_up).pack(pady=20)
    sign_in_btn = tk.Button(text_frame, text="Sign Up", font=("Merriweather-Black", 12), bg="#656D71", fg="white", width=20, command=handle_sign_up)
    sign_in_btn.pack(pady=20)
    # Switch to sign-in
    # switch_to_sign_in_label = tk.Label(text_frame, text="Already have an account? Sign In", font=("Merriweather-Black", 12), bg="#392F25", fg="white", cursor="hand2")
    # switch_to_sign_in_label.pack(pady=10)
    # switch_to_sign_in_label.bind("<Button-1>", lambda e: create_sign_in_window())
    sign_up_nav_btn = tk.Button(text_frame, text="Already have an account? Sign In", font=("Merriweather-Black", 10), bg="#656D71", fg="white", command=create_sign_in_window)
    sign_up_nav_btn.pack(pady=10)


    current_window.mainloop()

if __name__ == "__main__":
    create_sign_in_window()
