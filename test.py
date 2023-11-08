import pathlib


folder = pathlib.Path("audio/")
file = folder / "bonk.wav"
print(file.exists())