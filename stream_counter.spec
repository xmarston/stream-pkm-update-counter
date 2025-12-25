# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for stream-counter executable."""
import os
import sys

block_cipher = None

# Determine platform-specific Tesseract path
if sys.platform == 'win32':
    tesseract_src = os.environ.get('TESSERACT_PATH', 'tesseract-win')
    tesseract_dest = 'tesseract'
else:
    tesseract_src = os.environ.get('TESSERACT_PATH', 'tesseract-linux')
    tesseract_dest = 'tesseract'

# Check if Tesseract directory exists
tesseract_datas = []
if os.path.exists(tesseract_src):
    tesseract_datas = [(tesseract_src, tesseract_dest)]

a = Analysis(
    ['entry.py'],
    pathex=[],
    binaries=[],
    datas=tesseract_datas,
    hiddenimports=[
        'pytesseract',
        'cv2',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pytest',
        'pytest_cov',
        '_pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='stream-counter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
