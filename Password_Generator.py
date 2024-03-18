import tkinter as tk
import random
import string
import pyperclip

def generate_password(length, complexity, exclude_chars):
    characters = ''
    if complexity == "Weak":
        characters = string.ascii_lowercase
    elif complexity == "Normal":
        characters = string.ascii_letters + string.digits
    elif complexity == "Strong":
        characters = string.ascii_letters + string.digits + string.punctuation

    characters = ''.join(char for char in characters if char not in exclude_chars)
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_and_copy_password():
    length = int(length_entry.get())
    complexity = complexity_var.get()
    exclude_chars = exclude_entry.get()

    password = generate_password(length, complexity, exclude_chars)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_to_clipboard():
    password = password_entry.get()
    pyperclip.copy(password)

# GUI setup
root = tk.Tk()
root.title("Password Generator")

# Length
length_label = tk.Label(root, text="Password Length:")
length_label.grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1)

# Complexity
complexity_label = tk.Label(root, text="Password Complexity:")
complexity_label.grid(row=1, column=0, sticky="w")
complexity_var = tk.StringVar()
complexity_var.set("Normal")
complexity_menu = tk.OptionMenu(root, complexity_var, "Weak", "Normal", "Strong" )
complexity_menu.grid(row=1, column=1, sticky="ew")

# Exclude Characters
exclude_label = tk.Label(root, text="Exclude Characters:")
exclude_label.grid(row=2, column=0, sticky="w")
exclude_entry = tk.Entry(root)
exclude_entry.grid(row=2, column=1)

# Generate Button
generate_button = tk.Button(root, text="Generate Password", command=generate_and_copy_password, bg='light grey')
generate_button.grid(row=3, column=0, columnspan=2)

# Generated Password Entry
password_label = tk.Label(root, text="Generated Password:")
password_label.grid(row=4, column=0, sticky="w")
password_entry = tk.Entry(root)
password_entry.grid(row=4, column=1)

# Copy Button
copy_button = tk.Button(root, text="Copy", command=copy_to_clipboard, bg='light grey')
copy_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
