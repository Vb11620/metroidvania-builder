import tkinter as tk
from tkinter import ttk
import tkinter.filedialog


def open_level_dialog():
    selectLevelFileWindow = tk.Tk()
    selectLevelFileWindow.title("Select Level File")

    selectLevelFileWindow.tk.call("source", "forest-dark.tcl")
    ttk.Style(selectLevelFileWindow).theme_use("forest-dark")

    file_path = tk.StringVar()

    def search_level_file():
        # selecting existing lvl file
        open_file_path = tkinter.filedialog.askopenfilename(
            initialdir="res/levels/",
            filetypes=(("Level files", "*.xml"), ("All files", "*.*")),
        )
        if not isinstance(open_file_path, str):
            return

        file_path.set(open_file_path)
        selectLevelFileWindow.destroy()

    searchLevelFileButton = ttk.Button(
        selectLevelFileWindow,
        text="Open Level",
        style="Accent.TButton",
        command=search_level_file,
    )

    def new_level_file():
        # selecting the emplacement of the future lvl file
        open_file_path = tkinter.filedialog.asksaveasfilename(
            initialdir="res/levels/",
            filetypes=(("Level files", "*.xml"), ("All files", "*.*")),
        )
        if open_file_path == "":
            return

        # adding of the main structure of the lvl file
        open_file = open(open_file_path, mode="w")
        open_file.write("<selectLevelFileWindow></selectLevelFileWindow>")
        open_file.close()

        file_path.set(open_file_path)
        selectLevelFileWindow.destroy()

    newLevelFileButton = ttk.Button(
        selectLevelFileWindow, text="New Level", command=new_level_file
    )

    searchLevelFileButton.pack(pady=6, padx=3)
    newLevelFileButton.pack(pady=6, padx=3)

    def packWindow(window: tk.Tk):
        # Center the window, and set minsize
        window.update()
        window.minsize(window.winfo_width(), window.winfo_height())
        x_cordinate = int((window.winfo_screenwidth() / 2) - (window.winfo_width() / 2))
        y_cordinate = int(
            (window.winfo_screenheight() / 2) - (window.winfo_height() / 2)
        )
        window.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    packWindow(selectLevelFileWindow)

    selectLevelFileWindow.mainloop()

    return file_path.get()
