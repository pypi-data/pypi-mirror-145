#!/usr/bin/env python
# Licensed under an MIT license - see LICENSE

from setuptools import setup, find_packages
import os
from pathlib import Path
import re


## read __version__
with open(Path(__file__).parent.absolute().joinpath('divtel/version.py')) as f:
    exec(f.read())

long_description = open(Path(__file__,).parent.joinpath('README.md')).read()

setup(name='divtel',
      version=__version__,
      description="Divergent pointing mode for Imaging Atmospheric Cherenkov Telescopes arrays",
      packages=find_packages(),
      install_requires=['astropy',
                        'numpy',
                        'matplotlib',
                        ],
      extras_require={'tests': ['pytest', 'pytest-ordering'],
                      'examples': ['ipywidgets', 'ipympl', 'nodejs']
                      },
      package_data={},
      author='T. Vuillaume, A. Donini, T. Gasparetto',
      author_email='thomas.vuillaume@lapp.in2p3.fr',
      license='MIT',
      url='https://github.com/cta-observatory/divtel',
      long_description="Visit https://github.com/cta-observatory/divtel",
      )
