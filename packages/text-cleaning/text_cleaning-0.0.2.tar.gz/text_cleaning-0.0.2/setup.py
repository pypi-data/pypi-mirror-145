from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Text Cleaning'
LONG_DESCRIPTION = 'A package that allows to automatic and custom text cleaning.'

# Setting up
setup(
    name="text_cleaning",
    version=VERSION,
    author="Piyush Mittal",
    author_email="<piyushmittal2192@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['more_itertools', 'sklearn', 'collections', 'numpy', 'levenshtein']
    
)
