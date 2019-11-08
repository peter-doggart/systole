# Copyright (C) 2019 Nicolas Legrand
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


DESCRIPTION = "Embodied Computation Toolbox"
LONG_DESCRIPTION = """Physiological signal analyses with Python.
"""

DISTNAME = 'ect'
MAINTAINER = 'Nicolas Legrand'
MAINTAINER_EMAIL = 'nicolas.legrand@cfin.au.dk'
VERSION = '0.0.1'

INSTALL_REQUIRES = [
    'numpy>=1.15',
    'scipy>=1.3',
    'pandas>=0.24',
    'matplotlib>=3.0.2',
    'seaborn>=0.9.0',
    'psychopy>=3.2.3'
]

PACKAGES = [
    'ect',
]

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license=read('LICENSE'),
          version=VERSION,
          install_requires=INSTALL_REQUIRES,
          include_package_data=True,
          packages=PACKAGES,
          )