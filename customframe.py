# Copyright (C) 2023 by adriano22jr.
# Code Version: 1.0
# Author = adriano22jr


from typing import Literal, Optional, Tuple, Union
from typing_extensions import Literal
from customtkinter.windows.widgets.font import CTkFont
from button_loader import *
from uploader import *
import customtkinter, pygame
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

class PlayableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, scrollbar_fg_color: str | Tuple[str, str] | None = None, scrollbar_button_color: str | Tuple[str, str] | None = None, scrollbar_button_hover_color: str | Tuple[str, str] | None = None, label_fg_color: str | Tuple[str, str] | None = None, label_text_color: str | Tuple[str, str] | None = None, label_text: str = "", label_font: tuple | CTkFont | None = None, label_anchor: str = "center", orientation: Literal['vertical', 'horizontal'] = "vertical"):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, scrollbar_fg_color, scrollbar_button_color, scrollbar_button_hover_color, label_fg_color, label_text_color, label_text, label_font, label_anchor, orientation)
        self.__reader = DataReader()
        
    def play(self, mixer, button):
        sound_to_play = resource_path(str(ROOT_DIR) + "\\audio\\" + self.__reader.find_sound(button.cget("text")))
        mixer.music.load(sound_to_play)
        mixer.music.play()