#!/usr/bin/env python3

# coding: utf-8
"""Plotting and analysis tools for the ARTIS 3D supernova radiative transfer code."""

import datetime
import sys

from pathlib import Path
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

# sys.path.append('artistools/')
# from commands import console_scripts
from artistools.commands import console_scripts, completioncommands


# Add the following lines to your .zshrc file to get command completion:
# autoload -U bashcompinit
# bashcompinit
# source artistoolscompletions.sh
with open('artistoolscompletions.sh', 'w') as f:
    f.write('\n'.join(completioncommands))


class PyTest(TestCommand):
    """Setup the py.test test runner."""

    def finalize_options(self):
        """Set options for the command line."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Execute the test runner command."""
        # Import here, because outside the required eggs aren't loaded yet
        import pytest
        sys.exit(pytest.main(self.test_args))


def get_version():
    utcnow = datetime.datetime.utcnow()
    strversion = f'{utcnow.year}.{utcnow.month}.{utcnow.day}.'
    strversion += f'{utcnow.hour:02d}{utcnow.minute:02d}{utcnow.second:02d}.'
    strversion += 'dev'
    return strversion


setup(
    name="artistools",
    version='2022.04.04',
    author="ARTIS Collaboration",
    author_email="luke.shingles@gmail.com",
    packages=find_packages(),
    url="https://www.github.com/artis-mcrt/artistools/",
    license="MIT",
    description="Plotting and analysis tools for the ARTIS 3D supernova radiative transfer code.",
    long_description=(Path(__file__).absolute().parent / "README.md").open('rt').read(),
    long_description_content_type='text/markdown',
    install_requires=(Path(__file__).absolute().parent / "requirements.txt").open('rt').read().splitlines(),
    entry_points={
        'console_scripts': console_scripts,
    },
    scripts=['artistoolscompletions.sh'],
    python_requires='>==3.6',
    # test_suite='tests',
    setup_requires=['pytest', 'pytest-runner', 'pytest-cov'],
    tests_require=['pytest', 'pytest-runner', 'pytest-cov'],
    include_package_data=True)
