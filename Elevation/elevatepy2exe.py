__author__ = "Stitch626"
__version__ = "1.6"



from distutils.core import setup
import py2exe , sys, os

setup(
    options = {'py2exe': {'bundle_files': 1}},

    windows = [{'script': "elevate_ntct.py"}],
    zipfile = None,
)
