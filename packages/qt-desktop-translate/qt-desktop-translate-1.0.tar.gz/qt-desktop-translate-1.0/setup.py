#!/usr/bin/env python3
from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()


setup(name="qt-desktop-translate",
    version="1.0",
    description="Translate .desktop files with Qt",
    long_description=description,
    long_description_content_type="text/markdown",
    author="JakobDev",
    author_email="jakobdev@gmx.de",
    url="https://gitlab.com/JakobDev/qt-desktop-translate",
    python_requires=">=3.5",
    include_package_data=True,
    install_requires=[
        "lxml",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["desktop-lupdate = qt_desktop_translate.desktop_lupdate:main", "desktop-lrelease = qt_desktop_lrelease.desktop_lrelease:main"]
    },
    license="BSD",
    keywords=["JakobDev", "Qt"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Environment :: Other Environment",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Topic :: Games/Entertainment",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython"
    ]
)

