from gettext import install
from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A simple python package for testing'
LONG_DESCRIPTION = 'A simple python package for testing with slightly more text'

# Setting up the package
setup(
    name='test_material_brain',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=['Stephane Chattot', 'Andrea Bernasconi', 'Vincent Chapallaz', 'Remy Macherel'],
    author_email='stephane.chattot@heig-vd.ch, vincent.chapallaz@heig-vd.ch, andrea.bernasconi@heig-vd.ch, remy.macherel@heig-vd.ch',
    packages=find_packages(),
    install_requires=['os', 'struct', 'numpy', 'scipy', 'skimage', 'matplotlib', 'pandas', 'pathlib', 'sklearn','ssqueezepy', 'openpyxl', 'matplotlib'],
    keywords=['python', 'test', 'package', 'material_brain'],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ]
)
    