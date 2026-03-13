#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova语言安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取版本信息
version_file = os.path.join(os.path.dirname(__file__), 'src', 'nova', 'version.py')
if os.path.exists(version_file):
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(f.read())
else:
    # 默认版本
    __version__ = (0, 1, 0)

# 转换版本元组为字符串
version_str = '.'.join(map(str, __version__))

# 读取长描述
long_description = ''
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
if os.path.exists(readme_file):
    with open(readme_file, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='nova-language',
    version=version_str,
    description='Nova编程语言 - 一个现代、高性能的编程语言，支持LLVM JIT编译',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SamShang01',
    author_email='13823217069@139.com',
    url='https://github.com/SamShang01/nova-language',
    project_urls={
        'Bug Reports': 'https://github.com/SamShang01/nova-language/issues',
        'Source': 'https://github.com/SamShang01/nova-language',
        'Documentation': 'https://github.com/SamShang01/nova-language/blob/main/语言说明书.md',
    },
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'nova': ['*.py', '*.md', '*.nova'],
    },
    entry_points={
        'console_scripts': [
            'nova=nova.cli:cli_main',
        ],
        'gui_scripts': [
            'nova-gui=nova.cli:gui_main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 依赖项
    ],
)
