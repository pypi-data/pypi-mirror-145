#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('./docs/install.rst') as install_file:
    install = install_file.read()

with open('./docs/tutorial.rst') as tutorial_file:
    tutorial = tutorial_file.read()

with open('CHANGELOG.rst') as changelog_file:
    changelog = changelog_file.read()

tests_require = [
    'pytest>=7.0.1',
]

dev_require = [
    'ipdb',
    'ipython',
    'pre-commit'
]

docs_require = [
    'Sphinx~=4.0',
    'sphinx-autobuild',
    'sphinxcontrib-autorun',
    'sphinxcontrib-napoleon>=0.4.4',
    'sphinx_rtd_theme',
    'sphinxcontrib-httpdomain',
]
setup(
    name='glitter_sdk_test',
    version='0.1.0',
    author='ted',
    author_email='ted@glitterprotocol.io',
    url='https://docs.glitterprotocol.io/',
    description=u'Glitter Protocol is a blockchain based database and index engine for developing and hosting web3 applications in decentralized storage networks.',
    long_description=readme + '\n\n' + changelog,
    python_requires='>=3.5',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={},
    test_suite='tests',
    extras_require={
        'test': tests_require,
        'dev': dev_require + tests_require + docs_require,
        'docs': docs_require,
    },
)
