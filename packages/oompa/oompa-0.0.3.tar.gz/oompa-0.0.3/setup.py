#!/usr/bin/env python

from setuptools import setup

requirements = [
    'ansible>=4.10.0',
    'ansible-runner>=2.1.3',
    'dhall>=0.1.9',
    'docker>=5.0.3',
]

test_requirements = [
    'pytest>=7.0.1',
    'pytest-cov>=3.0.0',
]

setup(
    install_requires=requirements,
    tests_require=test_requirements,
    package_data={
        "": ['*.tar'],
    },
    entry_points={
        'console_scripts': [
            'oompa=oompa.oompa:main',
        ],
    },
)
