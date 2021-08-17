#!/usr/bin/env python


from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="disco",
    version="0.1.1",
    description="Python library to process company names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["Cython", "aca", "tqdm"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "tox"],
)
