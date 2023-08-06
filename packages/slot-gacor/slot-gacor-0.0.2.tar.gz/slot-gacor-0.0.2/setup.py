from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path

VERSION = '0.0.2'
DESCRIPTION = 'Daftar Link Bocoran Slot Gacor'
this_directory = Path(__file__).parent
long_description = (this_directory/"README.md").read_text()

# Setting up
setup(
    name="slot-gacor",
    version=VERSION,
    author="QQBARENG",
    author_email="<qqbareng@preout.download>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    keywords=['slot','slot gacor','slot gacor hari ini','link slot gacor','slot online'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
