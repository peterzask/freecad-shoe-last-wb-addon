import os
import sys
import pwd
import FreeCADGui as Gui
import FreeCAD as App

# snap overrides $HOME to the snap version dir; pwd gives the real home
_real_home = pwd.getpwuid(os.getuid()).pw_dir


class ShoelastWorkbench(Gui.Workbench):
    MenuText = "Shoelast WB"
    ToolTip  = "Workbench to make 3D printable shoe lasts from foot measurements"
    Icon     = ""   # set below

    def Initialize(self):
        # Compute paths here — exec() globals are gone by the time Initialize() runs.
        # os and sys are reliable; user-defined module-level names are not.
        import pwd as _pwd
        real_home = _pwd.getpwuid(os.getuid()).pw_dir
        wb = next(
            (p for p in sys.path if os.path.isdir(os.path.join(p, "shoelast_wb"))),
            os.path.join(real_home, "snap", "freecad", "common", "Mod", "freecad.shoe_last_wb")
        )
        icon_dir = os.path.join(wb, "shoelast_wb", "resources")
        macros   = os.path.join(real_home, "00_ausr", "work", "freecad", "macros")

        if macros not in sys.path:
            sys.path.insert(0, macros)

        import runpy

        class _Cmd:
            def __init__(self, label, tip, script):
                self._label  = label
                self._tip    = tip
                self._script = script
                self._icon   = os.path.join(icon_dir, "shoelast_wb.svg")
            def GetResources(self):
                return {"Pixmap":   self._icon,
                        "MenuText": self._label,
                        "ToolTip":  self._tip}
            def Activated(self):
                runpy.run_path(os.path.join(macros, self._script))
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


# Icon set after class — class body cannot see module-level vars under exec()
ShoelastWorkbench.Icon = os.path.join(
    next((p for p in sys.path if os.path.isdir(os.path.join(p, "shoelast_wb"))),
         os.path.join(_real_home, "snap", "freecad", "common", "Mod", "freecad.shoe_last_wb")),
    "shoelast_wb", "resources", "shoelast_wb.svg"
)
Gui.addWorkbench(ShoelastWorkbench())
