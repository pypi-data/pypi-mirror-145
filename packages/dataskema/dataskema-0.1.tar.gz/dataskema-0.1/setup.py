# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='dataskema',
    packages=['dataskema'],
    include_package_data=True,  # -- para que se incluyan archivos sin extension .py
    version='0.1',
    description='Data schema to validate parameters easily, quickly and with minimal code',
    author='Luis A. González Rivas',
    author_email="lagor55@gmail.com",
    license="MIT",
    url="https://github.com/lagor-github/dataskema",
    classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta", "Intended Audience :: Developers",
        "Operating System :: OS Independent"],
    )
