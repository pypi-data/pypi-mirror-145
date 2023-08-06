#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oyeahz_base",
    version="0.0.1",
    author="linan890107",
    author_email="linan890107@126.com",
    description="Oyeahz组件测试包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dGhpcyBpcyBteSB3b3JsZA/oyeahz_base.git",
    project_urls={
        "Bug Tracker": "https://github.com/dGhpcyBpcyBteSB3b3JsZA/oyeahz_base/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['oyeahz_base'],
    python_requires=">=3.6",
)