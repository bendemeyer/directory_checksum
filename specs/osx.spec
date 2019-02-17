# -*- mode: python -*-

block_cipher = None


a = Analysis(['../app.py'],
             pathex=['.'],
             binaries=[],
             datas=[('../resources/running_32.gif', 'resources'), ('../resources/empty_32.gif', 'resources')],
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
          [],
          exclude_binaries=True,
          name='DirectoryChecksum',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='resources/dc.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='app')
app = BUNDLE(coll,
             name='DirectoryChecksum.app',
             icon='resources/dc.icns',
             bundle_identifier=None)
