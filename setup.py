from setuptools import setup, find_packages
import codecs
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.2.61"
DESCRIPTION = 'ASCII Terminal Animation Package'
LONG_DESCRIPTION = 'A package that allows for various animations in the terminal'

# Setting up
setup(
    name="bruhanimate",
    version=VERSION,
    author="Ethan Christensen",
    author_email="ethanlchristensen@outlook.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/ethanlchristensen/bruhanimate',
    packages=find_packages(),
    install_requires=[
        "future",
        "bruhcolor",
        "pyfiglet",
        "pyaudio",
        "numpy",
        "openai",
        "requests"
    ],
    extras_require={
        ':sys_platform == "win32"': ['pywin32'],
    },
    setup_requires=['setuptools_scm'],
    keywords=['python', 'terminal', 'terminal-animation', 'bruhanimate'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)