#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

from setuptools import setup, find_packages
from cms_bootstrap4 import __version__
try:
    from pypandoc import convert
except ImportError:
    def convert(filename, fmt):
        with open(filename) as fd:
            return fd.read()

def create_mo_files():
    data_files = []
    localedir = 'cms_bootstrap4/locale'
    po_dirs = [localedir + '/' + l + '/LC_MESSAGES/'
               for l in next(os.walk(localedir))[1]]
    for d in po_dirs:
        mo_files = []
        po_files = [f
                    for f in next(os.walk(d))[2]
                    if os.path.splitext(f)[1] == '.po']
        for po_file in po_files:
            filename, extension = os.path.splitext(po_file)
            mo_file = filename + '.mo'
            msgfmt_cmd = 'msgfmt {} -o {}'.format(d + po_file, d + mo_file)
            subprocess.call(msgfmt_cmd, shell=True)
            mo_files.append(d + mo_file)
        data_files.append((d, mo_files))
    return data_files


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
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
    description='Templates and templatetags to be used with djangoCMS and Bootstrap4.',
    author='Nicolas PASCAL',
    author_email='np.pascal@gmail.com',
    url='https://github.com/haricot/djangocms-bs4forcascade/',
    packages=find_packages(),
    install_requires=[],
    license='LICENSE-MIT',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    long_description=convert('README.md', 'rst'),
    include_package_data=True,
    zip_safe=False,
    data_files=create_mo_files(),
)