from cx_Freeze import setup, Executable

script_file = "Copy_Images.py"
base = "Win32GUI"

executables = [Executable(script_file, base=base)]

setup(name="CopyDaoiImg",
      version="0.1",
      description="CopyDaoiImg GUI application",
      executables=executables,
      )
