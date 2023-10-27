import tkinter as tk, tkinter.ttk as ttk, tkinter.filedialog as fdlg, os, time
from typing import Union
from platform import system
from threading import Thread


def _resizewindow(windowname: str, mvarg: tuple):
    comstring = "wmctrl -r \""+windowname+"\" -e "
    i=0
    while (i<4):
        comstring += str(mvarg[i])+","
        i+=1
    comstring += str(mvarg[i])
    time.sleep(0.1)
    os.system(comstring)


def cut(root: tk.Tk, text_widget: Union[tk.Entry, ttk.Entry, tk.Text], stringvar: tk.StringVar):
        try:
            if (stringvar.get() == ''):
                return
            root.clipboard_clear()
            selected = text_widget.selection_get()
            selected_from_end = False
            if (stringvar.get().endswith(selected)):
                selected_from_end = True
            root.clipboard_append(selected)
            stringvar.set(stringvar.get().replace(selected, ''))
            if (not selected_from_end):
                text_widget.icursor(text_widget.index('insert')-len(selected))
            text_widget.selection_range(0,0)
        except:
            return


def copy(root: tk.Tk, text_widget: Union[tk.Entry, ttk.Entry, tk.Text], stringvar: tk.StringVar):
    try:
        if (stringvar.get() == ''):
            return
        root.clipboard_clear()
        selected = text_widget.selection_get()
        root.clipboard_append(selected)
        text_widget.selection_range(0,0)
    except:
        return


def paste(root: tk.Tk, text_widget: Union[tk.Entry, ttk.Entry, tk.Text], stringvar: tk.StringVar):
    try:
        clipboard_data = root.clipboard_get()
    except:
        clipboard_data = ''
    try:
        selected = text_widget.selection_get()
    except:
        selected = ''
    if (selected != '' and clipboard_data != ''):
        cut(root, text_widget, stringvar)
    if (selected != '' and clipboard_data == ''):
        text_widget.selection_range(0,0) 
    cursor_position = text_widget.index('insert')
    text_widget.insert(cursor_position, clipboard_data)
    text_widget.selection_range(cursor_position, cursor_position+len(clipboard_data))


def selectall(text_widget: Union[tk.Entry, ttk.Entry, tk.Text], stringvar: tk.StringVar):
    text_widget.selection_range(0, 'end')
    text_widget.icursor(len(stringvar.get()))
    text_widget.xview_moveto(1.0)

def browseforfile(root: tk.Tk, text_widget: Union[tk.Entry, ttk.Entry], stringvar: tk.StringVar, title : str = "Select File", filetypes: tuple = (("All Files", "*.*"),)):
    fev = stringvar.get()
    if (fev != ''):
        if (fev.find('/') != -1):
            initdir = fev[0:fev.rindex('/')+1]
        else:
            initdir = os.getcwd()
    else:
        initdir = os.getcwd()
    if (system() == "Linux"):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        winwidth = 640
        winheight = 480
        center_x = int((screen_width/2) - (winwidth/2))
        center_y = int((screen_height/2) - (winheight/2))
        thread_resize = Thread(target=_resizewindow, kwargs={"windowname": title, "mvarg": (0,center_x,center_y,winwidth,winheight)})
        thread_resize.start()  
    file_path = fdlg.askopenfilename(initialdir=initdir, title=title, filetypes=filetypes)
    if (system() == "Windows"):
        file_path = file_path.replace("/", "\\")
    if (file_path not in ['', tuple()]):
        stringvar.set(file_path)
    text_widget.selection_range(0, 'end')
    text_widget.icursor(len(stringvar.get()))
    text_widget.xview_moveto(1.0)
    text_widget.focus_set()