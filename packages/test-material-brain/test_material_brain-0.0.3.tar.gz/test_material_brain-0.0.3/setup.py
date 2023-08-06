from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'A simple python package for testing'
LONG_DESCRIPTION = 'A simple python package for testing with slightly more text'

# Setting up the package
setup(
    name='test_material_brain',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Stephane Chattot',
    author_email='stephane.chattot@heig-vd.ch',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'scikit-image', 'matplotlib', 'pandas', 'sklearn','ssqueezepy', 'openpyxl', 'matplotlib'],
    keywords=['python', 'test', 'package', 'material_brain'],
    classifiers=[
        "Development Status :: 3 - Alpha",
    ]
)
    