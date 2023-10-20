import tkinter as tk, tkinter.ttk as ttk, tkinter.font as font
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as mbox
import os

root_window = tk.Tk()
file_entry_value = tk.StringVar()

def run(event=None):
    if (file_entry_value.get() == ''):
        mbox.showinfo(title="No file chosen", message="Please type the location of the file in the entry box or click Browse to choose a file.")
    else:
        if (not os.path.isfile(file_entry_value.get())):
            mbox.showerror(title="Invalid file path", message="Chosen file does not exist. Please make sure that the file path in the entry box is correct.")
        else:
            os.system("gnome-terminal -- sh -c \"bash -c \\\"python3 \\\\\\\""+file_entry_value.get()+"\\\\\\\"; printf \\\\\\\"\\n\\n[Script execution complete. Press Enter to close this terminal window.]\\\\\\\"; read a\\\"\"")
    file_entry.selection_range(0,0)

def cutoption(event=None):
    try:
        selected = file_entry.selection_get()
        root_window.clipboard_append(selected)
        file_entry_value.set(file_entry_value.get().replace(selected, ''))
        file_entry.icursor(file_entry.index('insert')-len(selected))
        file_entry.selection_range(0,0)
    except:
        return

def copyoption(event=None):
    try:
        selected = file_entry.selection_get()
        root_window.clipboard_append(selected)
        file_entry.selection_range(0,0)
    except:
        return

def pasteoption(event=None):
    try:
        selected = file_entry.selection_get()
        root_window.clipboard_append(selected)
        file_entry_value.set(file_entry_value.get().replace(selected, ''))
        file_entry.icursor(file_entry.index('insert')-len(selected))
    except:
        selection = ''
    clipboard_data = root_window.clipboard_get()
    cursor_position = file_entry.index('insert')
    print (clipboard_data)
    #file_entry_value.set(file_entry_value.get().replace(selection, clipboard_data))
    file_entry.insert(cursor_position, clipboard_data)
    file_entry.selection_range(cursor_position, cursor_position+len(clipboard_data))
    file_entry.xview_moveto(1.0)
    
def selectalloption(event=None):
    file_entry.selection_range(0, 'end')
    file_entry.icursor(len(file_entry_value.get()))
    file_entry.xview_moveto(1.0)

def browse(event=None):
    fev = file_entry_value.get()
    if (fev != ''):
        initdir = fev[0:fev.rindex('/')+1]
    else:
        initdir = os.getcwd()
    file_path = askopenfilename(initialdir=initdir, title="Select File", filetypes=(("Python scripts","*.py"), ("All Files", "*.*")))
    if (file_path not in ['', tuple()]):
        file_entry_value.set(file_path)
    file_entry.selection_range(0, 'end')
    file_entry.icursor(len(file_entry_value.get()))
    file_entry.xview_moveto(1.0)
    file_entry.focus_set()

def close_root_window(event=None):
    filepath = file_entry_value.get()
    if (filepath != '' and os.path.isfile(filepath)):
        lof = open(last_opened_file, 'w')
        lof.write(file_entry_value.get())
        lof.close()
    root_window.destroy()

def entry_right_click(event=None):
    try:
        erc.tk_popup(event.x_root, event.y_root, 0)        
    finally:
        erc.grab_release()

def entry_right_click_menu_focusout(event=None):
    erc.unpost()

WINDOW_BG_COLOR = "#f6f5f4"


last_opened_file = os.path.expanduser("~/.config/runpyscript_lastopenedfile.conf")

if (os.path.isfile(last_opened_file)):
    lof = open(last_opened_file)
    file_entry_value.set(lof.read())
    lof.close()
else:
    file_entry_value.set('')

root_window.configure(background=WINDOW_BG_COLOR)
root_window.resizable(0,0)
ttk.Style(root_window).theme_use('clam')
appfont = font.Font(family='Arial', size=10)

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

root_window.title("Run Your Python 3 Script")

# When the window-close event is triggered, function close_root_window(self) is executed
root_window.protocol("WM_DELETE_WINDOW", close_root_window)

# Creating the "Choose file:" label with appropriate attributes
choose_file_label = ttk.Label(root_window, text = 'Choose file:', font=appfont, background=WINDOW_BG_COLOR)
choose_file_label.place(x=20, y=20)

file_entry = ttk.Entry(root_window, textvariable=file_entry_value, font=appfont, state='normal', width=34)
file_entry.place(x=20, y=45)
file_entry.icursor(len(file_entry_value.get()))
file_entry.xview_moveto(1.0)
file_entry.selection_range(0, 'end')
file_entry.bind("<Button-3>", entry_right_click)
file_entry.focus_set()

style = ttk.Style()
style.configure('my.TButton', font=appfont)
browse_button = ttk.Button(root_window, text="Browse...", style="my.TButton", command=browse)
browse_button.place(x=343, y=36)

run_button = ttk.Button(root_window, text="Run script", style="my.TButton", command=run)


applabel = ttk.Label(root_window, text="This app was created by Arijit Kumar Das (Github: @ArijitKD).\n By using this app, you agree to the terms of the MIT License.", font=appfont, background=WINDOW_BG_COLOR)


erc_options = {"Cut":cutoption, "Copy":copyoption, "Paste":pasteoption, "Select All":selectalloption}
erc = tk.Menu(file_entry, tearoff=0, font=font.Font(family='Arial', size=9))
for option in erc_options.keys():
    if (option == "Select All"):
        erc.add_separator()
    erc.add_command(label=option, command=erc_options[option])


applabel.pack(side='bottom', pady=30)
run_button.pack(side="bottom", pady=50)
root_window.bind("<Button-1>", entry_right_click_menu_focusout)
root_window.bind("<Control-a>", selectalloption)
#root_window.bind("<Control-c>", copyoption)
#root_window.bind("<Control-x>", cutoption)
root_window.mainloop()
