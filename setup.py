'''mailmig - A python-based mail migration / sync solution

See:
https://github.com/jhannah01/mailmig
'''

import os.path
import codecs
import pkg_resources
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = None

pkg_name = 'mailmig'
pkg_description = 'A python-based mail migration and syncing solution'
pkg_requirements=[
    'beautifultable',
    'beautifulsoup4',
    'requests',
    'imaplib2',
    'simplejson',
    'sqlitedict']
pkg_keywords = 'mail sync imap migration smartermail smartertools zoho',
from mailmig import __version__ as pkg_version


setup(
    name=pkg_name,
    version=pkg_version,
    description='A basic API wrapper for interacting with SmarterMail',
    long_description=long_description,
    url='https://github.com/jhannah01/%s' % pkg_name,
    license='GNU',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Communications :: Email'
    ],
    keywords=pkg_keywords,
    packages=find_packages(exclude=['contrib', 'docs', 'tests', '.local']),
    install_requires=pkg_requirements,
    #entry_points={
    #    'console_scripts': ['mailmig=mailmig.cli:run_clitool']
    #}
)

