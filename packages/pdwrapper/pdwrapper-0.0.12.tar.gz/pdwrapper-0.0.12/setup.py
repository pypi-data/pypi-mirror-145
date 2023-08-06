#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

test_requirements = ['pytest>=3', ]

setup(
    name="pdwrapper",
    version="0.0.12",
    author="Butler Hospitality",
    description="Script used inside nx targets for deploying services",
    python_requires='>=3.6',
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='pdwrapper',
    packages=find_packages(include=['pdwrapper', 'pdwrapper.*']),
    entry_points={
        'console_scripts': [
            'pdwrapper=pdwrapper.pdwrapper:cli',
        ],
    },
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False
)
