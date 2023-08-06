#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


# https://github.com/pypa/pip/blob/ec8edbf5df977bb88e1c777dd44e26664d81e216/setup.py#L15-L21
def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="oso-cloud",
    version=get_version("src/oso_cloud/__init__.py"),
    license="BSD-2-Clause",
    description="Oso Cloud client.",
    long_description=read("README.md"),
    author="Oso Security",
    author_email="support@osohq.com",
    url="https://github.com/osohq",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    project_urls={
        # "Documentation": "https://docs.osohq.com/",
        # "Changelog": "https://docs.osohq.com/",
        # "Issue Tracker": "https://github.com/osohq",
    },
    keywords=[
        "authorization",
        "rbac",
    ],
    python_requires=">=3.6",
    install_requires=["requests>=2.27.1"],
    setup_requires=["setuptools>=60.9.2"],
)
