# -*- mode: python -*-

block_cipher = None


a = Analysis(['application.py'],
             pathex=['.\\'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt5', 'pydoc', 'pytest', 'distutils', 'setuptools', ],
             win_no_prefer_redirects=False,
             win_private_assemblies=True,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Orchestrion',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True,
		  icon="icon.ico")
