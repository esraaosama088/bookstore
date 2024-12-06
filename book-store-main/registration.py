import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

# Function to create the SQLite database and table
def create_database():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT
    )
    """)
    conn.commit()
    conn.close()

# Function to check if a user already exists in the database
def user_exists(username):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Function to insert user data into the database
def insert_user(username, password, email):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO settings (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()

# Function to check user credentials during sign-in
def check_user_credentials(username, password):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings WHERE username = ? AND password = ?", (username, password))
    valid = cursor.fetchone() is not None
    conn.close()
    return valid

# Function to fetch user data
def get_user_data():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings WHERE id = 1")  # Assuming user ID is 1
    user = cursor.fetchone()
    conn.close()
    return user

# Function to update user data in the database
def update_user_in_database(new_email, new_password):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE settings SET email = ?, password = ? WHERE id = ?", 
                       (new_email, new_password, 1))  # Assuming user ID is 1
        conn.commit()
        return True
    except Exception as e:
        print(f"An error occurred while updating: {e}")
        return False
    finally:
        conn.close()

# Function to center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Function to show profile page and allow updates
def show_profile_page(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    profile_frame = tk.Frame(main_frame, bg="#FAF9F6")
    profile_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(profile_frame, text="Profile", font=("Arial", 24, "bold"), bg="#FAF9F6").pack(pady=(10, 20))

    user_data = get_user_data()  # Fetch user data from database
    username = user_data[1]  # Assuming index 1 is username
    email = user_data[3]      # Assuming index 3 is email

    tk.Label(profile_frame, text="Username:", font=("Arial", 14), bg="#FAF9F6").pack(anchor="w")
    username_label = tk.Label(profile_frame, text=username, font=("Arial", 12), bg="#FAF9F6")
    username_label.pack(anchor="w", padx=10)

    tk.Label(profile_frame, text="Email:", font=("Arial", 14), bg="#FAF9F6").pack(anchor="w")
    email_var = tk.StringVar(value=email)
    email_entry = tk.Entry(profile_frame, textvariable=email_var, font=("Arial", 12), bg="#FFFFFF")
    email_entry.pack(anchor="w", padx=10)

    tk.Label(profile_frame, text="New Password:", font=("Arial", 14), bg="#FAF9F6").pack(anchor="w")
    new_password_var = tk.StringVar()
    new_password_entry = tk.Entry(profile_frame, textvariable=new_password_var, show="*", font=("Arial", 12), bg="#FFFFFF")
    new_password_entry.pack(anchor="w", padx=10)

    def save_changes():
        new_email = email_var.get()
        new_password = new_password_var.get()

        # Check if the new email is valid and if the password meets criteria
        if not new_email:
            messagebox.showerror("Error", "Email cannot be empty.")
            return
        if len(new_password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        # Update the user data in the database
        if update_user_in_database(new_email, new_password):
            messagebox.showinfo("Success", "Profile updated successfully!")
        else:
            messagebox.showerror("Error", "Failed to update profile.")

    save_btn = tk.Button(profile_frame, text="Save Changes", font=("Arial", 14), bg="#4CAF50", fg="white",
                         command=save_changes)
    save_btn.pack(pady=20)

# Function to create the main app
def create_main_app():
    global root
    root = tk.Tk()
    root.title("Book Store App")
    root.geometry("1200x800")
    root.configure(bg="#FAF9F6")

    # Sidebar
    sidebar = tk.Frame(root, bg="#FCE6C9", width=250)
    sidebar.pack(side="left", fill="y")

    # User Info
    user_img = Image.open("WhatsApp Image 2024-07-03 at 19.56.48_ae64950a.jpg").resize((50, 50))
    user_img_tk = ImageTk.PhotoImage(user_img)
    user_img_label = tk.Label(sidebar, image=user_img_tk, bg="#FCE6C9")
    user_img_label.pack(pady=20)

    tk.Label(sidebar, text="Ahmed Nabil", font=("Arial", 14, "bold"), bg="#FCE6C9").pack()
    logout_btn = tk.Button(sidebar, text="LOG OUT", font=("Arial", 10), bg="black", fg="white", relief="flat", command=log_out)
    logout_btn.pack(pady=10)

    # Sidebar Menu
    menu_items = [
        {"name": "Home", "icon": "icons/home.png"},
        {"name": "Categories", "icon": "icons/options-lines.png"},
        {"name": "Saved", "icon": "icons/bookmark.png"},
        {"name": "Recommendations", "icon": "icons/advice.png"},
        {"name": "Reviews", "icon": "icons/positive-review.png"},
        {"name": "Settings", "icon": "icons/settings.png"},
        {"name": "Profile", "icon": "icons/user.png"},
        {"name": "Cart", "icon": "grocery-store.png"},
    ]
    main_frame = tk.Frame(root, bg="#FAF9F6")
    main_frame.pack(side="right", fill="both", expand=True)

    for item in menu_items:
        icon = Image.open(item["icon"]).resize((20, 20))
        icon_tk = ImageTk.PhotoImage(icon)

        btn = tk.Button(
            sidebar,
            text=item["name"],
            image=icon_tk,
            compound="left",
            font=("Arial", 12),
            bg="#FCE6C9",
            anchor="w",
            relief="flat",
            padx=20,
            activebackground='#FCE6C9',
            command=lambda name=item["name"]: show_profile_page(main_frame) if name == "Profile" else None
        )
        btn.image = icon_tk  # Keep a reference to prevent garbage collection
        btn.pack(fill="x", pady=5)

    root.mainloop()

# Function to log out and return to registration screen
def log_out():
    root.destroy()  # Close the main app window
    create_registration_screen()  # Open the registration screen

# Function for Sign Up page
def open_sign_up():
    global sign_up_window
    sign_up_window = tk.Tk()
    sign_up_window.title("Sign Up")
    sign_up_window.configure(bg="#FAF9F6")

    tk.Label(sign_up_window, text="Sign Up", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

    tk.Label(sign_up_window, text="New Username", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
    new_username_entry = tk.Entry(sign_up_window, font=("Arial", 12), width=30)
    new_username_entry.pack(pady=5)

    tk.Label(sign_up_window, text="New Password", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
    new_password_entry = tk.Entry(sign_up_window, font=("Arial", 12), width=30, show="*")
    new_password_entry.pack(pady=5)

    tk.Label(sign_up_window, text="Email", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
    new_email_entry = tk.Entry(sign_up_window, font=("Arial", 12), width=30)
    new_email_entry.pack(pady=5)

    def handle_sign_up():
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()
        new_email = new_email_entry.get()

        if len(new_username) < 6:
            messagebox.showerror("Error", "Username must be at least 6 characters long.")
        elif len(new_password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
        elif user_exists(new_username):
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            insert_user(new_username, new_password, new_email)
            messagebox.showinfo("Success", "Registration successful!")
            sign_up_window.destroy()
            create_main_app()

    sign_up_btn = tk.Button(sign_up_window, text="Sign Up", font=("Arial", 12), bg="#2196F3", fg="white", width=20, command=handle_sign_up)
    sign_up_btn.pack(pady=20)

    center_window(sign_up_window, 400, 400)
    sign_up_window.mainloop()

# Function for Sign In page
def open_sign_in():
    global sign_in_window
    sign_in_window = tk.Tk()
    sign_in_window.title("Sign In")
    sign_in_window.configure(bg="#FAF9F6")

    tk.Label(sign_in_window, text="Sign In", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

    tk.Label(sign_in_window, text="Username", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
    user_username_entry = tk.Entry(sign_in_window, font=("Arial", 12), width=30)
    user_username_entry.pack(pady=5)

    tk.Label(sign_in_window, text="Password", font=("Arial", 12), bg="#FAF9F6").pack(pady=5)
    user_password_entry = tk.Entry(sign_in_window, font=("Arial", 12), width=30, show="*")
    user_password_entry.pack(pady=5)

    def handle_user_sign_in():
        username = user_username_entry.get()
        password = user_password_entry.get()

        if check_user_credentials(username, password):
            messagebox.showinfo("Success", "Sign In successful!")
            sign_in_window.destroy()
            create_main_app()
        else:
            messagebox.showerror("Error", "Invalid credentials. Try again.")

    sign_in_btn = tk.Button(sign_in_window, text="Sign In", font=("Arial", 12), bg="#FF5722", fg="white", width=20, command=handle_user_sign_in)
    sign_in_btn.pack(pady=20)

    center_window(sign_in_window, 400, 400)
    sign_in_window.mainloop()

# Main registration screen with options
def create_registration_screen():
    global reg_window
    reg_window = tk.Tk()
    reg_window.title("Book Store - Registration")
    reg_window.configure(bg="#FAF9F6")

    tk.Label(reg_window, text="Welcome To Our Book Store", font=("Arial", 18, "bold"), bg="#FAF9F6").pack(pady=20)

    sign_in_btn = tk.Button(reg_window, text="Sign In", font=("Arial", 12), bg="#4CAF50", fg="white", width=20, command=open_sign_in)
    sign_in_btn.pack(pady=20)

    sign_up_btn = tk.Button(reg_window, text="Sign Up", font=("Arial", 12), bg="#2196F3", fg="white", width=20, command=open_sign_up)
    sign_up_btn.pack(pady=20)

    center_window(reg_window, 400, 300)
    reg_window.mainloop()

# Call this function to create the database at the beginning
create_database()

if __name__ == "__main__":
    # Start the registration screen
    create_registration_screen()