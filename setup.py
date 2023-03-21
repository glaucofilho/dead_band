from Cython.Build import cythonize
from distutils.core import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="dead_band", ext_modules=cythonize("dead_band.pyx"), version="1.0.3")
