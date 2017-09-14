from cx_Freeze import setup, Executable

base = None


executables = [Executable("ps4igrice.py", base=base)]

setup(
    name = "PS4IgriceKP",
    version = "0.1",
    description = 'Scrape KP and fill in GSheets with the data',
    executables = executables
)