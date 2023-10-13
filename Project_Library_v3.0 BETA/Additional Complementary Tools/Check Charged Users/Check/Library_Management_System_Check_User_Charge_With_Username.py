#Check User's debt
import tkinter as tk
from tkinter import messagebox
import sqlite3
import getpass
import subprocess


current_username = getpass.getuser()
event_by_admin = current_username
the_user = "*N-U-L-L*"
try:
    conn2 = sqlite3.connect("accounts.db")
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT id FROM login_logs WHERE event_by_admin=?", (event_by_admin,))
    Ids = cursor2.fetchall()
    if Ids is None:
        Ids = str(Ids)
    ids = max(Ids)
    for Id in ids:
        Id = int(Id)
    cursor2.execute("SELECT username FROM login_logs WHERE id=?", (Id,))
    user_name = cursor2.fetchone()
    if user_name is None:
        user_name = str(user_name)
    else:
        for the_user in user_name:
            the_user = str(the_user)
    conn2.close()
except (sqlite3.OperationalError , ValueError , sqlite3.ProgrammingError):
    pass

if the_user == "LOGGED->OUT" or the_user == "*N-U-L-L*":
    retry = True
    while retry:
        retry = messagebox.askretrycancel("LOGGED OUT!", "You are currently Logged Out!\n\nYOU'D BE BETTER OFF CANCELLING THIS & LOG-IN FIRST BEFORE YOU COME BACK & RETRY!")
    subprocess.Popen(['python', 'login.py'])
    exit()
else:
    pass

def check_charge():
    username = entry_username.get()

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT days_remaining FROM users WHERE username = ?", (username,)) #Checking user by their username
    result = c.fetchone()

    if str(username) == "":
        messagebox.showerror("Error", "Field is empty! Please submit a Username first.")
        return

    if result:
        days_remaining = result[0]

        if days_remaining == 'user_exempt' or (days_remaining is not None and int(days_remaining) > 0):
            messagebox.showinfo("Charge Status", "User is free of charge by now")
        else:
            if days_remaining is not None:
                charge_amount = abs(int(days_remaining)) * 5
                messagebox.showinfo("Charge Status", f"User has been charged ${charge_amount}")
            else:
                messagebox.showinfo("Error", "This user has not borrowed any book!")
    else:
        messagebox.showinfo("Error", "User not found")

    conn.close()

def list_charged_users():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT username, borrowed_ids FROM users WHERE days_remaining <= 0")
    charged_users = c.fetchall()

    if charged_users:
        messagebox.showinfo("Charged Users", "The following users have outstanding charges:")

        for user in charged_users:
            username, borrowed_ids = user
            messagebox.showinfo("Charged User", f"Username: {username}\nBorrowed IDs: {borrowed_ids}\n")

    else:
        messagebox.showinfo("Charged Users", "No users have outstanding charges.")

    conn.close()

def exit_the_program():
    window.destroy()

window = tk.Tk()
window.resizable(False,False)
window.title("Library Management System")
window.geometry("600x600")
window.configure(bg="#011042")

blank_frame = tk.Frame(window, bg="#011042", height=30)
blank_frame.pack()

username_label = tk.Label(window, bg="#011042", fg="#00ff00", text="Type person's username in the field down below:", font="arial 14 bold")
username_label.pack(pady=3)

entry_username = tk.Entry(window, font=("arial 17 bold"))
entry_username.configure(width=35, bg="#252525", relief="sunken", fg="#00ff00", justify="center")
entry_username.pack(pady=25)

submit_button = tk.Button(window, text="Check Charge of User", command=check_charge, font=("arial 14 bold"), bg="#00ff00")
submit_button.configure(height=3, width=42)
submit_button.pack(pady=5)

blank_frame1 = tk.Frame(window, bg="#011042", height=50)
blank_frame1.pack()
label_dash = tk.Label(window, bg="#011042", fg="blue", width=100, font="arial 20", text="--------------- OR ---------------")
label_dash.place(relx=0.5, rely=0.45, anchor=tk.N)
blank_frame1 = tk.Frame(window, bg="#011042", height=50)
blank_frame1.pack()

list_button = tk.Button(window, text="List Charged Users", command=list_charged_users, font=("arial 17 bold"), bg="yellow")
list_button.configure(height=4, width=32)
list_button.pack(pady=5)

exit_button = tk.Button(window, text="Exit", bg="red", fg="darkblue", font=("impact", 10, "bold"), command = exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack(pady=40)

window.mainloop()
