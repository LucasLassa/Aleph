import os
import sys

name = "aleph"
entry = os.path.join(SPECPATH, "src", "main.py")
icon_png = os.path.join(SPECPATH, "src", "resources", "icon.png")
font_otf = os.path.join(SPECPATH, "src", "resources", "Orange Kid.otf")
datas = [(icon_png, "resources"), (font_otf, "resources")]

a = Analysis(
    [entry],
    pathex=[SPECPATH],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_png if sys.platform == "win32" else None,
)
