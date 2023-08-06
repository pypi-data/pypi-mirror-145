import os

from setuptools import setup

PROJECT_ROOT, _ = os.path.split(__file__)

NAME = 'ferris-cli'
EMAILS = 'bal@ballab.com'
AUTHORS = 'Balaji Bal'
VERSION = '2.5.2'

URL = 'https://github.com/Ferris-Labs/ferris-cli/tree/v2'
LICENSE = 'Apache2.0'


SHORT_DESCRIPTION = 'Utilities for working with the Ferris.ai Platform'

try:
    import pypandoc
    DESCRIPTION = pypandoc.convert(os.path.join(PROJECT_ROOT, 'README.md'),
                                   'rst')
except (IOError, ImportError):
    DESCRIPTION = SHORT_DESCRIPTION

INSTALL_REQUIRES = open(os.path.join(PROJECT_ROOT, 'requirements.txt')). \
        read().splitlines()


setup(
    name=NAME,
    version=VERSION,
    author=AUTHORS,
    author_email=EMAILS,
    packages=[
        'ferris_cli',
        ],
    install_requires=INSTALL_REQUIRES,
    url=URL,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
    license=LICENSE,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Logging',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
