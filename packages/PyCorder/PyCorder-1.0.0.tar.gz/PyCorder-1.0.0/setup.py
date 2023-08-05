from setuptools import setup

import subprocess, pkgutil, platform, sys

IS_64_BIT = sys.maxsize > 2 ** 32

if platform.system() == 'Windows' and not 'wheel' in [pkg.name for pkg in pkgutil.iter_modules()]:
    subprocess.call(['pip3', 'install', 'wheel'])

if platform.system() == 'Windows':
    subprocess.call(['pip3', 'install', f'PyCorder\\builds\\{"PyAudio-0.2.11-cp310-cp310-win_amd64.whl" if IS_64_BIT else "PyAudio-0.2.11-cp310-cp310-win32.whl"}'])
elif platform.system() == 'Linux':
    subprocess.call(['sudo', 'apt-get', 'install', 'portaudio19-dev'])
    subprocess.call(['pip3', 'install', 'pyaudio'])
elif platform.system() == 'Darwin':
    subprocess.call(['brew', 'install', 'portaudio'])
    subprocess.call(['pip3', 'install', 'pyaudio'])
else:
    raise RuntimeError(f'Platform {platform.system()} is not defined.')

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

f.close()

from PyCorder import __version__

setup(
    name='PyCorder',
    version=__version__,
    description='A audio recorder for python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='LUA9',
    maintainer='LUA9',
    packages=['PyCorder'],
)