#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='nova-ide',
    version='0.1.0',
    description='Nova Language Integrated Development Environment',
    long_description='A dedicated IDE for Nova programming language',
    author='Nova Team',
    author_email='info@nova-lang.org',
    url='https://nova-lang.org',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'PyQt5==5.15.9',
        'QScintilla==2.13.3',
        'watchdog==3.0.0',
        'nova-language'
    ],
    entry_points={
        'console_scripts': [
            'nova-ide = main:main'
        ],
        'gui_scripts': [
            'nova-ide-gui = main:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: IDE'
    ],
    python_requires='>=3.7'
)