# Copyright (C) 2023 by adriano22jr.
# Code Version: 1.1
# Author = adriano22jr


from tkinter import filedialog
from sys import platform
from data_reader import *
from PIL import ImageTk, Image
import customtkinter
import os, sys, pathlib, shutil, ntpath

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

class Uploader(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.__width = 400
        self.__height = 150
        x, y = self.calculate_coords(self.__width, self.__height)
        self.geometry(f"{self.__width}x{self.__height}+{int(x)}+{int(y)}")
        
        self.iconbitmap(get_script_folder() / "data/icon.ico")
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(get_script_folder() / "/data/icon.ico"))
            
        self.title("Upload")
        self.grab_set()
        self.resizable(width = False, height = False)
        
        self.__input_path = None
        self.__input_sound_name = None
        self.__input_label = None 
        self.__reader = DataReader()
        self.create_frame()

    def calculate_coords(self, width, height):
        x_offset = (self.winfo_screenwidth() / 2) - (width / 2)
        y_offset = (self.winfo_screenheight() / 2) - (height / 2)
        
        return x_offset, y_offset
        
    def create_frame(self):
        self.__frame = customtkinter.CTkFrame(self, corner_radius = 5)        
        self.__frame.pack(padx = 10, pady = 10, expand = True, fill = "both")
        
        img = Image.open(get_script_folder() / "data/folder.png")
        img = img.resize((25, 25))
        btn_icon = ImageTk.PhotoImage(img)
        open_dialog = customtkinter.CTkButton(self.__frame, image = btn_icon, text = "", command = self.load, width = 30, height = 30)        
        open_dialog.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "w")
        
        self.__entry = customtkinter.CTkEntry(self.__frame, placeholder_text = "Insert sound name here!", width = 314)
        self.__entry.grid(row = 0, column = 0, padx = 56, pady = 10)
        
        input_guide = customtkinter.CTkLabel(self.__frame, text = "Selected sound:", font = customtkinter.CTkFont(size = 12))
        input_guide.grid(row = 1, column = 0, padx = 10, sticky = "w")
         
        save_button = customtkinter.CTkButton(self.__frame, text = "Save", width = 100, command = self.save)
        save_button.grid(row = 2, column = 0, padx = 140, pady = 10, sticky = "w")
    
    def load(self):
        self.__input_path = filedialog.askopenfilename(filetypes = [("Audio Files (.mp3, .wav)", ".mp3"), ("Audio Files (.mp3, .wav)", ".wav")])
        
        if self.__input_label is None:
            self.__input_label = customtkinter.CTkLabel(self.__frame, text = ntpath.basename(self.__input_path))
        else:
            self.__input_label.configure(text = ntpath.basename(self.__input_path))    
        self.__input_label.grid(row = 1, column = 0, padx = 100, sticky = "w")
        
    def save(self):
        self.__input_sound_name = self.__entry.get()        
        if self.__input_path is not None and self.__input_sound_name != "":
            shutil.copy(self.__input_path, get_script_folder() / "audio")
            
            filename = ntpath.basename(self.__input_path)
            
            try:
                data = self.__reader.load()
                data.append( (self.__input_sound_name, filename) )
                self.__reader.save(data)
            except:
                self.__reader.save([])
                data = self.__reader.load()
                data.append( (self.__input_sound_name, filename) )
                self.__reader.save(data)
                
            self.master.load_buttons()
            self.destroy()            