#!/usr/bin/env python3
"""Setup script for baseline-cli."""

from setuptools import setup, find_packages
import os

# Read version from __version__.py
version_info = {}
with open('__version__.py') as f:
    exec(f.read(), version_info)

# Read long description from README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name=version_info['__title__'],
    version=version_info['__version__'],
    author='baseline-cli',
    author_email='your-email@example.com',
    description=version_info['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Hiccup-za/baseline-cli',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Testing',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'baseline=baseline:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 