#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Nabil-Fareed Alikhan",
    author_email='nabil@happykhan.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Scrapes good music off Reddit, makes a spotify playlist",
    entry_points={
        'console_scripts': ['listentoeverything=listentoeverything.cli:main'],
    },
    install_requires=install_requires,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='listentoeverything',
    name='listentoeverything',
    packages=find_packages(include=['listentoeverything']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/happykhan/listentoeverything',
    version='0.3.1',
    zip_safe=False,
)
