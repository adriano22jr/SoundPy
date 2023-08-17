# Copyright (C) 2023 by adriano22jr.
# Code Version: 1.0
# Author = adriano22jr


from data_reader import *
import customtkinter

class ButtonLoader():
    def __init__(self, master, mixer) -> None:
        self.__reader = DataReader()
        self.__mixer = mixer
        self.__root = master
        
    def load_buttons(self):
        data = self.__reader.load()
        buttons = []
        for entry in data:
            buttons.append(self.create_button(entry[0]))
        
        return buttons

    def create_button(self, name):
        button = customtkinter.CTkButton(self.__root, text = name, width = 170)
        button.configure(command = lambda button = button: self.__root.play(self.__mixer, button))
        return button