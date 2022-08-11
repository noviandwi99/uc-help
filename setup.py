import setuptools
import os

from epslab.__version__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epslab", # Replace with your own username
    version=__version__,
    author="Muhammad Yasirroni",
    author_email="muhammadyasirroni@gmail.com",
    description="IBM CPLEX optimization tools implementation on electrical power system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/yasirroni/EPSLab",
    packages=setuptools.find_packages(),
    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Scientific Engineering :: Mathematics",
    ],
    python_requires='==3.7',
)
