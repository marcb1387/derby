import xml.etree.ElementTree as ET
import tkinter as tk
import time
from tkinter import filedialog
import tkinter.ttk as ttk


# parse the XML document
def parse_xml(file_path):
    tree = ET.parse(file_path)
    return tree.getroot()


# create the table header
def create_header(frame):
    tk.Label(frame, text="Heat", bg="grey", font=("Arial", font_size.get()), width=20, relief="solid").grid(row=0, column=1)
    tk.Label(frame, text="Race", bg="grey", font=("Arial", font_size.get()), width=20, relief="solid").grid(row=0, column=2)
    tk.Label(frame, text="Lane Number", bg="grey", font=("Arial", font_size.get()), width=20, relief="solid").grid(row=0, column=3)
    tk.Label(frame, text="Scout Name", bg="grey", font=("Arial", font_size.get()), width=20, relief="solid").grid(row=0, column=4)
    tk.Label(frame, text="Car", bg="grey", font=("Arial", font_size.get()), width=20, relief="solid").grid(row=0, column=5)
    tk.Label(frame, text="Result", bg="grey", font=("Arial", font_size.get()), width=20, relief="solid").grid(row=0, column=6)
    tk.Label(frame, text="ElapsedTime", bg="grey", font=("Arial", font_size.get()), width=20, relief="solid").grid(row=0, column=7)
    tk.Label(frame, text="Speed (mph)", bg="grey", font=("Arial", font_size.get()), width=20, relief="solid").grid(row=0, column=8)
    

# create the table body
def create_body(root, frame):
    races = []
    heat_count = 0
    for heat in root.findall('./Heats/Heat'):
        heat_count += 1
        for race in heat.findall('./Races/Race'):
            race_number = int(race.attrib["Number"])
            race_lanes = []
            for lane in race.findall('./Lanes/Lane'):
                elapsed_time = float(lane.attrib["ElapsedTime"])
                if elapsed_time == 0:  # skip lanes with 0 elapsed time
                    continue
                # calculate the speed in MPH
                speed = round((((32 / elapsed_time) / 1.4667) * 25), 0)
                lane_info = {"Car": lane.attrib["Car"], "Number": lane.attrib["Number"],
                             "Result": lane.attrib["Result"], "ElapsedTime": lane.attrib["ElapsedTime"], "Speed": speed}
                race_lanes.append(lane_info)
            races.append({"Number": race_number, "Lanes": race_lanes})

    # Find the last race with an elapsed_time greater than 0
    last_race = None
    for race in reversed(races):
        if race["Lanes"]:
            last_race = race
            break

    if last_race is None:
        return

    row_index = 1
    for lane in last_race["Lanes"]:
        tk.Label(frame, text=heat_count, font=("Arial", font_size.get()), width=20, relief="solid").grid(row=row_index, column=1)
        tk.Label(frame, text=last_race["Number"], font=("Arial", font_size.get()), width=20, relief="solid").grid(row=row_index, column=2)
        tk.Label(frame, text=lane["Number"], font=("Arial", font_size.get()), width=20, relief="solid").grid(row=row_index, column=3)
        car_element = root.find("./Cars/Car[@Number='" + lane["Car"] + "']")
        car_name = car_element.attrib["Name"]
        tk.Label(frame, text=car_name, font=("Arial", font_size.get()), width=20, relief="solid").grid(row=row_index, column=4)
        tk.Label(frame, text=lane["Car"], font=("Arial", font_size.get()), width=20, relief="solid").grid(row=row_index, column=5)
        tk.Label(frame, text=lane["Result"], font=("Arial", font_size.get()), width=20, relief="solid").grid(row=row_index, column=6)
        tk.Label(frame, text=lane["ElapsedTime"], font=("Arial", font_size.get()), width=20, relief="solid").grid(row=row_index, column=7)
        tk.Label(frame, text=str(lane["Speed"]), font=("Arial", font_size.get()), width=20, relief="solid").grid(row=row_index, column=8)  # add the speed column
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
font_size_label = tk.Label(root_window, text="Choose font size:")
font_size_label.pack()
font_size = tk.StringVar()
font_size_combo = ttk.Combobox(root_window, textvariable=font_size)
font_size_combo['values'] = ('12', '14', '16', '18', '20', '22', '24')
font_size_combo.current(3)
font_size_combo.pack()
tk.Button(root_window, text="Choose DBY File", command=choose_file).pack()
root_window.mainloop()
