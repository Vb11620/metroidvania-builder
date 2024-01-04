import tkinter as tk
import tkinter.filedialog
from tkinter import StringVar, ttk, simpledialog
import os


from miscellaneous_dep import *
from open_level_dialog import open_level_dialog
from xml_dep import *

# level_file_path = open_level_dialog()
level_file_path = "/home/vincent/Projets/metroidvania-builder/test.xml"

if not os.path.exists(level_file_path):
    critical_error(f'File "{level_file_path}" not found')
log(f"You work on {level_file_path}.")

root = tk.Tk()
root.title(f"LevelBuilder - {level_file_path}")
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
sound_path = StringVar()


def update_sound_button():
    level_file = Et.parse(level_file_path)
    level_root = level_file.getroot()

    sound_element = level_root.find("sound")
    if sound_element is not None:
        sound_path_str = sound_element.get("path")
        if sound_path_str is not None:
            sound_path.set(sound_path_str)
        else:
            sound_path.set("")
    else:
        sound_path.set("")


def select_sound():
    sound_path_str = tkinter.filedialog.askopenfilename(
        initialdir="res/levels/",
        filetypes=(("MP3 Sounds", "*.mp3"), ("All files", "*.*")),
    )
    if isinstance(sound_path_str, str):
        level_file = Et.parse(level_file_path)
        level_root = level_file.getroot()

        sound_element = level_root.find("sound")
        if sound_element is not None:
            level_root.remove(sound_element)
        if sound_path_str != "":
            Et.SubElement(level_root, "sound").set("path", sound_path_str)
        level_file.write(level_file_path)

    root.event_generate("<<uptate_all_data>>")


select_sound_button = ttk.Button(root, textvariable=sound_path, command=select_sound)
select_sound_button.grid(row=0, column=0, padx=(20, 5), pady=(10, 5), sticky="nw")

update_sound_button()

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

    textures_root = get_element_by_name_forced(
        level_root, "textures", level_file, level_file_path
    )

    textures_name_list = []
    for texture in textures_root:
        textures_name_list.append(texture.tag)

    if textures_name_list == []:
        textures_name_list.append(
            get_element_by_name_forced(
                textures_root, "foreground", level_file, level_file_path
            ).tag
        )
        textures_name_list.append(
            get_element_by_name_forced(
                textures_root, "background", level_file, level_file_path
            ).tag
        )

    textures_treeview.delete(*textures_treeview.get_children())
    iid = 0
    for texture_name in textures_name_list:
        textures_treeview.insert("", "end", str(iid), text=texture_name)
        iid += 1


update_textures_treeview()

# Delete texture button


def delete_texture():
    if textures_treeview.selection() != ():
        level_file = Et.parse(level_file_path)
        level_root = level_file.getroot()

        textures_root = get_element_by_name_forced(
            level_root, "textures", level_file, level_file_path
        )
        selected_texture_name = textures_treeview.item(
            textures_treeview.selection()[0]
        )["text"]

        remove_element_by_name(
            textures_root, selected_texture_name, level_file, level_file_path
        )

        root.event_generate("<<uptate_all_data>>")

    else:
        minor_log("No element selected")


delete_texture_button = ttk.Button(
    textures_frame, text="Delete", command=delete_texture
)
delete_texture_button.pack(side=tk.LEFT, padx=(0, 5), pady=5)

# Texture entry
create_texture_entry_stringVar = StringVar()
create_texture_entry = ttk.Entry(
    textures_frame, textvariable=create_texture_entry_stringVar
)
create_texture_entry.pack(side=tk.LEFT, pady=5, fill="x", expand=True)


def create_texture():
    if create_texture_entry.get() != "":
        level_file = Et.parse(level_file_path)
        level_root = level_file.getroot()

        textures_root = get_element_by_name_forced(
            level_root, "textures", level_file, level_file_path
        )

        create_element_if_doesnt_exist(
            textures_root, create_texture_entry.get(), level_file, level_file_path
        )

        root.event_generate("<<uptate_all_data>>")
    else:
        minor_log("No name given")


# Create texture button
create_texture_button = ttk.Button(
    textures_frame, text="Create", command=create_texture
)
create_texture_button.pack(side=tk.RIGHT, padx=(5, 0), pady=5)


# Activate when create_texture_entry is fill
def update_create_texture_button(*_):
    if create_texture_entry.get() != "":
        create_texture_button["style"] = "Accent.TButton"
    else:
        create_texture_button["style"] = "TButton"


create_texture_entry_stringVar.trace("w", update_create_texture_button)

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


def update_frames_frame(*_):
    if textures_treeview.selection() != ():
        selected_texture = textures_treeview.item(textures_treeview.selection()[0])[
            "text"
        ]
        frames_frame.config(text=selected_texture)

        level_file = Et.parse(level_file_path)
        level_root = level_file.getroot()

        textures_root = get_element_by_name_forced(
            level_root, "textures", level_file, level_file_path
        )
        frames_root = get_element_by_name_forced(
            textures_root, selected_texture, level_file, level_file_path
        )

        frames_path_list = []
        for frame in frames_root:
            frames_path_list.append(frame.get("path"))

        frames_treeview.delete(*frames_treeview.get_children())
        iid = 0
        for frame_path in frames_path_list:
            frames_treeview.insert("", "end", str(iid), text=frame_path)
            iid += 1
    else:
        frames_treeview.delete(*frames_treeview.get_children())
        frames_frame.config(text="")


update_frames_frame()
textures_treeview.bind("<<TreeviewSelect>>", update_frames_frame)


# Add frames button
def add_frame():
    if textures_treeview.selection() != ():
        new_frame_path = os.path.relpath(
            tkinter.filedialog.askopenfilename(
                initialdir="res/levels/",
                filetypes=(("PNG Images", "*.png"), ("All files", "*.*")),
            )
        )
        if isinstance(new_frame_path, str):
            level_file = Et.parse(level_file_path)
            level_root = level_file.getroot()
            selected_texture = textures_treeview.item(textures_treeview.selection()[0])[
                "text"
            ]

            textures_root = get_element_by_name_forced(
                level_root, "textures", level_file, level_file_path
            )
            frames_root = get_element_by_name_forced(
                textures_root, selected_texture, level_file, level_file_path
            )
            if new_frame_path != "":
                Et.SubElement(frames_root, "frame").set("path", new_frame_path)
                level_file.write(level_file_path)

                created = False
                for element in frames_root:
                    if element.get("path") == new_frame_path:
                        created = True
                if created:
                    achievement_log(
                        f'"<frame path="{new_frame_path}">" créé avec succès'
                    )
                else:
                    exit(
                        f'{Fore.RED}>> Error: "<frame path="{new_frame_path}">" can\'t be created, check the integrity of the file{Fore.RESET}'
                    )
        root.event_generate("<<uptate_all_data>>")
    else:
        minor_log("No texture selected")


add_frames_button = ttk.Button(
    frames_frame, text="Add", style="Accent.TButton", command=add_frame
)
add_frames_button.pack(side=tk.LEFT, pady=5)


# Remove frames button
def remove_frame():
    level_file = Et.parse(level_file_path)
    level_root = level_file.getroot()

    if frames_treeview.selection() != ():
        textures_root = get_element_by_name_forced(
            level_root, "textures", level_file, level_file_path
        )
        selected_texture_name = textures_treeview.item(
            textures_treeview.selection()[0]
        )["text"]
        frames_root = get_element_by_name_forced(
            textures_root, selected_texture_name, level_file, level_file_path
        )

        selected_frame_path = frames_treeview.item(frames_treeview.selection()[0])[
            "text"
        ]

        remove_elements_by_attribute(
            frames_root, "path", selected_frame_path, level_file, level_file_path
        )

        root.event_generate("<<uptate_all_data>>")

    else:
        minor_log("No element selected")


remove_frames_button = ttk.Button(frames_frame, text="Remove", command=remove_frame)
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
    level_file = Et.parse(level_file_path)
    level_root = level_file.getroot()

    elements_root = get_element_by_name_forced(
        level_root, "elements", level_file, level_file_path
    )

    elements_list = []
    for element in elements_root:
        state_list = []
        for state in element:
            state_list.append(state.tag)
        elements_list.append(tuple([element.tag, element.get("id")] + state_list))

    if elements_list == []:
        ground = get_element_by_name_forced(
            elements_root, "ground", level_file, level_file_path
        )
        ground.set("id", "default")
        default_ground_state = get_element_by_name_forced(
            ground, "default", level_file, level_file_path
        )
        elements_list.append((ground.tag, ground.get("id"), default_ground_state.tag))

    for i in elements_treeview.get_children():
        elements_treeview.delete(i)

    iid = 0
    for element in elements_list:
        if element[1] is not None:
            elements_treeview.insert(
                "", "end", str(iid), text=element[0], values=element[1]
            )
        else:
            critical_error(f"Level file broken, '{element[0]}' does not have id")
        parent = iid
        for state in element[2:]:
            iid += 1
            elements_treeview.insert(str(parent), "end", str(iid), text=state)
        iid += 1


update_elements_treeview()


# Delete element button
def delete_element_or_state():
    level_file = Et.parse(level_file_path)
    level_root = level_file.getroot()

    if elements_treeview.selection() != ():
        parent_iid = elements_treeview.parent(elements_treeview.selection()[0])
        if parent_iid == "":
            selected_state_parent_name = elements_treeview.item(
                elements_treeview.selection()[0]
            )["text"]

            elements_root = get_element_by_name_forced(
                level_root, "elements", level_file, level_file_path
            )

            remove_element_by_name(
                elements_root, selected_state_parent_name, level_file, level_file_path
            )

        else:
            selected_state_parent_name = elements_treeview.item(parent_iid)["text"]
            selected_state_name = elements_treeview.item(
                elements_treeview.selection()[0]
            )["text"]

            elements_root = get_element_by_name_forced(
                level_root, "elements", level_file, level_file_path
            )
            states_root = get_element_by_name_forced(
                elements_root, selected_state_parent_name, level_file, level_file_path
            )

            remove_element_by_name(
                states_root, selected_state_name, level_file, level_file_path
            )

        root.event_generate("<<uptate_all_data>>")

    else:
        minor_log("No element selected")


delete_element_button = ttk.Button(
    elements_frame, text="Delete", command=delete_element_or_state
)
delete_element_button.pack(side=tk.LEFT, padx=(0, 5), pady=5)

# Element entry
create_element_entry_stringVar = StringVar()
create_element_entry = ttk.Entry(
    elements_frame, textvariable=create_element_entry_stringVar
)
create_element_entry.pack(side=tk.LEFT, pady=5, fill="x", expand=True)


# Create state button
def create_state():
    if create_element_entry.get() != "":
        if elements_treeview.selection() != ():
            parent_iid = elements_treeview.parent(elements_treeview.selection()[0])
            if parent_iid == "":
                parent_iid = elements_treeview.selection()[0]

            level_file = Et.parse(level_file_path)
            level_root = level_file.getroot()

            elements_root = get_element_by_name_forced(
                level_root, "elements", level_file, level_file_path
            )

            states_root = get_element_by_name_forced(
                elements_root,
                elements_treeview.item(parent_iid)["text"],
                level_file,
                level_file_path,
            )

            create_element_if_doesnt_exist(
                states_root, create_element_entry.get(), level_file, level_file_path
            )

            root.event_generate("<<uptate_all_data>>")
        else:
            minor_log("No element selected")
    else:
        minor_log("No name given")


create_state_button = ttk.Button(
    elements_frame, text="Create state", command=create_state
)
create_state_button.pack(side=tk.RIGHT, padx=(5, 0), pady=5)


# Create element button
def create_element():
    if create_element_entry.get() != "":
        new_element_id = simpledialog.askstring(
            title="Element Id",
            prompt=f"What's the ID of {create_element_entry.get()}",
            parent=root,
        )
        if new_element_id is not None:
            if new_element_id == "":
                new_element_id = "default"
        else:
            new_element_id = "default"
        level_file = Et.parse(level_file_path)
        level_root = level_file.getroot()

        elements_root = get_element_by_name_forced(
            level_root, "elements", level_file, level_file_path
        )

        get_element_by_name_forced(
            elements_root, create_element_entry.get(), level_file, level_file_path
        ).set("id", new_element_id)
        level_file.write(level_file_path)

        root.event_generate("<<uptate_all_data>>")
    else:
        minor_log("No name given")


create_element_button = ttk.Button(
    elements_frame, text="Create element", command=create_element
)
create_element_button.pack(side=tk.RIGHT, padx=(5, 0), pady=5)


# Activate the buttons when create_element_entry is fill
def update_elements_buttons(*_):
    if create_element_entry.get() != "":
        create_element_button["style"] = "Accent.TButton"
        if elements_treeview.selection() != ():
            create_state_button["style"] = "Accent.TButton"
        else:
            create_state_button["style"] = "TButton"
    else:
        create_element_button["style"] = "TButton"
        create_state_button["style"] = "TButton"


create_element_entry_stringVar.trace("w", update_elements_buttons)


# var with the name of the selected state
selected_state = ""

# Frame for state form
state_frame = ttk.LabelFrame(root, padding=(5, 0))
state_frame.grid(row=2, column=1, padx=(5, 20), pady=(5, 20), sticky="nsew")

# Form for state parameters
# TODO: Add form inputs


def update_state_frame(*_):
    update_elements_buttons()
    if elements_treeview.selection() != ():
        parent_iid = elements_treeview.parent(elements_treeview.selection()[0])
        if parent_iid != "":
            selected_state = f"{elements_treeview.item(parent_iid)['text']} - {elements_treeview.item(elements_treeview.selection()[0])['text']}"
            state_frame.config(text=selected_state)
    else:
        state_frame.config(text="")


update_state_frame()
elements_treeview.bind("<<TreeviewSelect>>", update_state_frame)


# Function to uptate all
def uptate_all_data(*_):
    update_sound_button()
    update_textures_treeview()
    textures_treeview.selection_set("0")
    update_frames_frame()
    update_elements_treeview()
    elements_treeview.selection_set("0")
    update_state_frame()


root.bind("<<uptate_all_data>>", uptate_all_data)

# Center the window and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
root.geometry(f"+{x_cordinate}+{y_cordinate}")

# Start the main loop
root.mainloop()
