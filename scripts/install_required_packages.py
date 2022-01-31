from pip._internal import main as pipmain
import os
import sys
import site
sys.path.append(site.getusersitepackages())
import subprocess
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

print("\nStarting to install packages, if not already installedd...\n")

try:
    import requests
except ModuleNotFoundError:
    subprocess.call([python_exe, "-m", "pip", "install", "requests"])
try:
    import zipfile36
except ModuleNotFoundError:
    subprocess.call([python_exe, "-m", "pip", "install", "zipfile36"])
try:
    import remotezip
except ModuleNotFoundError:
    subprocess.call([python_exe, "-m", "pip", "install", "remotezip"])

print("\n\nAll packages installed! Starting to download tiles...\n")