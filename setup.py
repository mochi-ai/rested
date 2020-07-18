# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# use pytest for test command
class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = "--ignore=rested"
    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)

# package settings
setup(

    # info
    name='django-rested',
    version=open('rested/version.txt').read().strip(),
    author='Stephen Quebe',
    author_email='stephen@mochi.ai',
    url='https://github.com/mochi-ai/rested.git',
    description='Make creating rest APIs in Django simple.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    # include
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,

    # public dependencies
    install_requires=[
        'django==3.0',
        'channels==2.4.0',
        'channels-redis==2.4.1',
        'django-extensions==2.2.6',
        'ipython==7.11.1',
        'pytest==5.3.1',
        'pytest-django==3.7.0',
        'pytest-mock==3.2.0',
        'watchdog==0.9.0',
        'celery==4.4.0',
        'redis==3.3.11'],

    # cli scripts
    entry_points={'console_scripts': ['rested = rested.cli:main']},

    # tests
    tests_require=['django', 'pytest', 'pytest-django', 'pytest-watch', 'pytest-mock'],
    cmdclass={"test": PyTest},
)
