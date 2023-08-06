#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup
'''
:author:    madkote
:contact:   madkote(at)bluewin.ch
:copyright: Copyright 2021, madkote

setup
-----
Setup script
'''

from __future__ import absolute_import

import codecs
import importlib.util
import os
import sys

from setuptools import setup
from setuptools import find_packages

__author__ = 'madkote <madkote(at)bluewin.ch>'
__copyright__ = 'Copyright 2021, madkote'


if sys.version_info < (3, 6, 0):
    raise RuntimeError('Python 3.6+ required')
elif sys.version_info >= (3, 8, 0):
    raise RuntimeError('Python 3.8+ is not supported yet')


with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('CHANGES.md', 'r') as fh:
    changes_description = fh.read()

with open('LICENSE', 'r') as fh:
    licence_description = fh.read()

with open('NOTICE', 'r') as fh:
    licence_description += os.linesep + fh.read()


def get_version(package_name):
    try:
        version_file = os.path.join(
            os.path.dirname(__file__),
            package_name,
            'version.py'
        )
        spec = importlib.util.spec_from_file_location(
            '%s.version' % package_name,
            version_file
        )
        version_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(version_module)
        package_version = version_module.__version__
    except Exception as e:
        raise ValueError(
            'can not determine "%s" version: %s :: %s' % (
                package_name, type(e), e
            )
        )
    else:
        return package_version


def load_requirements(filename):
    def _is_req(s):
        return s and not s.startswith('-r ') and not s.startswith('git+http') and not s.startswith('#')  # noqa E501

    def _read():
        with codecs.open(filename, 'r', encoding='utf-8-sig') as fh:
            for line in fh:
                line = line.strip()
                if _is_req(line):
                    yield line
    return sorted(list(_read()))


NAME = 'rasa-nlu-contrib'
NAME_PACKAGE = NAME.replace('-', '_').replace('_contrib', '')
VERSION = get_version(NAME_PACKAGE)
DESCRIPTION = 'Rasa NLU engine backported from main Rasa project'
URL = 'https://github.com/madkote/%s' % NAME

REQUIRES_INSTALL = [
    'cloudpickle~=0.6.1',
    'coloredlogs~=10.0',
    'future~=0.17.1',
    'jsonschema~=2.6.0',
    'matplotlib~=2.2.4',
    'numpy~=1.16.0',
    'packaging~=18.0',
    'requests~=2.20.0',
    'ruamel.yaml~=0.15.78',
    'scikit-learn~=0.20.2',
    'simplejson~=3.13.2',
    'six~=1.11.0',
    'tqdm~=4.19.5',
    'typing~=3.6.2'
]
REQUIRES_DUCKLING = [
    'duckling==1.8.0',
    'Jpype1==0.6.2'
]
REQUIRES_MITIE = [
    'mitie==0.7.0',
]
REQUIRES_SERVER = [
    'hyperlink~=17.3.1',
    'klein~=17.10.0',
    'Twisted==20.3.0'
]
REQUIRES_SPACY = [
    'spacy~=2.0.18,>2.0',
    'scipy~=1.2.0',
    'sklearn-crfsuite~=0.3.6'
]
REQUIRES_TENSORFLOW = [
    'tensorflow~=1.13.1',
    'scipy~=1.2.0',
    'sklearn-crfsuite~=0.3.6'
]
REQUIRES_TESTS = [
    'bandit~=1.7.0',
    'docker-compose~=1.28.0',
    'flake8~=3.8.4',
    'httpretty~=0.9.5',
    'mock~=2.0.0',
    'moto~=1.3.8',
    'python-coveralls~=2.9.1',
    'pytest~=3.2.5',
    'pytest-pycodestyle~=1.4.0',
    'pytest-cov~=2.5.1',
    'pytest-twisted<1.6',
    'responses~=0.9.0',
    # 'tox~=3.21.0',  # TODO: currently ignored due to issues with SIX
    'treq~=17.8.0'
]
REQUIRES_ZH = [
    'jieba==0.39'
]
REQUIRES_EXTRA = {
    'all': REQUIRES_SERVER + REQUIRES_SPACY + REQUIRES_TENSORFLOW,
    'duckling': REQUIRES_DUCKLING,
    'mitie': REQUIRES_MITIE,
    'server': REQUIRES_SERVER,
    'spacy': REQUIRES_SPACY,
    'tensorflow': REQUIRES_TENSORFLOW,
    'test': REQUIRES_SERVER + REQUIRES_TESTS,
    'zh': REQUIRES_ZH
}

PACKAGES = find_packages(exclude=('scripts', 'tests*'))
PACKAGE_DATA = {}


# =============================================================================
# SETUP
# =============================================================================
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author='madkote',
    author_email=__author__.replace('(at)', '@'),
    url=URL,
    project_urls={
        'Bug Reports': 'https://github.com/madkote/rasa_nlu_contrib/issues',
        'Source': 'https://github.com/madkote/rasa_nlu_contrib',
    },
    download_url=URL + '/archive/{}.tar.gz'.format(VERSION),
    license='MIT / Apache 2.0',  # licence_description,
    keywords=[
        'nlp', 'machine-learning', 'machine-learning-library', 'bot', 'bots',
        'botkit', 'conversational-agents', 'conversational-ai', 'chatbot',
        'chatbot-framework', 'bot-framework'
    ],
    install_requires=REQUIRES_INSTALL,
    tests_require=REQUIRES_TESTS,
    extras_require=REQUIRES_EXTRA,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    python_requires='>=3.6, !=3.8.*, !=3.9.*, <4',
    include_package_data=True,
    long_description='\n\n'.join((long_description, changes_description)),
    long_description_content_type='text/markdown',
    platforms=['any'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
    ]
)

print('\nWelcome to Rasa NLU Backport!')
print('If any questions please visit documentation page https://legacy-docs.rasa.com/docs/nlu/')  # noqa E501
print('or join the community discussions on https://forum.rasa.com')
