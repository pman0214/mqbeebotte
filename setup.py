"""
A setuptools based setup module.

"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mqbeebotte',
    version='0.0.4',
    description='Unofficial Beebotte MQTT access package',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/pman0214/mqbeebotte',
    author='Shigemi ISHIDA',
    author_email='ishida+devel@f.ait.kyushu-u.ac.jp',
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # Pick your license as you wish
        'License :: OSI Approved :: BSD License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='mqtt beebotte',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    install_requires=['paho-mqtt'],
    project_urls={
        'Bug Reports': 'https://github.com/pman0214/mqbeebotte/issues',
        'Source': 'https://github.com/pman0214/mqbeebotte/',
    },
)
