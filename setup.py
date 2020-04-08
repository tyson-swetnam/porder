import sys
import os
import sys
import setuptools
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version

if StrictVersion(setuptools_version) < StrictVersion('38.3.0'):
    raise SystemExit(
        'Your `setuptools` version is old. '
        'Please upgrade setuptools by running `pip install -U setuptools` '
        'and try again.'
    )


def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='porder',
    version='0.6.8',
    packages=['porder'],
    url='https://github.com/samapriya/porder',
    package_data={'': ['bundles.json']},
    install_requires=['requests>=2.21.1','planet>=1.4.5','retrying>=1.3.3',
                      'progressbar2>=3.38.0',
                      'visvalingamwyatt>=0.1.2',
                      'pendulum>=2.0.4',
                      'DateTimeRange>=0.6.1',
                      'beautifulsoup4',
                      'pySmartDL==1.2.5;python_version<"3.4"',
                      'pySmartDL>=1.3.1;python_version>"3.4"',
                      'pyproj>=1.9.5.1;platform_system!="Windows"',
                      'shapely>=1.6.4;platform_system!="Windows"',
                      'fiona>=1.8.6;platform_system!="Windows"',
                      'geopandas>=0.5.0;platform_system!="Windows"',
                      'clipboard>=0.0.4','pyyaml>=3.12','prettytable>=0.7.2',],
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=2.7',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Simple CLI for Planet Orders v2',
    entry_points={
        "console_scripts": ["porder=porder.porder:main"]
    },
)
