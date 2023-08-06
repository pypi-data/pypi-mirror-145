from __future__ import print_function
from setuptools import setup,find_packages

setup(
    name='auto_rpa',
    version='0.1.38',
    author='zzf',
    author_email='13051732531@163.com',
    description='auto',
    license='MIT',
    url = 'https://github.com/spiderzzf/auto_rpa.git',
    packages = find_packages(),
    install_requires=['pandas','requests','psutil','PyAutoGUI',
                      'pynput','pypiwin32','Pillow','pytesseract'],
)