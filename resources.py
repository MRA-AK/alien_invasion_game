"""Helpers for locating data files in source and bundled builds."""

from pathlib import Path
import sys


def resource_path(*parts):
    """Return an absolute resource path, including inside PyInstaller."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    base_path = Path(bundle_root) if bundle_root else Path(__file__).resolve().parent
    return base_path.joinpath(*parts)
