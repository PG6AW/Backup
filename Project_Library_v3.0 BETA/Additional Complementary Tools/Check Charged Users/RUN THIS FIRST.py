#Update The Database

import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
from datetime import datetime
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

def convert_to_days(date):
    year, month, day = date.split(' ')[0].split('-')
    days = (int(year) * 365) + (int(month) * 30) + int(day)
    return days

def update_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, date_borrowed, days_remaining FROM users")
    rows = cursor.fetchall()

    for row in rows:
        Id = row[0]
        date_borrowed = row[1]
        days_remaining = row[2]

        if date_borrowed is None:
            continue

        day_borrowed = convert_to_days(date_borrowed)

        if days_remaining != "user_exempt":
            borrowed_days = int(days_remaining)
            return_day = borrowed_days + day_borrowed
            current_day = convert_to_days(datetime.now().strftime("%Y-%m-%d"))

            # days_margin = return_day - current_day
            # days_margin = str(days_margin)

            # if days_remaining != "user_exempt":
            #     cursor.execute("UPDATE users SET days_remaining = ? WHERE date_borrowed = ?", (days_margin, date_borrowed))
            #     cursor.execute("UPDATE users SET date_borrowed = ? WHERE id = ?", (datetime.now(), Id))

            if int(current_day) > int(day_borrowed) or int(current_day) < int(day_borrowed): #To avoid making insignificant changes to the database over time (for more accurate timestamping against what we have just commented above this method)
                days_margin = return_day - current_day #The commented part above also updates the time remaining till the breakpoint set predefined.
                days_margin = str(days_margin)

                if days_remaining != "user_exempt":
                    cursor.execute("UPDATE users SET days_remaining = ? WHERE date_borrowed = ?", (days_margin, date_borrowed))
                    cursor.execute("UPDATE users SET date_borrowed = ? WHERE id = ?", (datetime.now(), Id))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success-Update Notice", "Database's timezone has been / had been(already) successfully updated to the current Time & Date of your system!")

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
    cursor1.execute("""CREATE TABLE IF NOT EXISTS time_zone_update (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    button_fired TEXT,
                    event_by_admin TEXT,
                    sub_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()

    cursor1.execute("INSERT INTO time_zone_update (button_fired, event_by_admin, sub_admin, event_date) VALUES (?, ?, ?, ?)",
                ("CLICKED/FIRED by Admin", event_by_admin, the_user, datetime.now()))
    conn1.commit()
    conn1.close()

def exit_the_program():
    window.destroy()

window = tk.Tk()
window.title("Update Database Timing")
window.geometry("650x210")
window.configure(bg="lightgreen")
window.resizable(False,False)

button = tk.Button(window, text="Click this button to UPDATE Time & Date of the Database", bg="#00ff00", relief="ridge", fg="black", font=("Arial", 14, "bold"), command=update_database)
button.configure(width=45, height=4)
button.pack(pady=20)

exit_button = tk.Button(window, text="Exit", bg="red", relief="ridge", fg="darkblue", font=("impact", 10, "bold"), command = exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack()

window.mainloop()