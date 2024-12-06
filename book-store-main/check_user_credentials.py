import sqlite3


def check_user_credentials(username, password):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()

        # Query to find user by username and password
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()  # Fetch the first result

        conn.close()

        if user:
            return user[0]  # User found and credentials are correct
        else:
            return None  # Invalid credentials
    except Exception as e:
        print(f"Error checking user credentials: {e}")
        return None



def check_admin_credentials(username,password,admin_key):
    try:
        conn = sqlite3.connect('user_data.db')
        cursor= conn.cursor()
        cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ? AND admin_key = ?', (username, password,admin_key))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            return admin[0]
        else:
            return None
    except Exception as e:
        print(f"Error checking admin credentials: {e}")
        return None
