"""Render the simple week-1 diagram and keep legacy artifact names in sync."""
from pathlib import Path
from shutil import copyfile
from runpy import run_path

ROOT = Path(__file__).resolve().parents[1]
run_path(str(ROOT / "scripts" / "render-simple-architecture.py"), run_name="__main__")
diagrams = ROOT / "docs" / "diagrams"
for extension in ("png", "svg", "mmd"):
    copyfile(diagrams / f"architecture-week1-simple.{extension}", diagrams / f"architecture.{extension}")
print("Synchronized architecture.png/.svg/.mmd with the monochrome diagram")
