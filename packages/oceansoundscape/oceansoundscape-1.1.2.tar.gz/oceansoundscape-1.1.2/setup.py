#!/usr/bin/env python

from setuptools import setup
import re
import os

def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(
    name="oceansoundscape",
    version=get_version("oceansoundscape"),
    url='https://docs.mbari.org/oceansoundscape',
    license='GPL',
    description='A python package for analyzing ocean acoustic data',
    author='Danelle Cline',
    author_email='dcline@mbari.org',
    packages=get_packages("oceansoundscape"),
    package_data={
        "oceansoundscape": ["testdata/*.*"],
    },
    include_package_data=True,
    install_requires=[
        "h5py>=3.6.0",
        "numpy>=1.19.2",
        "librosa==0.9.1",
        "matplotlib>=3.2.2",
        "opencv-python-headless>=4.2.0",
        "pandas>=1.1.0",
        "scipy>=1.6.2",
        "soundfile==0.10.3.post1"
    ],
    python_requires='>=3.8,<3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    zip_safe=False,
)
