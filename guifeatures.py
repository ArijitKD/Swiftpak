import tkinter as tk
import tkinter.ttk as ttk
from typing import Union

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