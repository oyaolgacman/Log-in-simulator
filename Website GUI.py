import tkinter as tk

accounts = {}

def password_crit(password):
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one number")
    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one capital letter")
    if errors:
        return False, "\n".join(errors)
    else:
        return True, "Password is valid"

root = tk.Tk()
root.title("Oya's Website")
root.geometry("400x350")

label = tk.Label(root, text="Do you have an account?", wraplength=380, justify="left")
label.pack(pady=10)

# Yes/No buttons
v = tk.IntVar()
yes = tk.Radiobutton(root, text="Yes", variable=v, value=1)
yes.pack()
no = tk.Radiobutton(root, text="No", variable=v, value=2)
no.pack()
submit_btn = tk.Button(root, text="Submit")
submit_btn.pack(pady=10)

content_frame = tk.Frame(root)
content_frame.pack(pady=10)

# Log in
def show_login():
    for widget in content_frame.winfo_children():
        widget.destroy()
    label.config(text="Sign In")

    tk.Label(content_frame, text="Username").pack()
    username_entry = tk.Entry(content_frame)
    username_entry.pack()

    tk.Label(content_frame, text="Password").pack()
    password_entry = tk.Entry(content_frame, show="*")
    password_entry.pack()

    show_var = tk.IntVar()
    def toggle_password():
        if show_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")
    tk.Checkbutton(content_frame, text="Show Password", variable=show_var, command=toggle_password).pack()

    def login():
        u = username_entry.get()
        p = password_entry.get()

        if u in accounts and accounts[u] == p:
            label.config(text=f"Welcome {u}!")
            return

        # Login fail
        label.config(text="Invalid username or password")

        # Go to create an account
        if u not in accounts:
            goto_signup_btn = tk.Button(content_frame, text="Create an account.", command=show_signup)
            goto_signup_btn.pack(pady=5)

    tk.Button(content_frame, text="Login", command=login).pack(pady=5)

# Sign up
def show_signup():
    for widget in content_frame.winfo_children():
        widget.destroy()
    label.config(text="Create an Account")

    tk.Label(content_frame, text="Username").pack()
    username_entry = tk.Entry(content_frame)
    username_entry.pack()

    tk.Label(content_frame, text="Password").pack()
    password_entry = tk.Entry(content_frame, show="*")
    password_entry.pack()

    tk.Label(content_frame, text="Confirm Password").pack()
    confirm_entry = tk.Entry(content_frame, show="*")
    confirm_entry.pack()

    show_var = tk.IntVar()
    def toggle_password():
        if show_var.get():
            password_entry.config(show="")
            confirm_entry.config(show="")
        else:
            password_entry.config(show="*")
            confirm_entry.config(show="*")
    tk.Checkbutton(content_frame, text="Show Password", variable=show_var, command=toggle_password).pack()

    def create_account():
        u = username_entry.get()
        p = password_entry.get()
        p_confirm = confirm_entry.get()

        valid, msg = password_crit(p)
        if p != p_confirm:
            valid = False
            if msg:
                msg += "\nPasswords do not match"
            else:
                msg = "Passwords do not match"

        if not valid:
            label.config(text=msg)
            return

        accounts[u] = p
        label.config(text="Account created! Redirecting to login...")
        show_login()

    tk.Button(content_frame, text="Create Account", command=create_account).pack(pady=5)

# Yes or No
def submit_choice():
    choice = v.get()
    if choice == 0:
        label.config(text="Please choose Yes or No")
        return
    yes.destroy()
    no.destroy()
    submit_btn.destroy()
    if choice == 1:
        show_login()
    else:
        show_signup()

submit_btn.config(command=submit_choice)

root.mainloop()
