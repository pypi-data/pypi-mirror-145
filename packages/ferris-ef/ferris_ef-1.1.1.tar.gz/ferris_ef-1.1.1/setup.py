import os
import imp
from setuptools import setup, find_packages

PACKAGE_NAME = "ferris_ef"
version = "1.1.1"


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname)).read()


def desc():
    return read('README.md')

setup(
    name=PACKAGE_NAME,
    version=version,
    url='https://pypi.org/project/ferris-ef/',
    license='Apache2.0',
    author="Nikola Gajin",
    author_email="nikola@ferrislab.net",
    description="Utilities for working with Ferris Executor Framework",
    long_description_content_type='text/markdown',
    long_description=desc(),
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=["ferris_cli"],
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
