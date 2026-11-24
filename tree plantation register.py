import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import math

FILE = "tree_records.json"

# LOAD DATA
def load_data():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []

records = load_data()

# SAVE DATA
def save_data():
    with open(FILE, "w") as f:
        json.dump(records, f, indent=4)

# ADD TREE
def add_tree():
    name = name_entry.get().strip()
    location = location_entry.get().strip()
    quantity = quantity_entry.get().strip()

    if not name or not location:
        messagebox.showerror("Error", "Enter tree name and location")
        return

    try:
        count = int(quantity)
        if count < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid quantity")
        return

    records.append({
        "name": name,
        "location": location,
        "quantity": count,
        "status": "Alive"
    })

    save_data()
    show_records()

    name_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

# DISPLAY RECORDS
def show_records():
    for item in table.get_children():
        table.delete(item)

    for i, r in enumerate(records):
        table.insert("", "end", values=(
            i + 1,
            r["name"],
            r["location"],
            r["quantity"],
            r["status"]
        ))

    total = sum(r["quantity"] for r in records)
    alive = sum(r["quantity"] for r in records
                if r["status"] == "Alive")

    total_label.config(text=f"🌳 Total Trees: {total}")
    alive_label.config(text=f"🌱 Alive Trees: {alive}")

# UPDATE TREE STATUS
def update_status():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Select", "Select a record first")
        return

    index = int(table.item(selected[0])["values"][0]) - 1

    records[index]["status"] = (
        "Dead" if records[index]["status"] == "Alive" else "Alive"
    )

    save_data()
    show_records()

# MAIN WINDOW
root = tk.Tk()
root.title("Tree Plantation Register")
root.geometry("1000x750")
root.configure(bg="#e5f5e5")

# NATURE CANVAS
canvas = tk.Canvas(
    root,
    height=180,
    bg="#b9e8bd",
    highlightthickness=0
)
canvas.pack(fill="x")

# SUN
canvas.create_oval(
    820, 15, 900, 95,
    fill="#ffdf70",
    outline=""
)

# CLOUDS
clouds = []

for x, y in [(100, 45), (400, 30), (680, 60)]:
    cloud = canvas.create_oval(
        x, y, x + 90, y + 35,
        fill="white",
        outline=""
    )
    clouds.append({"id": cloud, "x": x, "y": y})

# DRAW TREES
def draw_tree(x, y, size):
    canvas.create_line(
        x, y, x, y - 65 * size,
        fill="#79502b",
        width=int(7 * size)
    )

    canvas.create_oval(
        x - 35 * size,
        y - 105 * size,
        x + 35 * size,
        y - 45 * size,
        fill="#278b42",
        outline=""
    )

for x in [80, 220, 500, 750, 950]:
    draw_tree(x, 170, 0.8)

# FALLING LEAVES
leaves = []

for i in range(18):
    x = random.randint(10, 980)
    y = random.randint(-180, 170)

    leaf = canvas.create_oval(
        x, y, x + 9, y + 6,
        fill="#3c9b42",
        outline=""
    )

    leaves.append({
        "id": leaf,
        "x": x,
        "y": y,
        "speed": random.uniform(1, 3)
    })

# ANIMATION
frame = 0

def animate():
    global frame
    frame += 1

    # Falling leaf animation
    for leaf in leaves:
        leaf["y"] += leaf["speed"]

        leaf["x"] += math.sin(
            frame / 10 + leaf["y"] / 20
        ) * 1.5

        if leaf["y"] > 180:
            leaf["y"] = random.randint(-50, -10)
            leaf["x"] = random.randint(10, 980)

        canvas.coords(
            leaf["id"],
            leaf["x"],
            leaf["y"],
            leaf["x"] + 9,
            leaf["y"] + 6
        )

    # Moving clouds
    for cloud in clouds:
        cloud["x"] += 0.5

        if cloud["x"] > 1050:
            cloud["x"] = -100

        canvas.coords(
            cloud["id"],
            cloud["x"],
            cloud["y"],
            cloud["x"] + 90,
            cloud["y"] + 35
        )

    root.after(40, animate)

# TITLE
tk.Label(
    root,
    text="🌳 TREE PLANTATION REGISTER 🌳",
    font=("Arial", 23, "bold"),
    bg="#174d32",
    fg="white",
    pady=18
).pack(fill="x")

# TREE COUNTERS
total_label = tk.Label(
    root,
    text="🌳 Total Trees: 0",
    font=("Arial", 16, "bold"),
    bg="#e5f5e5",
    fg="#174d32"
)
total_label.pack(pady=8)

alive_label = tk.Label(
    root,
    text="🌱 Alive Trees: 0",
    font=("Arial", 16, "bold"),
    bg="#e5f5e5",
    fg="#278b42"
)
alive_label.pack(pady=5)

# INPUT FORM
form = tk.Frame(root, bg="#e5f5e5")
form.pack(pady=20)

tk.Label(
    form,
    text="Tree Name",
    bg="#e5f5e5",
    font=("Arial", 11, "bold")
).grid(row=0, column=0)

name_entry = tk.Entry(form, width=18, font=("Arial", 11))
name_entry.grid(row=1, column=0, padx=8)

tk.Label(
    form,
    text="Location",
    bg="#e5f5e5",
    font=("Arial", 11, "bold")
).grid(row=0, column=1)

location_entry = tk.Entry(form, width=18, font=("Arial", 11))
location_entry.grid(row=1, column=1, padx=8)

tk.Label(
    form,
    text="Quantity",
    bg="#e5f5e5",
    font=("Arial", 11, "bold")
).grid(row=0, column=2)

quantity_entry = tk.Entry(form, width=12, font=("Arial", 11))
quantity_entry.grid(row=1, column=2, padx=8)

tk.Button(
    form,
    text="🌱 Add Tree",
    command=add_tree,
    bg="#247344",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15
).grid(row=1, column=3, padx=10)

# TABLE DESIGN
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    rowheight=30,
    font=("Arial", 10),
    background="white",
    fieldbackground="white"
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold"),
    background="#247344",
    foreground="white"
)

table = ttk.Treeview(
    root,
    columns=("ID", "Name", "Location", "Quantity", "Status"),
    show="headings"
)

for col in ("ID", "Name", "Location", "Quantity", "Status"):
    table.heading(col, text=col)
    table.column(col, width=150, anchor="center")

table.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)

# UPDATE BUTTON
tk.Button(
    root,
    text="🔄 Update Survival Status",
    command=update_status,
    bg="#315f83",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=8
).pack(pady=10)

# START APPLICATION
show_records()
animate()

root.mainloop()