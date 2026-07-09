from tkinter import *
from tkinter.ttk import *
from tkinter import ttk, filedialog
import tkinter as tk
import os, uuid, time
import zipfile, threading, shutil
import json

root = Tk()
root.resizable(False, False)
frame = ttk.Frame(root, padding=10)
frame.grid()

selectedpacks = []
selpacksui = tk.StringVar(value="")
commojangpath = fr"{os.path.expandvars(r"%appdata%")}AppData\Roaming\Minecraft Bedrock\Users\Shared\games\com.mojang"
pathforui = tk.StringVar(value=commojangpath)


ttk.Label(frame, textvariable=pathforui).grid(column=1, row=1)
def choosepacks():
    selpacks = filedialog.askopenfilenames(
        title="select packs",
        filetypes=[("packs", ("*.zip", "*.mcpack", "*.mcaddon"))]
    )
    for packpaths in selpacks:
        selectedpacks.append(packpaths)
        selectedpacksforui = selpacksui.get()
        selpacksui.set(f"{selectedpacksforui}\n{os.path.basename(packpaths)}")
ttk.Button(frame, text="select packs to import",command=choosepacks).grid(column=1, row=2)
ttk.Label(frame, textvariable=selpacksui).grid(column=1, row=3)
def setcommojangpath():
    commjng = filedialog.askdirectory(
        mustexist=True,
        title="select a folder",
        initialdir=str(os.path.expandvars(r"%appdata%"))
    )
    if commjng == "":
        return
    global commojangpath
    commojangpath = commjng
    pathforui.set(commjng)
ttk.Button(frame, text="select com.mojang", command=setcommojangpath).grid(column=1, row=4)
def cprint(text: str):
    oldoutput = output.get()
    output.set(f"{oldoutput}\n{text}")

def findmanifest(folderpath: str):
    for root , folders, files in os.walk(folderpath):
        for file in files:
            if file == "manifest.json":
                packname = os.path.dirname(file)
                return os.path.join(root, file), packname

def importpacks():
    output.set("\r")
    startedziptime = time.time()
    for zipname in selectedpacks:
        with zipfile.ZipFile(zipname) as zf:
            puuid = os.path.join("temp", str(uuid.uuid4()))
            starttime = time.time()
            cprint(f"started importing {os.path.basename(zipname)}")
            zf.extractall(puuid)
            manifest, manifestdir = findmanifest(puuid)
            with open(manifest, "r") as manifestjson:
                manifest = json.load(manifestjson)
            packtype = False
            for i in manifest["modules"]:
                if i in ("data", "resource", "skin_pack", "world_template"):
                    packtype = i

            if packtype:
                behavior_packdir = os.path.join(commojangpath, "behavior_packs")
                resource_packdir = os.path.join(commojangpath, "resource_packs")
                skin_packdir = os.path.join(commojangpath, "skin_packs")
                world_templatesdir = os.path.join(commojangpath, "world_templates")
                if packtype == "data":
                    shutil.move(manifestdir, behavior_packdir)
                elif packtype == "resource":
                    shutil.move(manifestdir, resource_packdir)
                elif packtype == "skin_pack":
                    shutil.move(manifestdir, skin_packdir)
                elif packtype == "world_template":
                    shutil.move(manifestdir, world_templatesdir)

            print(f"{puuid}\n {os.path.basename(zipname)} finished in {abs(starttime - time.time())}")
            cprint(f"{os.path.basename(zipname)} finished in {abs(starttime - time.time()):.3f} seconds")
    selectedpacks.clear()
    selpacksui.set("")
    cprint(f"finished in {abs(startedziptime - time.time()):.2f} seconds")

def startimportpacksthread():
    threading.Thread(target=importpacks, daemon=True).start()
ttk.Button(frame, text="import", padding=(20, 10), command=startimportpacksthread).grid(column=1, row=6)
frame.rowconfigure(5, minsize=20)


output = tk.StringVar(value="\r")
ttk.Label(frame, textvariable=output, padding=(15, 0)).grid(column=1, row=7)
frame.columnconfigure(2, minsize=50)
frame.columnconfigure(0, minsize=50)
frame.rowconfigure(0, minsize=20)
frame.rowconfigure(10, minsize=20)
root.mainloop()