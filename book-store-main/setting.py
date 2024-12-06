import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the SQLite database


# Function to fetch user data for validation
def get_user_data():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, email, password FROM settings WHERE id = 1")  # Assuming user ID is 1
    conn.close
    return cursor.fetchone()

# Function to update the user in the database
def update_user_in_database(new_first_name, new_last_name, new_password):
    try:
        cursor.execute("UPDATE settings SET first_name = ?, last_name = ?, password = ? WHERE id = ?", 
                       (new_first_name, new_last_name, new_password, 1)) 
        conn.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Function to show user data in a new window
def show_user_data():
    user_data_window = tk.Toplevel(root)
    user_data_window.title("User Data")
    user_data_window.geometry("400x300")
    
    cursor.execute("SELECT * FROM settings WHERE id = 1")
    rows = cursor.fetchall()

    if rows:
        for index, row in enumerate(rows):
            tk.Label(user_data_window, text=row).pack(anchor="w", padx=10, pady=5)
    else:
        tk.Label(user_data_window, text="No user data found.").pack(pady=20)

# Function to show payment methods
def show_payment_methods():
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment Methods")
    payment_window.geometry("400x300")

    cursor.execute("SELECT * FROM payment_methods")
    methods = cursor.fetchall()

    if methods:
        for method in methods:
            tk.Label(payment_window, text=method[1]).pack(anchor="w", padx=10, pady=5)
    else:
        tk.Label(payment_window, text="No payment methods found.").pack(pady=20)

# Function to clear the current frame and show a new one
def show_page(page_function, main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()
    page_function(main_frame)

# Function to show the settings page
def show_settings_page(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    settings_frame = tk.Frame(main_frame, bg="#FAF9F6")
    settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(settings_frame, text="Settings", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))

    tk.Label(settings_frame, text="Account Settings", font=("Arial", 18, "bold"), bg="#FAF9F6", fg="#4CAF50").pack(anchor="w", pady=(10, 5))
    tk.Button(settings_frame, text="Update Username/Password", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=lambda: show_page(show_update_account_page, main_frame)).pack(fill="x", padx=10, pady=5)
    tk.Button(settings_frame, text="Manage Payment Methods", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=lambda: show_page(show_payment_methods_page, main_frame)).pack(fill="x", padx=10, pady=5)

    tk.Button(settings_frame, text="View User Data", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=show_user_data).pack(fill="x", padx=10, pady=5)

    # Preferences Section
    tk.Label(settings_frame, text="Preferences", font=("Arial", 18, "bold"), bg="#FAF9F6", fg="#4CAF50").pack(anchor="w", pady=(20, 5))
    
    genres = ["Fiction", "Non-Fiction", "Mystery", "Science Fiction", "Fantasy"]
    selected_genre = tk.StringVar(value="Fiction")

    tk.Label(settings_frame, text="Preferred Genre:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    genre_menu = tk.OptionMenu(settings_frame, selected_genre, *genres)
    genre_menu.config(font=("Arial", 12), bg="#FAF9F6", fg="#333")
    genre_menu.pack(anchor="w", padx=10, pady=(0, 10))

    tk.Label(settings_frame, text="Preferred Currency:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    currency_var = tk.StringVar(value="USD")
    tk.Entry(settings_frame, textvariable=currency_var, font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    # Notifications Toggle
    notifications_var = tk.BooleanVar(value=True)
    tk.Checkbutton(settings_frame, text="Enable Email Notifications", variable=notifications_var, font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=10)

    # Display Options
    tk.Label(settings_frame, text="Display Options", font=("Arial", 18, "bold"), bg="#FAF9F6", fg="#4CAF50").pack(anchor="w", pady=(20, 5))
    font_size_var = tk.IntVar(value=12)
    tk.Label(settings_frame, text="Font Size:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    tk.Scale(settings_frame, from_=8, to=24, orient="horizontal", variable=font_size_var, bg="#FAF9F6").pack(anchor="w", pady=(0, 10))

    # Save Settings Button
    def save_settings():
        preferences = {
            "genre": selected_genre.get(),
            "currency": currency_var.get(),
            "notifications": notifications_var.get(),
            "font_size": font_size_var.get(),
        }
        messagebox.showinfo("Settings Saved", f"Your preferences have been updated:\n{preferences}")

    tk.Button(settings_frame, text="Save Settings", font=("Arial", 14), bg="#4CAF50", fg="white", command=save_settings).pack(pady=(20, 10), fill="x", padx=10)

# Function to show the Update Username/Password page
def show_update_account_page(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    update_frame = tk.Frame(main_frame, bg="#FAF9F6")
    update_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(update_frame, text="Update Username/Password", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))

    tk.Label(update_frame, text="Old Username:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    old_username_var = tk.StringVar()
    tk.Entry(update_frame, textvariable=old_username_var, font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Label(update_frame, text="Old Password:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    old_password_var = tk.StringVar()
    tk.Entry(update_frame, textvariable=old_password_var, show='*', font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Label(update_frame, text="New Username:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    new_username_var = tk.StringVar()
    tk.Entry(update_frame, textvariable=new_username_var, font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Label(update_frame, text="New Password:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    new_password_var = tk.StringVar()
    tk.Entry(update_frame, textvariable=new_password_var, show='*', font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Button(update_frame, text="Save Changes", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=lambda: save_account_changes(old_username_var.get(), old_password_var.get(), new_username_var.get(), new_password_var.get())).pack(pady=(20, 10), fill="x", padx=10)

    tk.Button(update_frame, text="Back", font=("Arial", 14), bg="#FF5722", fg="white",
              command=lambda: show_page(show_settings_page, main_frame)).pack(pady=4, fill="x", padx=10)

def save_account_changes(old_username, old_password, new_username, new_password):
    current_user = get_user_data()
    current_first_name = current_user[0] if current_user else None
    current_last_name = current_user[1] if current_user else None
    current_password = current_user[3] if current_user else None

    if not old_username or not old_password or not new_username or not new_password:
        messagebox.showerror("Error", "All fields must be filled.")
        return

    if old_username != f"{current_first_name} {current_last_name}" or old_password != current_password:  
        messagebox.showerror("Error", "Old username or password is incorrect.")
        return

    new_username_parts = new_username.split()
    if len(new_username_parts) < 2:
        messagebox.showerror("Error", "Please enter both first and last names.")
        return

    new_first_name, new_last_name = new_username_parts[0], " ".join(new_username_parts[1:])

    if update_user_in_database(new_first_name, new_last_name, new_password):
        messagebox.showinfo("Account Updated", "Username and Password updated successfully!")
    else:
        messagebox.showerror("Error", "Failed to update account. Try again.")

# Function to show the Manage Payment Methods page
def show_payment_methods_page(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    payment_frame = tk.Frame(main_frame, bg="#FAF9F6")
    payment_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(payment_frame, text="Manage Payment Methods", font=("Arial", 24, "bold"), bg="#FAF9F6", fg="#333").pack(pady=(10, 20))

    tk.Label(payment_frame, text="Add Payment Method:", font=("Arial", 14), bg="#FAF9F6", fg="#333").pack(anchor="w", pady=(5, 5))
    payment_method_var = tk.StringVar()
    tk.Entry(payment_frame, textvariable=payment_method_var, font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=10, pady=(0, 10))

    tk.Button(payment_frame, text="Add Payment Method", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=lambda: add_payment_method(payment_method_var.get())).pack(pady=(10, 10), fill="x", padx=10)

    tk.Button(payment_frame, text="View Payment Methods", font=("Arial", 14), bg="#4CAF50", fg="white",
              command=show_payment_methods).pack(pady=(10, 10), fill="x", padx=10)

    tk.Button(payment_frame, text="Back", font=("Arial", 14), bg="#FF5722", fg="white",
              command=lambda: show_page(show_settings_page, main_frame)).pack(pady=4, fill="x", padx=10)

def add_payment_method(payment_method):
    if payment_method:
        cursor.execute("INSERT INTO payment_methods (method) VALUES (?)", (payment_method,))
        conn.commit()
        messagebox.showinfo("Payment Method Added", f"Payment Method: {payment_method} added successfully!")
    else:
        messagebox.showerror("Error", "Payment Method cannot be empty.")

# Main function to start the application
def main():
    show_page(show_settings_page, root)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Book Store Application")
    root.geometry("800x600")
    main() 
    root.mainloop()

# Close the database connection when the application closes
conn.close()