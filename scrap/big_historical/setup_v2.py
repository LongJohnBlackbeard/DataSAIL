from distutils.core import Extension, setup
from Cython.Build import cythonize

# define an extension that will be cythonized and compiled
ext = Extension(name="big_historical_v2_cython", sources=["big_historical_v2_cython.pyx"])
setup(ext_modules=cythonize(ext))
