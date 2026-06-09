## Installation

---

## Linux Installation (FreeCAD via Snap)

Two separate GitHub repos are needed: the workbench addon and the macros.

### Step 1 - Find the FreeCAD user Mod folder

Open FreeCAD, go to View -> Panels -> Python Console, and run:

    import FreeCAD; print(FreeCAD.getUserAppDataDir())

For the snap package this is typically:

    /home/yourname/snap/freecad/common/

The Mod folder is inside that: .../snap/freecad/common/Mod/
Create it if it does not exist:

    mkdir -p ~/snap/freecad/common/Mod

### Step 2 - Install the workbench addon

    cd ~/snap/freecad/common/Mod
    git clone https://github.com/peterzask/freecad-shoe-last-wb-addon.git shoe-last-wb

Or download the zip, extract the inner folder (GitHub adds an extra wrapper), and place it as:

    ~/snap/freecad/common/Mod/shoe-last-wb/InitGui.py   <-- must be at this level

### Step 3 - Install the macros

    cd ~/snap/freecad/common/Mod/shoe-last-wb
    mkdir macros
    cd macros
    git clone https://github.com/peterzask/freecad-shoe-last-wb.git .

Or copy your working macros directory:

    cp /path/to/macros/*.py ~/snap/freecad/common/Mod/shoe-last-wb/macros/

### Step 4 - Deploy script (dev workflow)

If you are actively editing the macros, the deploy.sh script in the addon repo
keeps the Mod copy in sync with your working directory:

    cd /path/to/freecad-shoe-last-wb-addon
    ./deploy.sh

Run after editing InitGui.py or commands.py; restart FreeCAD to pick up changes.
The macros themselves are run directly from disk so edits take effect immediately.

### Step 5 - Run

1. Restart FreeCAD
2. Select "Shoelast WB" from the workbench dropdown
3. Open or create a FreeCAD document (File -> New) -- required before running
4. Click "Generate Last" in the Shoelast toolbar

---

## Windows Installation (FreeCAD 1.1)

Two separate GitHub repos are needed: the workbench addon and the macros.

---

### Step 1 - Find the FreeCAD user Mod folder

Open FreeCAD, go to View -> Panels -> Python Console, and run:

    import FreeCAD; print(FreeCAD.getUserAppDataDir())

The output will be something like:

    C:\Users\yourname\AppData\Roaming\FreeCAD\v1-1\

The Mod folder is inside that: ...\v1-1\Mod\
Create the Mod folder if it does not exist.

---

### Step 2 - Download and install the workbench addon

Download:  https://github.com/peterzask/freecad-shoe-last-wb-addon/archive/refs/heads/master.zip

When you extract the zip, GitHub creates an extra wrapper folder inside:

    freecad-shoe-last-wb-addon-master\
        freecad-shoe-last-wb-addon-master\   <-- actual files are here
            InitGui.py
            package.xml
            shoelast_wb\

You want the INNER folder (the one containing InitGui.py).
Move or rename it to shoe-last-wb and place it in the Mod folder:

    ...\v1-1\Mod\shoe-last-wb\
        InitGui.py
        package.xml
        shoelast_wb\

In Command Prompt, from inside the outer extracted folder:

    move freecad-shoe-last-wb-addon-master "C:\Users\yourname\AppData\Roaming\FreeCAD\v1-1\Mod\shoe-last-wb"

---

### Step 3 - Download and install the macros

Download:  https://github.com/peterzask/freecad-shoe-last-wb/archive/refs/heads/master.zip

NOTE: this is a different repo from the addon above (no "-addon" in the name).

Extract the zip. Again GitHub wraps it:

    freecad-shoe-last-wb-master\
        freecad-shoe-last-wb-master\   <-- actual files are here
            uv_0.py
            xs_base.py
            last_insole.py
            ... (20+ .py files)

Create a macros subfolder inside the addon and copy the .py files into it:

    mkdir "C:\Users\yourname\AppData\Roaming\FreeCAD\v1-1\Mod\shoe-last-wb\macros"
    copy "path\to\freecad-shoe-last-wb-master\freecad-shoe-last-wb-master\*.py" "C:\Users\yourname\AppData\Roaming\FreeCAD\v1-1\Mod\shoe-last-wb\macros\"

---

### Step 4 - Final folder structure

    v1-1\Mod\shoe-last-wb\
        InitGui.py
        package.xml
        shoelast_wb\
            __init__.py
            commands.py
            resources\
                shoelast_wb.svg
        macros\
            uv_0.py
            xs_base.py
            last_insole.py
            last_profile.py
            helper_funcs.py
            xs_0.py ... xs_8.py
            ... (all macro .py files)

---

### Step 5 - Run

1. Restart FreeCAD
2. Select "Shoelast WB" from the workbench dropdown
3. Open or create a FreeCAD document (File -> New) -- required before running
4. Click "Generate Last" in the Shoelast toolbar
