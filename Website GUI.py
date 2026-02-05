import tkinter as tk
from tkinter import ttk

accounts = {}

THEMES = {
    "dark": {"bg": "#1E1E1E", "text": "#ff5858", "button": "#2A2A2A", "button_text": "#ff5858", "entry_bg": "#2E2E2E", "entry_text": "#ff5858"},
    "light": {"bg": "#F4F4F4", "text": "#000000", "button": "#DCDCDC", "button_text": "#000000", "entry_bg": "#FFFFFF", "entry_text": "#000000"},
    "greenpink": {"bg": "#b3ecec", "text": "#0086ad", "button": "#ff93ac", "button_text": "#FFFFFF", "entry_bg": "#89ecda", "entry_text": "#fc3468"},
    "yellpurple": {"bg": "#fffb96", "text": "#b967ff", "button": "#ff71ce", "button_text": "#ffffff", "entry_bg": "#b967ff", "entry_text": "#05ffa1"},
    "deepsunset": {"bg": "#0057e7", "text": "#ff00c1", "button": "#ff4d00", "button_text": "#ffffff", "entry_bg": "#ffffff", "entry_text": "#ff4d00"}
}

COLORS = {"error": "#FF3B3B", "success": "#2ECC71", "warning": "#F1C40F", "info": "#3498DB"}

current_theme = THEMES["dark"]

root = tk.Tk()
root.title("Oya's Website")
root.geometry("600x600")
root.minsize(500, 300)
root.resizable(True, True)
root.config(bg=current_theme["bg"])

style = ttk.Style()
style.theme_use("default")
style.configure("TButton", borderwidth=0, relief="flat",
                background=current_theme["button"],
                foreground=current_theme["button_text"])

# Theme selection
theme_var = tk.StringVar(value="dark")
def change_theme():
    global current_theme
    current_theme = THEMES[theme_var.get()]
    root.config(bg=current_theme["bg"])
    style.configure("TButton", background=current_theme["button"], foreground=current_theme["button_text"])
    apply_theme(root)

theme_frame = tk.Frame(root, bg=current_theme["bg"])
theme_frame.pack(pady=5)
tk.Label(theme_frame, text="Theme:", bg=current_theme["bg"], fg=current_theme["text"]).pack(side="left")
for t in THEMES:
    tk.Radiobutton(theme_frame, text=t.capitalize(), variable=theme_var, value=t,
                   command=change_theme, bg=current_theme["bg"], fg=current_theme["text"]).pack(side="left", padx=3)

# Main UI
label = tk.Label(root, text="Do you have an account?", wraplength=380, fg=current_theme["text"], bg=current_theme["bg"])
label.pack(pady=10)

message_label = tk.Label(root, text="", wraplength=380, fg=COLORS["error"], bg=current_theme["bg"])
message_label.pack(pady=10)

v = tk.IntVar()
yes = tk.Radiobutton(root, text="Yes", variable=v, value=1, fg=current_theme["text"], bg=current_theme["bg"])
yes.pack()
no = tk.Radiobutton(root, text="No", variable=v, value=2, fg=current_theme["text"], bg=current_theme["bg"])
no.pack()
submit_btn = ttk.Button(root, text="Submit")
submit_btn.pack(pady=10)

content_frame = tk.Frame(root, bg=current_theme["bg"])
content_frame.pack(pady=10)

def apply_theme(widget):
    for child in widget.winfo_children():
        if isinstance(child, tk.Label):
            child.config(bg=current_theme["bg"], fg=current_theme["text"])
        elif isinstance(child, tk.Entry):
            child.config(bg=current_theme["entry_bg"], fg=current_theme["entry_text"], insertbackground=current_theme["entry_text"])
        elif isinstance(child, tk.Frame):
            child.config(bg=current_theme["bg"])
            apply_theme(child)
        elif isinstance(child, ttk.Button):
            style.configure("TButton", background=current_theme["button"], foreground=current_theme["button_text"])
        elif isinstance(child, (tk.Checkbutton, tk.Radiobutton)):
            child.config(bg=current_theme["bg"], fg=current_theme["text"])

def show_message(text, color_key="error"):
    message_label.config(text=text, fg=COLORS[color_key])

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
    return True, "Password is valid"

# Log in
def show_login():
    for widget in content_frame.winfo_children():
        widget.destroy()
    label.config(text="Sign In")
    show_message("")

    tk.Label(content_frame, text="Username", fg=current_theme["text"], bg=current_theme["bg"]).pack()
    username_entry = tk.Entry(content_frame, bg=current_theme["entry_bg"], fg=current_theme["entry_text"], insertbackground=current_theme["entry_text"])
    username_entry.pack()

    tk.Label(content_frame, text="Password", fg=current_theme["text"], bg=current_theme["bg"]).pack()
    password_entry = tk.Entry(content_frame, show="*", bg=current_theme["entry_bg"], fg=current_theme["entry_text"], insertbackground=current_theme["entry_text"])
    password_entry.pack()

    show_var = tk.IntVar()
    def toggle_password(): password_entry.config(show="" if show_var.get() else "*")
    tk.Checkbutton(content_frame, text="Show Password", variable=show_var, command=toggle_password, fg=current_theme["text"], bg=current_theme["bg"]).pack()

    def login():
        u = username_entry.get()
        p = password_entry.get()

        if u in accounts and accounts[u] == p:
            for widget in content_frame.winfo_children():
                widget.destroy()
            label.config(text=f"Welcome {u}!", fg=COLORS["success"])
            show_message("Login successful", "success")
            return

        show_message("Invalid username or password", "error")

        if u not in accounts:
            if hasattr(login, "signup_btn"): login.signup_btn.destroy()
            login.signup_btn = ttk.Button(content_frame, text="Create an account", command=show_signup)
            login.signup_btn.pack(pady=5)
            apply_theme(content_frame)

    ttk.Button(content_frame, text="Login", command=login).pack(pady=5)
    apply_theme(content_frame)

# Sign up
def show_signup():
    for widget in content_frame.winfo_children():
        widget.destroy()
    label.config(text="Create an Account")
    show_message("")

    tk.Label(content_frame, text="Username", fg=current_theme["text"], bg=current_theme["bg"]).pack()
    username_entry = tk.Entry(content_frame, bg=current_theme["entry_bg"], fg=current_theme["entry_text"], insertbackground=current_theme["entry_text"])
    username_entry.pack()

    tk.Label(content_frame, text="Password", fg=current_theme["text"], bg=current_theme["bg"]).pack()
    password_entry = tk.Entry(content_frame, show="*", bg=current_theme["entry_bg"], fg=current_theme["entry_text"], insertbackground=current_theme["entry_text"])
    password_entry.pack()

    tk.Label(content_frame, text="Confirm Password", fg=current_theme["text"], bg=current_theme["bg"]).pack()
    confirm_entry = tk.Entry(content_frame, show="*", bg=current_theme["entry_bg"], fg=current_theme["entry_text"], insertbackground=current_theme["entry_text"])
    confirm_entry.pack()

    show_var = tk.IntVar()
    def toggle_password():
        state = "" if show_var.get() else "*"
        password_entry.config(show=state)
        confirm_entry.config(show=state)
    tk.Checkbutton(content_frame, text="Show Password", variable=show_var, command=toggle_password, fg=current_theme["text"], bg=current_theme["bg"]).pack()

    def create_account():
        u = username_entry.get()
        p = password_entry.get()
        p_confirm = confirm_entry.get()

        if u in accounts:
            show_message("Username already exists", "warning")
            return

        valid, msg = password_crit(p)
        if p != p_confirm:
            valid = False
            msg += "\nPasswords do not match"

        if not valid:
            show_message(msg, "error")
            return

        accounts[u] = p
        show_message("Account created successfully!", "success")

        # Clear signup widgets before redirecting to login
        for widget in content_frame.winfo_children():
            widget.destroy()
        show_login()

    ttk.Button(content_frame, text="Create Account", command=create_account).pack(pady=5)
    apply_theme(content_frame)

# Yes or No
def submit_choice():
    choice = v.get()
    if choice == 0:
        show_message("Please choose Yes or No", "warning")
        return
    yes.destroy()
    no.destroy()
    submit_btn.destroy()
    if choice == 1:
        show_login()
    else:
        show_signup()

submit_btn.config(command=submit_choice)
apply_theme(root)
root.mainloop()