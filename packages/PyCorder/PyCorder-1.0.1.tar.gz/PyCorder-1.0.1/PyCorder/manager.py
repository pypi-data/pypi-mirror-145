import subprocess, platform, pkgutil

packages = [package.name for package in pkgutil.iter_modules()]
system = platform.system()

def install():
    if system == 'Windows' and not 'pipwin' in packages:
        subprocess.call(['pip', 'install', 'pipwin'])

    if not 'pyaudio' in packages:
        if system == 'Windows':
            return subprocess.call(['pipwin', 'install', 'pyaudio'])
        elif system == 'Darwin':
            subprocess.call(['brew', 'install', 'portaudio'])
            return subprocess.call(['pip', 'install', 'pyaudio'])
        elif system == 'Linux':
            subprocess.call(['sudo', 'apt-get', 'portaudio19-dev'])
            return subprocess.call(['pip', 'install', 'pyaudio'])
        else:
            raise RuntimeError(f'Unable to install pyaudio: platform {system!r} is not defined.')
    return None