import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as Et
import os
from colorama import Fore


from miscellaneous_dep import *
from open_level_dialog import open_level_dialog

level_file_path = open_level_dialog()

if not os.path.exists(level_file_path):
    critical_error(f'File "{level_file_path}" not found')
log(f"You work on {level_file_path}.")

root = tk.Tk()
root.title("LevelBuilder")
root.option_add("*teaOff", False)

# Import and apply the theme
root.tk.call("source", "forest-dark.tcl")
ttk.Style(root).theme_use("forest-dark")

# Make the app responsive
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

## Tools section

# Sound section
selected_sound_path = "/res/sound/youll_die.mp3"
select_sound_button = ttk.Button(root, text=selected_sound_path)
select_sound_button.grid(row=0, column=0, padx=(20, 5), pady=(10, 5), sticky="nw")

## Textures Section

# Frame for textures treeview
textures_frame = ttk.LabelFrame(root, text="Textures", padding=(5, 0))
textures_frame.grid(row=1, column=0, padx=(20, 5), pady=(5, 5), sticky="nsew")

# Textures treeview scrollbar
textures_treeview_scrollbar = ttk.Scrollbar(textures_frame)
textures_treeview_scrollbar.pack(side="right", pady=(0, 5), fill="y")

# Textures treeview
textures_treeview = ttk.Treeview(
    textures_frame,
    yscrollcommand=textures_treeview_scrollbar.set,
    show=["tree"],
    height=8,
)
textures_treeview.pack(expand=True, fill="both")
textures_treeview_scrollbar.config(command=textures_treeview.yview)


def update_textures_treeview():
    level_file = Et.parse(level_file_path)
    level_root = level_file.getroot()

    textures_root = level_root.find("textures")
    if textures_root is None:
        # création de la balise <textures> si elle n'existe pas
        Et.SubElement(level_root, "textures")
        level_file.write(level_file_path)
        textures_root = level_root.find("textures")
        if textures_root is not None:
            log('"<textures>" créé avec succès')
        else:
            exit(
                f'{Fore.RED}>> Error: "<textures>" can\'t be created, check the integrity of the file{Fore.RESET}'
            )

    textures_name_list = []
    for texture in textures_root:
        textures_name_list.append(texture.tag)
    iid = 0
    for texture_name in textures_name_list:
        textures_treeview.insert("", "end", str(iid), text=texture_name)
        iid += 1
    # TODO: change to update with the real values


update_textures_treeview()
# TODO: add event to update

# Delete texture button
delete_texture_button = ttk.Button(textures_frame, text="Delete")
delete_texture_button.pack(side=tk.LEFT, padx=(0, 5), pady=5)

# Texture entry
create_texture_entry = ttk.Entry(textures_frame)
create_texture_entry.pack(side=tk.LEFT, pady=5, fill="x", expand=True)
# TODO: add auto placeholder

# Create texture button
create_texture_button = ttk.Button(textures_frame, text="Create")
create_texture_button.pack(side=tk.RIGHT, padx=(5, 0), pady=5)
# TODO: activate when create_texture_entry is fill


# var with the name of the selected texture
selected_texture = ""

# Frame for frame path treeview
frames_frame = ttk.LabelFrame(root, padding=(5, 0))
frames_frame.grid(row=1, column=1, padx=(5, 20), pady=(5, 10), sticky="nsew")

# Frames treeview scrollbar
frames_treeview_scrollbar = ttk.Scrollbar(frames_frame)
frames_treeview_scrollbar.pack(
    side="right",
    pady=(0, 5),
    fill="y",
)

# Frames treeview
frames_treeview = ttk.Treeview(
    frames_frame,
    selectmode="extended",
    yscrollcommand=frames_treeview_scrollbar.set,
    show=["tree"],
    height=8,
)
frames_treeview.pack(expand=True, fill="both")
frames_treeview_scrollbar.config(command=frames_treeview.yview)


def update_frames_frame():
    selected_texture = "texture_porte_1"
    frames_frame.config(text=selected_texture)
    # TODO: change with the real value of the selection

    test_frames_path_list = [
        "/res/ttttt_0.png",
        "/res/zeedffc_0.png",
        "/res/ttttt_1.png",
        "/res/ttttt_2.png",
        "/res/ttttt_3.png",
        "/res/ttttt_4.png",
        "/res/azedc_0.png",
    ]
    iid = 0
    for frame_path in test_frames_path_list:
        frames_treeview.insert("", "end", str(iid), text=frame_path)
        iid += 1
    # TODO: change to update with the real values


textures_treeview.selection_set("0")
update_frames_frame()
# TODO: add event to update setlected textures on double click

# Add frames button
add_frames_button = ttk.Button(frames_frame, text="Add", style="Accent.TButton")
add_frames_button.pack(side=tk.LEFT, pady=5)

# Remove frames button
remove_frames_button = ttk.Button(frames_frame, text="Remove")
remove_frames_button.pack(side=tk.RIGHT, pady=5)

## Elements Section

# Frame for elements treeview
elements_frame = ttk.LabelFrame(root, text="Elements", padding=(5, 0))
elements_frame.grid(row=2, column=0, padx=(20, 5), pady=(5, 20), sticky="nsew")

# Elements treeview scrollbar
elements_treeview_scrollbar = ttk.Scrollbar(elements_frame)
elements_treeview_scrollbar.pack(side="right", pady=(0, 5), fill="y")

# Elements treeview
elements_treeview = ttk.Treeview(
    elements_frame,
    selectmode="browse",
    yscrollcommand=elements_treeview_scrollbar.set,
    columns=("1"),
    height=10,
)
elements_treeview.pack(expand=True, fill="both")
elements_treeview_scrollbar.config(command=elements_treeview.yview)

# Elements treeview columns
elements_treeview.column("#0", width=150)
elements_treeview.column(1, width=150)

# Elements headings
elements_treeview.heading("#0", text="Name", anchor="w")
elements_treeview.heading(1, text="Id", anchor="w")


def update_elements_treeview():
    test_elements_list = [
        ("plateforme1", "default", "default"),
        ("plateforme2", "default", "default"),
        ("porte1", "p1", "open", "close"),
        ("porte2", "p2", "open", "close"),
        ("porte3", "p3", "open", "close"),
        ("ladder1", "default", "default"),
        ("switch1", "p1", "activate", "desactivate"),
        ("switch2", "p2", "activate", "desactivate"),
        ("switch2", "p3", "activate", "desactivate"),
    ]
    iid = 0
    for element in test_elements_list:
        elements_treeview.insert(
            "", "end", str(iid), text=element[0], values=element[1]
        )
        parent = iid
        for state in element[2:]:
            iid += 1
            elements_treeview.insert(str(parent), "end", str(iid), text=state)
        iid += 1
    # TODO: change to update with the real values


update_elements_treeview()
# TODO: add event to refresh

# Delete element button
delete_element_button = ttk.Button(elements_frame, text="Delete")
delete_element_button.pack(side=tk.LEFT, padx=(0, 5), pady=5)

# Element entry
create_element_entry = ttk.Entry(elements_frame)
create_element_entry.pack(side=tk.LEFT, pady=5, fill="x", expand=True)
# TODO: add auto placeholder

# Create element button
create_element_button = ttk.Button(elements_frame, text="Create state")
create_element_button.pack(side=tk.RIGHT, padx=(5, 0), pady=5)
# TODO: activate when create_element_entry is fill

# Create state button
create_state_button = ttk.Button(elements_frame, text="Create element")
create_state_button.pack(side=tk.RIGHT, padx=(5, 0), pady=5)
# TODO: activate when create_element_entry is fill


# var with the name of the selected state
selected_state = ""

# Frame for state form
state_frame = ttk.LabelFrame(root, padding=(5, 0))
state_frame.grid(row=2, column=1, padx=(5, 20), pady=(5, 20), sticky="nsew")

# Form for state parameters
# TODO: Add form inputs


def update_element_form():
    selected_state = "porte1 - open"
    state_frame.config(text=selected_state)
    # TODO: change with real value


elements_treeview.selection_set("0")
update_element_form()
# TODO: add event to update state form on double click


# Center the window and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
root.geometry(f"+{x_cordinate}+{y_cordinate}")

# Start the main loop
root.mainloop()
