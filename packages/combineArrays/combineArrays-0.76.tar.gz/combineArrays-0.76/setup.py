from setuptools import setup

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup( 
    name="combineArrays",
    version="0.76",
    description="Using Python CFFI bindings for funtions to combine NumPy arrays in C++",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    author='Norbert Henseler',
    author_email='nhenseler@web.de',
    license_file='LICENSE',
    py_modules=['combineArrays'],
    package_dir={'': 'src'},
    install_requires=['cffi>=1.0.0'],
    setup_requires=['cffi>=1.0.0'],
    cffi_modules=['./src/buildCombineArrays.py:ffibuilder'],
    include_package_data=True,
    package_data={'':['tests/test.py']},
)

    
    