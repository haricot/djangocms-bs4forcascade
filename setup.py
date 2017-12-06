#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages
from cmsplugin_bs4forcascade import __version__
try:
    from pypandoc import convert
except ImportError:
    import io

    def convert(filename, fmt):
        with io.open(filename, encoding='utf-8') as fd:
            return fd.read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django :: 1.9',
    'Framework :: Django :: 1.10',
    'Framework :: Django :: 1.11',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

setup(
    name='djangocms-bs4forcascade',
    version=__version__,
    description='Collection of extendible plugins for django-CMS to create and edit widgets in a simple manner, specialy for djangocms-cascade and bootstrap4',
    author='Nicolas PASCAL',
    author_email='np.pascal@gmail.com',
    url='https://github.com/haricot/djangocms-bs4forcascade',
    packages=find_packages(exclude=['examples', 'docs', 'tests']),
    install_requires=[
        'djangocms-cascade>=0.15.3'
    ],
    license='LICENSE-MIT',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    long_description=convert('README.md', 'rst'),
    include_package_data=True,
    zip_safe=False,
)
