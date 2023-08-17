# Copyright (C) 2023 by adriano22jr.
# Code Version: 1.0
# Author = adriano22jr


from typing import Optional, Tuple, Union
from button_loader import *
from uploader import *
from customframe import *
import os, sys, pathlib
import customtkinter, pygame

ROOT_DIR = pathlib.Path(os.path.dirname(sys.modules['__main__'].__file__)).resolve()

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PySound(customtkinter.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        self.__width = 800
        self.__height = 400
        x, y = self.calculate_coords(self.__width, self.__height)
        self.geometry(f"{self.__width}x{self.__height}+{int(x)}+{int(y)}")
        self.resizable(width = False, height = False)        
        self.iconbitmap(resource_path(str(ROOT_DIR) + "\\data\\icon.ico"))     
        self.title("SoundPy")
        customtkinter.set_appearance_mode("dark")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.__mixer = pygame.mixer        
        self.__mixer.init()
        self.__mixer.music.set_volume(0.5)
        
        self.create_sidebar() 
        self.create_mainframe()
        self.create_volume_frame()
        
    def calculate_coords(self, width, height):
        x_offset = (self.winfo_screenwidth() / 2) - (width / 2)
        y_offset = (self.winfo_screenheight() / 2) - (height / 2)
        
        return x_offset, y_offset
        
    def create_sidebar(self):
        self.__sidebar = customtkinter.CTkFrame(self, width = 200, corner_radius = 0)
        self.__sidebar.grid(row = 0, column = 0, rowspan = 4, sticky = "nsew")
        self.__sidebar.grid_rowconfigure(4, weight=1)
        
        self.__app_name = customtkinter.CTkLabel(self.__sidebar, text = "SoundPy", font = customtkinter.CTkFont(size = 20, weight = "bold"))
        self.__app_name.grid(row = 0, column = 0, padx = 20, pady = 10)
        
        self.__app_versione = customtkinter.CTkLabel(self.__sidebar, text = "v1.0", font = customtkinter.CTkFont(size = 10))
        self.__app_versione.grid(row = 0, column = 0, padx = 25, pady = 10, sticky = "e")

        self.__add_button = customtkinter.CTkButton(self.__sidebar, text = "Add a sound", command = self.add)
        self.__add_button.grid(row = 1, column = 0, padx = 20, pady = 10)  

        self.__appearance_mode_label = customtkinter.CTkLabel(self.__sidebar, text = "Appearance Mode:", anchor = "w")
        self.__appearance_mode_label.grid(row = 5, column = 0, padx = 20)

        self.__appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.__sidebar, values = ["Light", "Dark", "System"], command = self.change_appearance)
        self.__appearance_mode_optionemenu.grid(row = 6, column = 0, padx = 20, pady = 10)
        
        copyright_label = customtkinter.CTkLabel(self.__sidebar, text = "Copyright \u00A9 2023 adriano22jr\nAll rights reserved.\n Follow on github for more!", font = customtkinter.CTkFont(size = 10))
        copyright_label.grid(row = 7, column = 0, padx = 20)
        
    def create_mainframe(self):        
        self.__mainframe = PlayableFrame(self, corner_radius = 5)
        self.__mainframe.grid(row = 0, column = 1, rowspan = 3, padx = 10, pady = 10, sticky = "nsew")
        
        self.__button_loader = ButtonLoader(self.__mainframe, self.__mixer)
        self.__buttons = []
        
        self.load_buttons()
        
    def create_volume_frame(self):
        self.__volume_frame = customtkinter.CTkFrame(self, corner_radius = 10)
        self.__volume_frame.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = "nsew")
        
        self.__volume_label = customtkinter.CTkLabel(self.__volume_frame, text = "Sound Volume:", anchor = "w")
        self.__volume_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")
        
        self.__volume_slider = customtkinter.CTkSlider(self.__volume_frame, from_= 1, to = 100, orientation = "horizontal", width = 200, command = self.change_volume)
        self.__volume_slider.grid(row = 0, column = 1, padx=(10, 10), pady=(10, 10))
        
        self.__volume_progressbar = customtkinter.CTkProgressBar(self.__volume_frame, orientation = "horizontal", width = 200)
        self.__volume_progressbar.grid(row = 0, column = 2, padx=(10, 20), pady=(10, 10))
        
        self.__volume = customtkinter.CTkLabel(self.__volume_frame, text = "50")
        self.__volume.grid(row = 0, column = 3, padx = 10, pady = 10)
  
    def load_buttons(self):
        for btn in self.__buttons:
            btn.destroy()        
        
        buttons = self.__button_loader.load_buttons()
        
        row = 0
        col = 0
        for btn in buttons:      
            btn.grid(row = row, column = col, padx = 10, pady = 10)      
            if col != 2: col += 1
            else: 
                col = 0
                row += 1          
            
        self.__buttons = buttons

    def add(self):
        upl = Uploader(self)     
        
    def change_appearance(self, new_appearance: str):
        customtkinter.set_appearance_mode(new_appearance)
        
    def change_volume(self, *args):
        current = round(self.__volume_slider.get())
        self.__volume.configure(text = current)
        self.__volume_progressbar.set(current/100)
        self.__mixer.music.set_volume(current/100)