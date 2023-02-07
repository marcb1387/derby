import xml.etree.ElementTree as ET
import tkinter as tk
import time
from tkinter import filedialog

# parse the XML document
def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()

# create the table header
def create_header(root, frame):
    tk.Label(frame, text="Lane", bg="grey", font=("Arial", 12), width=20, relief="solid").grid(row=0, column=0)
    tk.Label(frame, text="Time", bg="grey", font=("Arial", 12), width=20, relief="solid").grid(row=0, column=1)

# create the table body
def create_body(root, frame):
    for row_index, lane in enumerate(root.findall(".//Lane")):
        tk.Label(frame, text=lane.attrib["id"], font=("Arial", 12), width=20, relief="solid").grid(row=row_index + 1, column=0)
        time = lane.find("ElapsedTime").text
        tk.Label(frame, text=time, font=("Arial", 12), width=20, relief="solid").grid(row=row_index + 1, column=1)

# refresh the table
def refresh_table(file_path, root, frame):
    root = parse_xml(file_path)
    for widget in frame.winfo_children():
        widget.destroy()
    create_header(root, frame)
    create_body(root, frame)
    frame.after(5000, refresh_table, file_path, root, frame)

# choose the file
def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("DBY files", "*.dby")])
    if not file_path:
        return
    root = parse_xml(file_path)
    frame = tk.Frame(root_window)
    frame.pack()
    create_header(root, frame)
    create_body(root, frame)
    refresh_table(file_path, root, frame)

# create the root window
root_window = tk.Tk()
root_window.title("Derby Data Analyzer")
tk.Button(root_window, text="Choose DBY File", command=choose_file).pack()
root_window.mainloop()
