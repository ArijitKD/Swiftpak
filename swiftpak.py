import tkinter as tk, tkinter.ttk as ttk, tkinter.font as font, tkinter.messagebox as mbox, os
from platform import system

import guifeatures as guif


if (__name__ == "__main__"):    #Define private functions that will be accessible from here only
    def _run():
        if (file_entry_value.get() == ''):
            mbox.showinfo(title="No file chosen", message="Please type the location of the file in the entry box or click Browse to choose a file.")
        else:
            if (not os.path.isfile(file_entry_value.get())):
                mbox.showerror(title="Invalid file path", message="Chosen file does not exist. Please make sure that the file path in the entry box is correct.")
            else:
                os.system("gnome-terminal -- sh -c \"bash -c \\\"python3 \\\\\\\""+file_entry_value.get()+"\\\\\\\"; printf \\\\\\\"\\n\\n[Script execution complete. Press Enter to close this terminal window.]\\\\\\\"; read a\\\"\"")
        file_entry.selection_range(0,0)


    def _close_root_window():
        filepath = file_entry_value.get()
        print (filepath)
        config_data["last_opened_file"] = filepath
        _save_config(config_data, config_file)
        root_window.destroy()

    def _entry_right_click(event):
        try:
            erc.tk_popup(event.x_root, event.y_root, 0)        
        finally:
            erc.grab_release()

    def _entry_right_click_menu_focusout():
        erc.unpost()

    def _save_config(config_data, config_file):
        print ("Save config data -->", config_data)
        with open(config_file, 'w') as configurations:
            keys = tuple(config_data.keys())
            values = tuple(config_data.values())
            for i in range(len(config_data)):
                configurations.write("[%s]\n"%(keys[i].upper(),))
                configurations.write("%s\n\n"%(values[i],))

    def _load_config(config_file):
        with open(config_file) as configurations:
            tmp_config_data = configurations.readlines()
            for line in tmp_config_data:
                if (line.startswith("#") or line.startswith("//")):
                    tmp_config_data.pop(tmp_config_data.index(line))
            config_data = dict()
            for i in range(len(tmp_config_data)):
                tmp_config_data[i] = tmp_config_data[i].strip()
                if (tmp_config_data[i].startswith('[') and tmp_config_data[i].endswith(']')):
                    try:
                        config_data[tmp_config_data[i][1:-1].lower()] = tmp_config_data[i+1].rstrip('\n')
                    except IndexError:
                        config_data[tmp_config_data[i][1:-1].lower()] = ""
        print ("Load config data -->", config_data)
        return config_data
    
    def _load_language_pack(language="english"):
        separator = "\\" if SYSTEM == "Windows" else "/"
        with open(LANGUAGES_DIR+separator+language, encoding="utf-8") as langfile:
            tmp_lang_data = langfile.readlines()
            for line in tmp_lang_data:
                if (line.startswith("#") or line.startswith("//")):
                    tmp_lang_data.pop(tmp_lang_data.index(line))
            lang_data = dict()
            for i in range(len(tmp_lang_data)):
                tmp_lang_data[i] = tmp_lang_data[i].strip()
                if (tmp_lang_data[i].startswith('[') and tmp_lang_data[i].endswith(']')):
                    try:
                        tmp_lang_data[i+1] = tmp_lang_data[i+1].rstrip('\n')
                        tmp_lang_data[i+1] = tmp_lang_data[i+1].replace("\\n", "\n").replace("\\\'", "\'").replace("\\\"", "\"").replace("\\t", "\t").replace("\\\\", '\\')
                        lang_data[tmp_lang_data[i][1:-1].lower()] = tmp_lang_data[i+1][1:-1] if tmp_lang_data[i+1] != "" else tmp_lang_data[i][1:-1]
                    except IndexError:
                        lang_data[tmp_lang_data[i][1:-1].lower()] = tmp_lang_data[i][1:-1]
        #print ("Load language data -->", lang_data)
        return lang_data


## CONSTANTS
LANGUAGES_DIR = "languages"
WINDOW_BG_COLOR = '#f6f5f4'
SYSTEM = system()
DEFAULT_CONFIG_DATA = {
                            "last_opened_file" : "",
                            "app_language"     : "english"
}


# Execution starts from here...

# Create the configuration directory and file, if not present already and set the default configuration if the app is running for the 1st time
if (SYSTEM == "WINDOWS"):
    config_dir = os.environ["APPDATA"]+"\\Swiftpak"
    if (not os.path.isdir(config_dir)):
        os.mkdir(config_dir)
    config_file = config_dir+"\\config.cfg"
else:
    config_dir = os.path.expanduser("~/.config/Swiftpak")
    if (not os.path.isdir(config_dir[:config_dir.rindex('/')])):
        os.mkdir(config_dir[:config_dir.rindex('/')])
    if (not os.path.isdir(config_dir)):
        os.mkdir(config_dir)
    config_file = config_dir+"/config.cfg"

if (not os.path.isfile(config_file)):
     _save_config(DEFAULT_CONFIG_DATA, config_file)

# Load all configurations
config_data = _load_config(config_file)

# Creating the root window
root_window = tk.Tk()
file_entry_value = tk.StringVar()

# Setting the loaded configurations
lang_data = _load_language_pack(config_data["app_language"])    # Set app language

# Setting the file entry value from loaded configuration
if (os.path.isfile(config_data['last_opened_file'])):
    file_entry_value.set(config_data['last_opened_file'])
else:                                                           # What if the file has been moved or deleted?
    file_entry_value.set('')
    config_data['last_opened_file'] = DEFAULT_CONFIG_DATA['last_opened_file']

APP_NAME = lang_data["app_name"]                                # The default title that will appear on the title bar.
ALLOWED_FILE_TYPES = (
                            (lang_data["browse_dialog_box_filetype_png"],"*.png"),
                            (lang_data["browse_dialog_box_filetype_jpeg"], "*.jpeg *.jpg"),
                            (lang_data["browse_dialog_box_filetype_all"], "*.*")
)


root_window.title(APP_NAME)                                     # Set the app name in the chosen language
root_window.configure(background=WINDOW_BG_COLOR)
root_window.resizable(0,0)
appfont = font.Font(family='Arial', size=int(lang_data['font_size']))

if (SYSTEM != "Windows"):
    ttk.Style(root_window).theme_use('clam')

# Screen dimensions
screen_width = root_window.winfo_screenwidth()
screen_height = root_window.winfo_screenheight()

# Fixed dimensions of the root window (480x300)
root_winwidth = 480
root_winheight = 300

# The code fragment below will position the root window at the centre of the screen
center_x = int((screen_width/2) - (root_winwidth/2))
center_y = int((screen_height/2) - (root_winheight/2))
root_window.geometry(str(root_winwidth)+"x"+str(root_winheight)+"+"+str(center_x)+"+"+str(center_y))

# When the window-close event is triggered, function close_root_window(self) is executed
root_window.protocol("WM_DELETE_WINDOW", _close_root_window)

# Creating the "Choose file:" label with appropriate attributes
choose_file_label = ttk.Label(root_window, text = lang_data['choose_file']+':', font=appfont, background=WINDOW_BG_COLOR)
choose_file_label.place(x=20, y=20)

file_entry = ttk.Entry(root_window, textvariable=file_entry_value, font=appfont, state='normal', width=42)
file_entry.place(x=20, y=45)
file_entry.icursor(len(file_entry_value.get()))
file_entry.xview_moveto(1.0)
file_entry.selection_range(0, 'end')
file_entry.bind("<Button-3>", _entry_right_click)
file_entry.focus_set()

style = ttk.Style()
style.configure('my.TButton', font=appfont)
browse_button = ttk.Button(root_window, text=lang_data["browse_button"]+"...", style="my.TButton", command=lambda: guif.browseforfile(root_window, file_entry, file_entry_value, title=lang_data["browse_dialog_box_title"], filetypes=ALLOWED_FILE_TYPES))

run_button = ttk.Button(root_window, text=lang_data["compress_button"], style="my.TButton", command=_run)


app_label = ttk.Label(root_window, text=lang_data["app_label"], font=appfont, background=WINDOW_BG_COLOR, justify='center')


erc_options = {
                lang_data["cut"]           :   (lambda: guif.cut(root_window, file_entry, file_entry_value)),
                lang_data["copy"]          :   (lambda: guif.copy(root_window, file_entry, file_entry_value)),
                lang_data["paste"]         :   (lambda: guif.paste(root_window, file_entry, file_entry_value)),
                lang_data["select_all"]    :   (lambda event: guif.selectall(file_entry, file_entry_value))
}

erc = tk.Menu(file_entry, tearoff=0, font=font.Font(family='Arial', size=9))
for option in erc_options.keys():
    if (option == "Select All"):
        erc.add_separator()
    erc.add_command(label=option, command=erc_options[option])

if (SYSTEM == "Windows"):
    browse_button.place(x=343, y=44)
else:
    browse_button.place(x=343, y=36)
app_label.pack(side='bottom', pady=25)
run_button.pack(side="bottom", pady=50)
root_window.bind("<Button-1>", lambda event: _entry_right_click_menu_focusout())
root_window.bind("<Control-a>", erc_options[lang_data["select_all"]])
root_window.mainloop()
