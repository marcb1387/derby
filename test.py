import xml.etree.ElementTree as ET
import tkinter as tk
import time
from tkinter import filedialog

# parse the XML document
def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()


# create the table header
def create_header(frame):
    tk.Label(frame, text="Heat", bg="grey", font=("Arial", 12), width=20, relief="solid").grid(row=0, column=1)
    tk.Label(frame, text="Race", bg="grey", font=("Arial", 12), width=20, relief="solid").grid(row=0, column=2)
    tk.Label(frame, text="Lane Number", bg="grey", font=("Arial", 12), width=20, relief="solid").grid(row=0, column=3)
    tk.Label(frame, text="Car", bg="grey", font=("Arial", 12), width=20, relief="solid").grid(row=0, column=4)
    tk.Label(frame, text="Result", bg="grey", font=("Arial", 12), width=20, relief="solid").grid(row=0, column=5)
    tk.Label(frame, text="ElapsedTime", bg="grey", font=("Arial", 12), width=20, relief="solid").grid(row=0, column=6)
    

# create the table body
def create_body(root, frame):
    races = []
    heat_count = 0
    for heat in root.findall('./Heats/Heat'):
        heat_count += 1
        for race in heat.findall('./Races/Race'):
            race_number = race.attrib["Number"]
            race_lanes = []
            for lane in race.findall('./Lanes/Lane'):
                lane_info = {"Car": lane.attrib["Car"], "Number": lane.attrib["Number"],
                             "Result": lane.attrib["Result"], "ElapsedTime": lane.attrib["ElapsedTime"]}
                race_lanes.append(lane_info)
            races.append({"Number": race_number, "Lanes": race_lanes})
        
    last_race = races[-1]
    row_index = 1

    for lane in last_race["Lanes"]:
        tk.Label(frame, text=heat_count, font=("Arial", 12), width=20, relief="solid").grid(row=row_index, column=1)
        tk.Label(frame, text=last_race["Number"], font=("Arial", 12), width=20, relief="solid").grid(row=row_index, column=2)
        tk.Label(frame, text=lane["Number"], font=("Arial", 12), width=20, relief="solid").grid(row=row_index, column=3)
        tk.Label(frame, text=lane["Car"], font=("Arial", 12), width=20, relief="solid").grid(row=row_index, column=4)
        tk.Label(frame, text=lane["Result"], font=("Arial", 12), width=20, relief="solid").grid(row=row_index, column=5)
        tk.Label(frame, text=lane["ElapsedTime"], font=("Arial", 12), width=20, relief="solid").grid(row=row_index, column=6)
        row_index += 1



# refresh the table
def refresh_table(file_path, root, frame):
    root = parse_xml(file_path)
    print (root)
    for widget in frame.winfo_children():
        widget.destroy()
    create_header(frame)
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
    create_header(frame)
    create_body(root, frame)
    refresh_table(file_path, root, frame)

# create the root window
root_window = tk.Tk()
root_window.title("Derby Data Analyzer")
tk.Button(root_window, text="Choose DBY File", command=choose_file).pack()
root_window.mainloop()
