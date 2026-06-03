#!/bin/bash
# Copy workbench files to FreeCAD Mod directory.
# Run after editing InitGui.py or commands.py; FreeCAD must be restarted to pick up changes.
MOD_DIR="$HOME/snap/freecad/common/Mod/freecad.shoe_last_wb"
SRC_DIR="$(dirname "$(realpath "$0")")"
rsync -av --exclude='deploy.sh' --exclude='*.pyc' --exclude='__pycache__' "$SRC_DIR/" "$MOD_DIR/"
echo "Deployed to $MOD_DIR"
