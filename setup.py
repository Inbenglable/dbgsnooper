# Copyright 2019 Ram Rachum and collaborators.
# This program is distributed under the MIT license.
import setuptools
import re


def read_file(filename):
    with open(filename) as file:
        return file.read()

version = re.search("__version__ = '([0-9.]*)'",
                    read_file('dbgsnooper/__init__.py')).group(1)

setuptools.setup(
    name='dbgsnooper',
    version=version,
    author='axel',
    author_email='',
    description="dbgsnooper for debugging agent",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/Inbenglable/PySnooper.git',
    packages=setuptools.find_packages(exclude=['tests*']),
    install_requires=[],
    extras_require={
        'tests': {
            'pytest',
        },
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Debuggers',
    ],
)
