# Copyright (C) 2023 by adriano22jr.
# Code Version: 1.1
# Author = adriano22jr


from tkinter import filedialog
from sys import platform
from data_reader import *
from button_loader import *
import customtkinter
import os, sys, pathlib

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

# https://stackoverflow.com/questions/70405069/pyinstaller-executable-saves-files-to-temp-folder
def get_script_folder():
    # path of main .py or .exe when converted with pyinstaller
    if getattr(sys, 'frozen', False):
        script_path = os.path.dirname(sys.executable)
    else:
        script_path = os.path.dirname(
            os.path.abspath(sys.modules['__main__'].__file__)
        )
    return pathlib.Path(script_path)

class Remover(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.__width = 475
        self.__height = 300
        x, y = self.calculate_coords(self.__width, self.__height)
        self.geometry(f"{self.__width}x{self.__height}+{int(x)}+{int(y)}")
        
        self.iconbitmap(get_script_folder() / "data/icon.ico")
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(get_script_folder() / "data/icon.ico"))
            
        self.title("Remove")
        self.grab_set()
        self.resizable(width = False, height = False)
        
        self.__reader = DataReader()
        self.create_frame()

    def calculate_coords(self, width, height):
        x_offset = (self.winfo_screenwidth() / 2) - (width / 2)
        y_offset = (self.winfo_screenheight() / 2) - (height / 2)
        
        return x_offset, y_offset
        
    def create_frame(self):
        self.__frame = customtkinter.CTkScrollableFrame(self, corner_radius = 5)        
        self.__frame.pack(padx = 10, pady = 10, expand = True, fill = "both")
        
        self.__label = customtkinter.CTkLabel(self.__frame, text = "Click the button you want to remove:")
        self.__label.grid(row = 0, column = 0, padx = 10, sticky = "w")
        
        self.__button_loader = ButtonLoader(self.__frame, None)
        self.__buttons = []
        self.load_buttons()
        
    def load_buttons(self):
        for btn in self.__buttons:
            btn.destroy()        
        
        buttons = self.__button_loader.load_buttons()
        
        for button in buttons:
            button.configure(command = lambda button = button: self.remove(button))
        
        row = 1
        col = 0
        for btn in buttons:      
            btn.grid(row = row, column = col, padx = 10, pady = 10)      
            if col != 1: col += 1
            else: 
                col = 0
                row += 1          
            
        self.__buttons = buttons
        
    def remove(self, button):
        couples = self.__reader.load()
        
        for pos, couple in enumerate(couples):
            if couple[0] == button.cget("text"):
                path = get_script_folder() / "audio" + str(couple[1])
                os.remove(path)
                del couples[pos]
                
        self.__reader.save(couples)
        self.master.load_buttons()
        self.destroy()    