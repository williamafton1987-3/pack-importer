# Building Pack Importer yourself (.exe)

This guide walks through building a standalone Windows executable from `app.py` using PyInstaller.

## Disclaimers

This will create a folder named `temp` in the directory it’s run from.

The folder gets deleted afterward, but it may cause issues if a folder named `temp` already exists there. It’s recommended to keep the `.exe` in its own dedicated folder.

## Requirements

- Windows 10/11
- Python 3.x installed from [python.org](https://www.python.org/downloads/) (check **“Add Python to PATH”** during install)

No third-party pip packages are required to *run* `app.py` — it only uses Python’s standard library (`tkinter`, `os`, `uuid`, `time`, `zipfile`, `threading`, `shutil`, `json`). The only real dependency is `pyinstaller`, which is needed to build the `.exe`.

## Building from source

If you already have Python and pip installed:

```bat
pip install -r requirements.txt
pyinstaller app.py --onefile --windowed
```

The built `.exe` will be in the `dist` folder.

## Optional

- Add a custom icon:
  
  ```bat
  pyinstaller app.py --onefile --windowed --icon=icon.ico --name PackImporter
  ```
- Test the `.exe` on a machine without Python installed to confirm it runs standalone.
- Windows SmartScreen/Defender may flag unsigned PyInstaller builds as unrecognized — this is a common false positive for indie/open-source tools, not a sign of malware.

## Clean up (optional)

PyInstaller generates a `build/` folder and a `.spec` file alongside `dist/`. These can be deleted after building if you only need the final `.exe`.
