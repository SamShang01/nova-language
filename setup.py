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
readme_file = os.path.join(os.path.dirname(__file__), '语言说明书.md')
if os.path.exists(readme_file):
    with open(readme_file, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='nova-language',
    version=version_str,
    description='Nova编程语言',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nova Team',
    author_email='nova@example.com',
    url='https://github.com/nova-language/nova',
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
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.14',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Interpreters',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 依赖项
    ],
)
