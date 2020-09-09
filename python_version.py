#!/usr/bin/env python3
#encoding=utf-8

#execute command:
# /Applications/FontForge.app/Contents/Resources/opt/local/bin/fontforge bmp.py--input Regular.sfdir --output folder

import subprocess
import sys
#import pip

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def pip_install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def cli():
    print(sys.version)
    #install('pillow')

if __name__ == "__main__":
    cli()
