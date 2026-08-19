"""Build configuration for the compiled extension.

Everything declarative lives in pyproject.toml. This file exists only because
`ext_modules` has no pyproject equivalent: setuptools still needs Python code to
describe a Cython extension.
"""

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

extensions = [
    Extension(
        name="dead_band.cython_modules.c_deadband",
        sources=["src/dead_band/cython_modules/c_deadband.pyx"],
        extra_compile_args=["-O3"],
    )
]

setup(
    name="dead-band",
    ext_modules=cythonize(extensions, language_level="3"),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
