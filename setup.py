from setuptools import setup, find_packages

setup(
    name="match-report",
    maintainer="Fraser Ewing",
    version="0.0.1",
    author="Fraser Ewing",
    description="A package for creating football match reports using Statsbomb spatio-temporal event data",
    url="https://github.com/frasere/match-report",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
    ),
)