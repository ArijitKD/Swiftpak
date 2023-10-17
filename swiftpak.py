import tkinter as tk, tkinter.ttk as ttk, platform, tkinter.font as font

## CONSTANTS
APP_NAME = "Swiftpak" # The default title for Regalter that
                      # will appear on the title bar.
WINDOW_BG_COLOR = '#f6f5f4'
SYSTEM = platform.system()

class GUI:
    def __init__(self):

        # Creating the root window
        self.root_window = tk.Tk()

        self.font = font.Font(family='Arial', size=10)

        if (SYSTEM == "Windows"):
            self.font.configure(size=11)
        if (SYSTEM != "Windows"):
            ttk.Style(self.root_window).theme_use('clam')

        # Screen dimensions
        self.screen_width = self.root_window.winfo_screenwidth()
        self.screen_height = self.root_window.winfo_screenheight()

        # Fixed dimensions of the root window (480x300)
        self.root_winwidth = 480
        self.root_winheight = 300

        # The code fragment below will position the root window at the centre of the screen
        center_x = int((self.screen_width/2) - (self.root_winwidth/2))
        center_y = int((self.screen_height/2) - (self.root_winheight/2))
        self.root_window.geometry(str(self.root_winwidth)+"x"+str(self.root_winheight)+"+"+str(center_x)+"+"+str(center_y))

        # Since the root window has only a few widgets, so it would be better if we disable the maximization
        # of the window. Also, it won't appear great when maximized on displays with higher resolutions.
        self.root_window.resizable(0,0)

        # Setting the default window title
        self.root_window.title(APP_NAME)

        # Set tkinter window background color
        self.root_window.configure(bg=WINDOW_BG_COLOR)

        # When the window-close event is triggered, function close_root_window(self) is executed
        self.root_window.protocol("WM_DELETE_WINDOW", self.close_root_window)

        # Creating the "Choose file:" label with appropriate attributes
        self.choose_file_label = ttk.Label(self.root_window, text = 'Choose file:', font=self.font, background=WINDOW_BG_COLOR)
        self.choose_file_label.place(x=20, y=20)


        self.file_entry = ttk.Entry(self.root_window, textvariable = None, font=self.font, state='normal', width=34)
        if (SYSTEM == "Windows"):
            self.file_entry.configure(width=40)
        self.file_entry.place(x=20, y=45)
        self.file_entry.focus_set()

        style = ttk.Style()
        style.configure('my.TButton', font=self.font)
        self.browse_button = ttk.Button(self.root_window, text="Browse...", style="my.TButton")
        if (SYSTEM == "Windows"):
            self.browse_button.place(x=362, y=42)
        else:
            self.browse_button.place(x=343, y=36)

    def load_settings(self):
        if (SYSTEM == "Windows"):
            pass

    def close_root_window(self):
        self.root_window.destroy()

gui = GUI()
gui.root_window.mainloop()