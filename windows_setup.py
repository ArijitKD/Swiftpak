import sys
from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need find tuning
build_exe_options = {"packages": ["tkinter", "ctypes", "os", "sys", "numpy"], "include_files": ["assets\\"]}

setup  (name = "Swiftpak",
        version = "pre-alpha",
        description = "Swiftpak - A File Compression Utility Software",
        options = {"build_exe": build_exe_options},
        executables = [Executable(script="swiftpak.py", base="Win32GUI", icon="assets\\swiftpak-icon_32X32.ico", copyright = "Copyright 2023 Team CyberTron (GPLv3.0)")])