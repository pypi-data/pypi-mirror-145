from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.11'
DESCRIPTION = 'Package for df transformations using pandas'
LONG_DESCRIPTION = 'A package that contains transformers for NAN cleaning, IQR filtering, plotting learning curve.' \
                   'To avoid redundant code in the colab notebook'

# Setting up
setup(
    name="pianko",
    version=VERSION,
    author="Pavel Ianko",
    author_email="<pavel.evgenievich.ianko@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'sklearn', 'matplotlib'],
    keywords=['python', 'pandas', 'numpy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
