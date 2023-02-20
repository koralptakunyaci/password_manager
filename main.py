from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
    }}

    if website == "" or password == "" or email == "":
        messagebox.showwarning(title="Warning", message="You must fill the blanks to save your data!")
    else:
        # is_ok = messagebox.askokcancel(title=website, message=f"Your Email is {email}\nYour password is {password}\n"
        #                                                       f"Do you want to save?")
        # if is_ok:
        try:
            with open("data.json", "r") as data_file:
                # data_file.write(f"{website} | {email} | {password}\n")
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# --------------------------- FIND PASSWORD --------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=f"{website}", message=f"Your Email is {email}.\n"
                                                            f"Your Password is {password}")
        elif website == "":
            messagebox.showinfo(title="Error", message=f"You must enter a website to see your data.")
        else:
            messagebox.showinfo(title="Error", message=f"No data for {website} exist.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")

window.config(pady=50, padx=50)

# Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(130, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
label_website = Label(text="Website:")
label_website.grid(row=1, column=0, pady=2)

label_email = Label(text="Email/Username:")
label_email.grid(row=2, column=0, pady=2)

label_password = Label(text="Password:")
label_password.grid(row=3, column=0, pady=2)

# Entries
website_entry = Entry(width=32)
website_entry.grid(row=1, column=1, columnspan=2, sticky="W", pady=2)
website_entry.focus()
email_entry = Entry(width=51)
email_entry.grid(row=2, column=1, columnspan=2, sticky="W", pady=2)
email_entry.insert(0, "alp@email.com")

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1, sticky="W", pady=2)

# Button

generate_button = Button(text="Generate Password", command=password_generator)
generate_button.grid(row=3, column=2, pady=2)
add_button = Button(text="Add", width=43, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="W", pady=2)
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
