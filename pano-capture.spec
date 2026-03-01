# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['pano_capture.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include any data files you need
        # ('configs/', 'configs/'),  # Example: include config directory
    ],
    hiddenimports=[
        # Force include modules that PyInstaller might miss
        'pygame',
        'keyboard',
        'mss',
        'mss.tools',
        'screenshot',
        'screenshot.built_in',
        'screenshot.external_app',
        'screenshot.factory',
        'control',
        'core',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude test modules from the build
        'tests',
        'pytest',
        'pytest_mock',
        'pytest_cov',
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
    name='pano-capture',
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