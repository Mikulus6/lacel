#!/usr/bin/env python3

from os import walk
from os.path import join
from setuptools import find_packages,\
                       setup

directory = "lacel"
version_file = join(directory, "version.txt")

with open(version_file, 'r') as f:
    version = f.read()

# include entire directory
datafiles = [(d, [join(d, f) for f in files])
             for d, folders, files in walk(directory)]

optional_packages = {'Pillow': ['Pillow>=9.2.0']}

setup(name="lacel",
      version=version,
      description="Łacel (Łoś assets conversions external library) is a library (package) written in Python 3"
                  "for assets and files conversions from the video game \"Po prostu Łoś\".\n"
                  "For further information read file \"README.md\".",
      author="Mikołaj Walc \"Mikulus\"",
      author_email="mikulus6@gmail.com",
      url="https://github.com/Mikulus6/lacel",
      packages=find_packages(where=directory),
      package_dir={"": directory},
      include_package_data=True,
      data_files=datafiles,
      extras_require=optional_packages
      )
