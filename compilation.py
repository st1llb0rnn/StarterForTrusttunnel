import PyInstaller.__main__

PyInstaller.__main__.run([
    "--onefile",
    "main.py",
    "get_localizations.py",
    "for_create_localization_file.py",
    "--name",
    "StarterForTrusttunnel"
])
