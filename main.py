from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import string
import pyperclip
import json


def search_website():
    website_name = website_entry.get().title()
    try:
        with open('website_info.json') as file:
            data = json.load(file)
            website = data[website_name]
    except (KeyError, FileNotFoundError):
        messagebox.showerror(message=f"Website not found")
    else:
        message = f"Email/Username: {website['Email/Username']}\n\nPassword: {website['Password']}"
        messagebox.showinfo(title=f'{website_name} info', message=message)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_random_password():
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_entry.delete(0, END)

    password_list = [choice(string.ascii_letters) for _ in range(randint(9, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 5))]
    password_list += [str(randint(0,9)) for _ in range(randint(3, 5))]

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """If all entires are filled out then save info to a txt file, otherwise alert the user"""
    website = website_entry.get().title()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "Email/Username": username,
            "Password": password,
        }
    }
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title='Error', message="Some fields are empty")
        return

    confirmation = f"These are the details entered:\n\n{website}\n{username}\n{password}\n\nIs it okay to save?"
    if not messagebox.askokcancel(title=website, message=confirmation):
        return

    try:
        with open('website_info.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        with open('website_info.json', 'w') as file:
            json.dump(new_data, file, indent=4)
    else:
        data.update(new_data)
        with open('website_info.json', 'w') as file:
            json.dump(data, file, indent=4)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        messagebox.showinfo(title='Success', message="Information successfully saved")

# ---------------------------- UI SETUP ------------------------------- #

#Window

window = Tk()
window.title("Password-Manager")
window.configure(padx=50, pady=50)

#Canvas

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#Labels

website_label = Label(text="Website:", padx=30)
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#Entries

website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()
username_entry = Entry(width=52)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(END, string="user_email")
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

#Buttons

generate_button = Button(text="Generate Password", width=15, command=generate_random_password)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=15, command=search_website)
search_button.grid(column=2, row=1)

#MessageBox

window.mainloop()