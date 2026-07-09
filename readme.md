# disclaimers

this will create a folder named temp in the directory its in

the folder gets deleted,but it may break some things if there is already a folder named temp

so i suggest putting the exe into its own folder

# building from source
if you already have pip / python installed
```bat
pip -r .req
pyinstaller app.py --onefile --windowed
```
