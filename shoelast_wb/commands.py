import os
import sys
import runpy
import FreeCAD as App

_wb_dir     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MACROS_PATH = os.path.join(os.path.dirname(_wb_dir), "macros")
ICON_PATH   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")


def _run(script_name):
    if MACROS_PATH not in sys.path:
        sys.path.insert(0, MACROS_PATH)
    runpy.run_path(os.path.join(MACROS_PATH, script_name))


class CmdGenerateLast:
    def GetResources(self):
        return {
            "Pixmap":   os.path.join(ICON_PATH, "shoelast_wb.svg"),
            "MenuText": "Generate Last",
            "ToolTip":  "Run full pipeline: geometry → NURBS surface → export STL/STEP",
        }

    def Activated(self):
        _run("uv_0.py")

    def IsActive(self):
        return App.ActiveDocument is not None


class CmdShowWireframe:
    def GetResources(self):
        return {
            "Pixmap":   os.path.join(ICON_PATH, "shoelast_wb.svg"),
            "MenuText": "Show Wireframe",
            "ToolTip":  "Display control-point wireframe grid",
        }

    def Activated(self):
        _run("make_wireframe.py")

    def IsActive(self):
        return App.ActiveDocument is not None


class CmdAnalyzeSurface:
    def GetResources(self):
        return {
            "Pixmap":   os.path.join(ICON_PATH, "shoelast_wb.svg"),
            "MenuText": "Analyze Surface",
            "ToolTip":  "Print planarity, shear, aspect, and curvature metrics",
        }

    def Activated(self):
        _run("analyze_uv_matrix.py")

    def IsActive(self):
        return App.ActiveDocument is not None
