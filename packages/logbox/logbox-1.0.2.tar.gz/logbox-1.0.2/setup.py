# Copyright (C) 2021 Matthias Nadig

from setuptools import setup, find_packages
from setuptools import Extension


with open('README.md', 'r') as f:
    long_description = f.read()

path_package_toplevel = 'src'

ext_module = Extension('logbox._cli._windows',
                       sources=['src/extension/windows.cpp'],)

setup(
    name='logbox',
    version='1.0.2',
    description='Toolbox for terminal output and logging to file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matthias Nadig',
    author_email='matthias.nadig@yahoo.com',
    license='MIT',
    package_dir={'': path_package_toplevel},
    packages=find_packages(where=path_package_toplevel),
    ext_modules=[ext_module],
    install_requires=[],
)
