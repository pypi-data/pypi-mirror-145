from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'fNIRS BIDS Validator'
LONG_DESCRIPTION = 'A package that takes path to the fNIRS BIDS folder and returns metadata validation info'

# Setting up
setup(
    name="fNIRS_BIDS_Validator",
    version=VERSION,
    author="Sreekanth Kura",
    author_email="<sreekanth.kura7@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'fNIRS-BIDS', 'fNIRS', 'BIDS'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)