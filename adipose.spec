# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['adipose/cli/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('adipose/templates', 'adipose/templates'),
        ('README.md', '.'),
        ('DOCUMENTATION.md', '.'),
    ],
    hiddenimports=[
        'adipose.cli.main',
        'adipose.core.generator',
        'adipose.schemas.config',
        'adipose.utils.helpers',
        'adipose.generators.backend.django_generator',
        'adipose.generators.backend.express_generator',
        'adipose.generators.backend.dotnet_generator',
        'adipose.generators.backend.springboot_generator',
        'adipose.generators.backend.laravel_generator',
        'adipose.generators.frontend.javascript_generator',
        'adipose.generators.frontend.flutter_generator',
        'adipose.generators.frontend.swift_generator',
        'adipose.generators.frontend.kotlin_generator',
        'adipose.generators.frontend.avaloniaui_generator',
        'pydantic',
        'pydantic_core',
        'yaml',
        'jinja2',
        'click',
        'jsonschema',
        'inflection',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='adipose',
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
