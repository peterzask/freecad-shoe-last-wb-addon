import FreeCADGui as Gui
import FreeCAD as App


class ShoelastWorkbench(Gui.Workbench):
    MenuText = "Shoelast WB"
    ToolTip  = "Workbench to make 3D printable shoe lasts from foot measurements"
    Icon     = ""  # set in Initialize() - module globals unreliable under FreeCAD exec()

    def Initialize(self):
        import os, sys
        from pathlib import Path

        # Locate workbench root. __file__ is not set by FreeCAD's exec() on Windows,
        # so fall back to searching sys.path for the dir that contains shoelast_wb/.
        try:
            wb_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            wb_dir = next(
                (p for p in sys.path if os.path.isdir(os.path.join(p, "shoelast_wb"))),
                ""
            )

        icon = os.path.join(wb_dir, "shoelast_wb", "resources", "shoelast_wb.svg")
        self.Icon = icon

        # Locate macros directory.
        env = os.environ.get("SHOELAST_MACROS", "").strip()
        if env and os.path.isdir(env):
            macros = env
        elif os.path.isdir(os.path.join(wb_dir, "macros")):
            macros = os.path.join(wb_dir, "macros")
        elif os.path.isfile(os.path.join(wb_dir, "uv_0.py")):
            macros = wb_dir
        else:
            dev = os.path.join(str(Path.home()), "00_ausr", "work", "freecad", "macros")
            macros = dev if os.path.isdir(dev) else None

        if not macros:
            App.Console.PrintError(
                "ShoelastWB: macros directory not found.\n"
                "  Option A: set SHOELAST_MACROS env var to the macros folder path.\n"
                "  Option B: place macros folder inside the workbench dir as 'macros/'.\n"
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
                self._icon   = icon
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
                            "Run full pipeline: geometry -> NURBS surface -> export STL/STEP",
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
