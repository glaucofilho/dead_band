import numpy as np
import pandas as pd
from distutils.core import setup
from Cython.Build import cythonize

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="dead_band", ext_modules=cythonize("dead_band.pyx"), version="1.0.2")
