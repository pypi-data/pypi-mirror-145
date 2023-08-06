# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# OARepo-Communities is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that adds support for communities"""

import os

from setuptools import find_packages, setup

readme = open('README.md').read()
history = open('CHANGES.rst').read()

OAREPO_VERSION = os.environ.get('OAREPO_VERSION', "3.3.134")

tests_require = [
    'pydocstyle',
    'isort'
]

extras_require = {
    'tests': [
        'oarepo[tests]~={version}'.format(version=OAREPO_VERSION),
        *tests_require
    ],
    'build': [
         'oarepo-model-builder'
    ]
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
]

install_requires = [

    'deepmerge'
]

packages = find_packages(exclude=["tests", 'tests.api', 'tests.api.mappings', 'tests.api.mappings.v7'])

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('oarepo_loose_validation', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='oarepo-loose-validation',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio oarepo loose validation',
    long_description_content_type='text/markdown',
    license='MIT',
    author='Alžběta Pokorná',
    author_email='lili3@cesnet.cz',
    url='https://github.com/oarepo/oarepo-loose-validation',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={

    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 1 - Planning',
    ],
)
