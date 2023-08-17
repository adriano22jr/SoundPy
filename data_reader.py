# Copyright (C) 2023 by adriano22jr.
# Code Version: 1.0
# Author = adriano22jr


import os, sys, pathlib, pickle

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

class DataReader():
    def __init__(self) -> None:
        pass
    
    def load(self):
        couples = []
        try:
            data = open(resource_path(str(ROOT_DIR) + "\\data\\data.txt"), "rb")
            couples = pickle.load(data)
            data.close()
        except:
            pass
        return couples
    
    def save(self, couples):
        data = open(resource_path(str(ROOT_DIR) + "\\data\\data.txt"), "wb")
        pickle.dump(couples, data)
        data.close()
        
    def find_sound(self, name):
        data = open(resource_path(str(ROOT_DIR) + "\\data\\data.txt"), "rb")
        couples = pickle.load(data)
        data.close()
        
        for entry in couples:
            if entry[0] == name:
                return entry[1]