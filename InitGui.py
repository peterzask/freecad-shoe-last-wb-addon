import os
import sys
from pathlib import Path
import FreeCADGui as Gui
import FreeCAD as App

# Workbench root: the directory containing this InitGui.py.
# Using __file__ avoids the sys.path search and works on all platforms.
_wb_dir = os.path.dirname(os.path.abspath(__file__))
_icon   = os.path.join(_wb_dir, "shoelast_wb", "resources", "shoelast_wb.svg")


def _find_macros():
    """Return the macros directory path, or None if not found.
    Search order:
      1. SHOELAST_MACROS env var (user sets this on Windows or non-standard installs)
      2. macros/ subfolder bundled inside the workbench dir
      3. Workbench dir itself (flat layout: all .py files alongside InitGui.py)
      4. Linux dev path ~/00_ausr/work/freecad/macros (fallback for the dev machine)
    """
    env = os.environ.get("SHOELAST_MACROS", "").strip()
    if env and os.path.isdir(env):
        return env
    bundled = os.path.join(_wb_dir, "macros")
    if os.path.isdir(bundled):
        return bundled
    if os.path.isfile(os.path.join(_wb_dir, "uv_0.py")):
        return _wb_dir
    dev = os.path.join(str(Path.home()), "00_ausr", "work", "freecad", "macros")
    if os.path.isdir(dev):
        return dev
    return None


class ShoelastWorkbench(Gui.Workbench):
    MenuText = "Shoelast WB"
    ToolTip  = "Workbench to make 3D printable shoe lasts from foot measurements"
    Icon     = _icon

    def Initialize(self):
        macros = _find_macros()
        if not macros:
            App.Console.PrintError(
                "ShoelastWB: macros directory not found.\n"
                "  Option A: set the SHOELAST_MACROS environment variable to the macros folder.\n"
                "  Option B: place the macros folder inside the workbench directory as 'macros/'.\n"
            )
            return

        if macros not in sys.path:
            sys.path.insert(0, macros)

        import runpy

        class _Cmd:
            def __init__(self, label, tip, script):
                self._label  = label
                self._tip    = tip
                self._script = os.path.join(macros, script)
                self._icon   = _icon
            def GetResources(self):
                return {"Pixmap":   self._icon,
                        "MenuText": self._label,
                        "ToolTip":  self._tip}
            def Activated(self):
                runpy.run_path(self._script)
            def IsActive(self):
                return App.ActiveDocument is not None

        Gui.addCommand("ShoelastWB_GenerateLast",
                       _Cmd("Generate Last",
                            "Run full pipeline: geometry → NURBS surface → export STL/STEP",
                            "uv_0.py"))
        Gui.addCommand("ShoelastWB_ShowWireframe",
                       _Cmd("Show Wireframe",
                            "Display control-point wireframe grid",
                            "make_wireframe.py"))
        Gui.addCommand("ShoelastWB_Analyze",
                       _Cmd("Analyze Surface",
                            "Print planarity, shear, aspect, and curvature metrics",
                            "analyze_uv_matrix.py"))

        cmd_list = ["ShoelastWB_GenerateLast",
                    "ShoelastWB_ShowWireframe",
                    "ShoelastWB_Analyze"]
        self.appendToolbar("Shoelast", cmd_list)
        self.appendMenu("Shoelast WB", cmd_list)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(ShoelastWorkbench())
