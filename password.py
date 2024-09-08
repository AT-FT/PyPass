import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# Generate and store the key securely
key = Fernet.generate_key()
cipher_suite = Fernet(key)

#Creaating Database Password_Manager
def create_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='enter_your_username_here',
            password='enter_your_password_here'
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS password_manager")
        print("Database created successfully")
        connection.close()
    except Error as e:
        print(f"Error: {e}")

#Establishing Connection with MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='password_manager',
            user='enter_your_username_here',
            password='enter_your_password_here'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

#Adding New Password to the Database:
def add_password(connection, account_name, username, password):
    try:
        encrypted_password = cipher_suite.encrypt(password.encode())
        cursor = connection.cursor()
        query = "INSERT INTO passwords (account_name, username, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (account_name, username, encrypted_password))
        connection.commit()
        messagebox.showinfo("Success", "Password added successfully")
    except Error as e:
        messagebox.showerror("Error", f"Error: {e}")

#View All Passwords Stored in the Database
def view_passwords(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM passwords"
        cursor.execute(query)
        rows = cursor.fetchall()
        decrypted_rows = [(row[0], row[1], row[2], cipher_suite.decrypt(row[3]).decode()) for row in rows]
        return decrypted_rows
    except Error as e:
        messagebox.showerror("Error", f"Error: {e}")
        return []

#Deleting Passwords from the Database
def delete_password(connection, password_id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM passwords WHERE id = %s"
        cursor.execute(query, (password_id,))
        connection.commit()
        messagebox.showinfo("Success", "Password deleted successfully")
    except Error as e:
        messagebox.showerror("Error", f"Error: {e}")

#UI of AddPassword using TKinter
def add_password_ui():
    account_name = account_name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    add_password(connection, account_name, username, password)
    account_name_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

#UI of ViewPasswords using TKinter
def view_passwords_ui():
    passwords_listbox.delete(0, tk.END)
    rows = view_passwords(connection)
    for row in rows:
        passwords_listbox.insert(tk.END, f"ID: {row[0]}, Account: {row[1]}, Username: {row[2]}, Password: {row[3]}")

#UI for DeletePassword using TKinter
def delete_password_ui():
    password_id = delete_id_entry.get()
    delete_password(connection, password_id)
    delete_id_entry.delete(0, tk.END)

#Main TKinter Window
root = tk.Tk()
root.title("Password Manager")

#Basic Layout
tk.Label(root, text="Account Name").grid(row=0, column=0)
account_name_entry = tk.Entry(root)
account_name_entry.grid(row=0, column=1)

tk.Label(root, text="Username").grid(row=1, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1)

tk.Label(root, text="Password").grid(row=2, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1)

add_button = tk.Button(root, text="Add Password", command=add_password_ui)
add_button.grid(row=3, column=0, columnspan=2)

view_button = tk.Button(root, text="View Passwords", command=view_passwords_ui)
view_button.grid(row=4, column=0, columnspan=2)

passwords_listbox = tk.Listbox(root, width=50)
passwords_listbox.grid(row=5, column=0, columnspan=2)

tk.Label(root, text="Password ID to Delete").grid(row=6, column=0)
delete_id_entry = tk.Entry(root)
delete_id_entry.grid(row=6, column=1)

delete_button = tk.Button(root, text="Delete Password", command=delete_password_ui)
delete_button.grid(row=7, column=0, columnspan=2)

#Creating Database
create_database()

#Connecting with database
connection = create_connection()

#Main Loop
root.mainloop()
