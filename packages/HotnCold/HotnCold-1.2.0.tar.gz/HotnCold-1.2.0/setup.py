#!/usr/bin/env python
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

VERSION = '1.2.0'

setup(name='HotnCold',
      version=VERSION,
      description="a Hot and Cold Game",
      long_description=README,
      author='Samic',
      author_email='hotncold@samic.org',
      url='https://gitlab.com/samic130/hotncold/',
      license='GPLv3',
      packages=["HotnCold"],
      classifiers =[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",],
      include_package_data=True,
      zip_safe=False,
      install_requires=['matplotlib'],
      entry_points={'console_scripts': [
          'HotnCold = HotnCold.HotnCold:main',
          'hotncold = HotnCold.HotnCold:main',]})
