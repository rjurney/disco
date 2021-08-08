#!/usr/bin/env python


from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="disco",
    description="Python library to process company names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["disco"],
    install_requires=["cython", "aca", "tqdm"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "tox"],
)
