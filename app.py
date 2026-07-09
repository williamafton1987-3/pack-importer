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
appdata = os.path.expandvars(r"%appdata%")
defaultcmpath = r"Minecraft Bedrock\Users\Shared\games\com.mojang"
commojangpath = os.path.join(appdata, defaultcmpath)
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
ttk.Button(frame, text="select packs to import",command=choosepacks).grid(column=1, row=4)
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
ttk.Button(frame, text="select com.mojang", command=setcommojangpath).grid(column=1, row=2)
def cprint(text: str):
    oldoutput = output.get()
    output.set(f"{oldoutput}\n{text}")

def findmanifest(folderpath: str):
    for root , _, files in os.walk(folderpath):
        for file in files:
            if file == "manifest.json":
                return os.path.join(root, file), root

def importpacks():
    output.set("\r")
    startedziptime = time.time()
    try:
        for zipname in selectedpacks:
            with zipfile.ZipFile(zipname) as zf:
                setuuid = uuid.uuid4()
                puuid = os.path.join("temp", str(setuuid))
                starttime = time.time()
                cprint(f"started importing {os.path.basename(zipname)}")
                zf.extractall(puuid)
                manifest, manifestdir = findmanifest(puuid)
                with open(manifest, "r") as manifestjson:
                    manifest = json.load(manifestjson)
                packtype = False
                for i in manifest.get("modules", []):
                    mtype = i.get("type")
                    if mtype in ("data", "resources", "skin_pack", "world_template"):
                        packtype = mtype

                if packtype:
                    behavior_packdir = os.path.join(commojangpath, "behavior_packs")
                    resource_packdir = os.path.join(commojangpath, "resource_packs")
                    skin_packdir = os.path.join(commojangpath, "skin_packs")
                    world_templatesdir = os.path.join(commojangpath, "world_templates")
                    if packtype == "data":
                        cprint("behavior pack detected")
                        dest = os.path.join(behavior_packdir, str(setuuid))
                        shutil.move(manifestdir, dest)
                    elif packtype == "resources":
                        cprint("resource pack detected")
                        dest = os.path.join(resource_packdir, str(setuuid))
                        shutil.move(manifestdir, dest)
                    elif packtype == "skin_pack":
                        cprint("skin pack detected")
                        dest = os.path.join(skin_packdir, str(setuuid))
                        shutil.move(manifestdir, dest)
                    elif packtype == "world_template":
                        cprint("world template detected")
                        dest = os.path.join(world_templatesdir, str(setuuid))
                        shutil.move(manifestdir, dest)
                    if os.path.exists(puuid):
                        shutil.rmtree(puuid)

                print(f"{puuid}\n {os.path.basename(zipname)} finished in {abs(starttime - time.time())}")
                cprint(f"{os.path.basename(zipname)} finished in {abs(starttime - time.time()):.3f} seconds")
        selectedpacks.clear()
        selpacksui.set("")
        cprint(f"finished in {abs(startedziptime - time.time()):.2f} seconds")
    except Exception as e:
        cprint(str(e))
        print(e)

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