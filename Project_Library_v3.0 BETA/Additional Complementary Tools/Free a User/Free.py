#Free User of Charge or debt
import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
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

def free_user():
    user_id = id_entry.get()
    username = username_entry.get()

    if str(user_id) == "" and str(username) == "" :
        messagebox.showerror("Empty Fields!", "Please fill at least one of the fields!")
        return

    if str(user_id) != "":
        try:
            user_id = int(user_id)
        except ValueError:
            messagebox.showerror("Invalid Value", "User ID must be a Number!")
            return
        
    if str(user_id) != "" or str(username) != "":
        free_user_confirmation = messagebox.askyesno("Confirmation Message", "You're attempting to free a user of charge.\n\nAnd that their fees would reach to '0' if you do this!\nDo it ONLY if you know what you're actually doing & all at your own risk!\n\n--PROCEED?--")
        if free_user_confirmation:
            pass
        else:
            return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    if user_id:
        cursor.execute("UPDATE users SET days_remaining = 'user_exempt', borrowed_ids = NULL WHERE ID = ?", (user_id,))
    elif username:
        cursor.execute("UPDATE users SET days_remaining = 'user_exempt', borrowed_ids = NULL WHERE username = ?", (username,))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "User Successfully Redeemed of any Charge!")

    user_id = str(user_id)
    username = str(username)
    try:
        user_id = int(user_id)
    except (ValueError , TypeError):
        pass

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

    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""CREATE TABLE IF NOT EXISTS user_charge_redemption (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note TEXT,
                    username TEXT,
                    user_id TEXT,
                    event_by_admin TEXT,
                    sub_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()

    if username == "":
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        if user is None:
            user = str(user)
        else:
            for username in user:
                username = str(username)
        conn.close()
        tup = ("Admin User-Free Attempt", f"@ {username}", user_id, event_by_admin, the_user, datetime.datetime.now())

    elif user_id == "":
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        iden = cursor.fetchone()
        if iden is None:
            iden = str(iden)
        else:
            for user_id in iden:
                user_id = str(user_id)
        conn.close()
        tup = ("Admin User-Free Attempt", username, f"# {user_id}", event_by_admin, the_user, datetime.datetime.now())

    cursor1.execute("INSERT INTO user_charge_redemption (note, username, user_id, event_by_admin, sub_admin, event_date) VALUES (?, ?, ?, ?, ?, ?)", tup)
    conn1.commit()
    conn1.close()

def exit_the_program():
    window.destroy()

window = tk.Tk()
window.title("Free User")
window.geometry("1000x376")
window.configure(bg="darkblue")
window.resizable(False,False)

label_text = "Please enter a Username or an ID of the user you want to Free. Use this only if you need to free a user of Charge:\n"
label = tk.Label(window, text=label_text, font="tahoma 14 italic", bg="brown", fg="yellow")
label.pack(pady=20)

id_label = tk.Label(window, text="ID:", font="arial 14 bold", bg="darkblue", fg="yellow")
id_label.pack()

id_entry = tk.Entry(window, font="Helvetica 14 italic", justify="center", width=60, fg="red")
id_entry.pack(pady=10)

username_label = tk.Label(window, text="Username:", font="arial 14 bold", bg="darkblue", fg="yellow")
username_label.pack()

username_entry = tk.Entry(window, font="Helvetica 14 italic", justify="center", width=80, fg="red")
username_entry.pack(pady=10)

free_button = tk.Button(window, text="Free!", font=("bold",16), command=free_user, bg="#00ff00")
free_button.pack(pady=15)

exit_button = tk.Button(window, text="Quit!", bg="red", fg="darkblue", font=("impact", 14, "bold"), command = exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack()

window.mainloop()