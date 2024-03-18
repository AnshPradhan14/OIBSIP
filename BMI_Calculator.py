import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Create SQLite database and table
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             weight REAL,
             height REAL,
             bmi REAL,
             date TEXT)''')
conn.commit()


# Function to calculate BMI
def calculate_bmi(weight, height, unit):
    if weight <= 0 or height <= 0:
        return None
    if unit == "Meters":
        return round(weight / (height ** 2), 2)
    elif unit == "Feet":
        # Convert feet to meters
        height_meters = height * 0.3048
        return round(weight / (height_meters ** 2), 2)


# Function to categorize BMI
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Healthy weight"
    elif 25.0 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


# Function to handle user input and calculate BMI
def calculate_button_clicked():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        unit = unit_var.get()
        bmi = calculate_bmi(weight, height, unit)
        if bmi:
            result_label.config(text=f"BMI: {bmi} ({categorize_bmi(bmi)})")
            # Insert data into database
            ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
            c.execute("INSERT INTO users (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                      (name, weight, height, bmi, ist_time.strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            clear_button.grid(row=3, column=2)
            plot_button.grid(row=6, column=0, columnspan=2)
        else:
            messagebox.showerror("Error", "Weight and height must be positive numbers")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for weight and height")


# Function to clear weight and height fields
def clear_values():
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")
    clear_button.grid_forget()
    plot_button.grid_forget()


# Function to view historical data
def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    scrollbar = tk.Scrollbar(history_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    history_listbox = tk.Listbox(history_window, yscrollcommand=scrollbar.set)
    history_listbox.pack(fill=tk.BOTH, expand=1)

    c.execute("SELECT name, date, bmi FROM users WHERE name=?", (name_entry.get(),))
    data = c.fetchall()
    for row in data:
        history_listbox.insert(tk.END, f"Name: {row[0]} - Date/Time: {row[1]} - BMI: {row[2]}")

    scrollbar.config(command=history_listbox.yview)


# Function to plot historical BMI data
def plot_history():
    c.execute("SELECT date, bmi FROM users WHERE name=?", (name_entry.get(),))
    data = c.fetchall()
    dates = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') for row in data]
    bmis = [row[1] for row in data]

    plt.plot(dates, bmis, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.title('BMI Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# GUI
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1)

tk.Label(root, text="Height:").grid(row=2, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1)

unit_var = tk.StringVar(root)
unit_var.set("Meters")
unit_menu = tk.OptionMenu(root, unit_var, "Meters", "Feet")
unit_menu.grid(row=2, column=2)

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_button_clicked, bg='light grey')
calculate_button.grid(row=3, column=0)

clear_button = tk.Button(root, text="Clear Values", command=clear_values, bg='light grey')
result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

history_button = tk.Button(root, text="View History", command=view_history, bg='light grey')
history_button.grid(row=5, column=0, columnspan=2)

plot_button = tk.Button(root, text="Plot History", command=plot_history, bg='light grey')

root.mainloop()

# Close database connection
conn.close()
