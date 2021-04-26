# -*- mode: python ; coding: utf-8 -*-

import platform

block_cipher = None


a = Analysis(['pognlp/pognlp.py'],
             binaries=[],
             datas=[],
             hiddenimports=[
                    'srsly.msgpack.util',
                    'cymem.cymem',
                    'murmurhash.mrmr',
                    'cytoolz.utils',
                    'cytoolz._signatures',
                    'spacy.strings',
                    'spacy.morphology',
                    'spacy.lexeme',
                    'spacy.tokens.underscore',
                    'preshed.maps',
                    'thinc.backends.linalg',
                    'blis',
             ],
             hookspath=['pyinstaller-hooks/'],
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
          name='pognlp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

if platform.system() == "Darwin":
	app = BUNDLE(exe,
		     name='pognlp.app',
		     icon=None,
		     bundle_identifier=None)
