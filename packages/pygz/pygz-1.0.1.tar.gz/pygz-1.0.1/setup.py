#!/usr/bin/env python
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygz",
    version="1.0.1",
    author="Zonggui Chen",
    author_email="ggchenzonggui@qq.com",
    description="A wrapper for gzip and pigz in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/chenzonggui/pygz",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix"
    ],
    test_suite="tests",
    python_requires=">=3.6",
)