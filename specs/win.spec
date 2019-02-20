# -*- mode: python -*-
import os
app_dir = os.path.abspath('.')

block_cipher = None

a = Analysis(['..\\app.py'],
             pathex=[app_dir],
             binaries=[],
             datas=[('..\\resources\\running_32.gif', 'resources'), ('..\\resources\\empty_32.gif', 'resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='DirectoryChecksum',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='resources\\dc.ico')
