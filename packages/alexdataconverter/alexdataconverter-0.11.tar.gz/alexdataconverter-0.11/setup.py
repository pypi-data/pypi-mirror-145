from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='alexdataconverter',
    version='0.11',
    description='Converts databases between .txt, .json, .csv or .xlxs files through python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://pypi.org/',
    install_requires=['openpyxl==3.0.9'],
    packages=['alexdataconverter'],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
