"""Holds all relevant information for packaging and publishing to PyPI."""
from typing import List

import setuptools

# no external requirements of now
requirements: List[str] = []

test_requirements = [
    "pytest",
    "pytest-cov",
    "pytest-timeout",
    "mypy",
    "types-all",
    "pylint_runner",
    "flake8",
    "flake8-docstrings",
    "flake8-bugbear",
    "bandit",
    "black",
]

dev_requirements = test_requirements.copy()

extra_requirements = {
    "test": test_requirements,
    "dev": dev_requirements,
    "all": [
        *requirements,
        *test_requirements,
        *dev_requirements,
    ],
}

VERSION = "0.0.2"

# pylint: disable=line-too-long
with open("README.md", "r", encoding="utf-8") as fh_read:
    long_description = fh_read.read()
setuptools.setup(
    name="cztile",
    version=VERSION,
    author="Nuno Mesquita",
    author_email="nuno.mesquita@zeiss.com",
    description="A set of tiling utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Note: Exclude test folder in MANIFEST.in to also remove from source dist
    # See https://stackoverflow.com/questions/8556996/setuptools-troubles-excluding-packages-including-data-files
    # See https://docs.python.org/3.6/distutils/sourcedist.html
    packages=setuptools.find_packages(exclude=["test", "test.*"]),
    license_files=["LICENSE.txt", "NOTICE.txt"],
    # Classifiers help users find your project by categorizing it.
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # Make required Python version compliant with official TF docs (https://www.tensorflow.org/install)
    # It follows: We build a pure Python wheel
    # Note that Python used to build the sources specifies the Python version of the dist (relevant during build only)
    # See https://packaging.python.org/guides/distributing-packages-using-setuptools/#pure-python-wheels for more info
    # We also restrict the code to >3.6 to:
    # - fully benefit from type annotations (See https://realpython.com/python-type-checking/ for more info)
    # - having dataclasses natively supported (starting 3.7+)
    # - + see https://realpython.com/python-data-classes/
    # - + no need to include it as ext. pkg through backport in 3.6 (dev.to/hanpari/dataclasses-in-python-3-6-29id)
    # We also restrict the code to <3.10 since:
    # - No source distribution support for 3.10 yet
    # - + See https://stackoverflow.com/questions/69458399/numpy-1-21-2-may-not-yet-support-python-3-10
    # - + See https://github.com/numpy/numpy/issues/17044
    # - + not relevant as of today, but maybe in the future
    python_requires=">3.6,<3.10",
    install_requires=requirements,
    extras_require=extra_requirements,
)
