#!/usr/bin/env python

import sys
import os
try:
    from setuptools import setup
    from setuptools.depends import get_module_constant
except ImportError:
    from distutils.core import setup

# import dockerhub_status_image_api
HERE = os.path.abspath(os.path.dirname(__file__))
__version__ = get_module_constant("dockerhub_status_image_api", "__version__")
__doc__ = get_module_constant("dockerhub_status_image_api", "__doc__")
__author__ = get_module_constant("dockerhub_status_image_api", "__author__")

def read_file_named(file_name):
    file_path = os.path.join(HERE, file_name)
    with open(file_path) as file:
        return file.read()

def read_requirements_file(file_name):
    content = read_file_named(file_name)
    lines = []
    for line in content.splitlines():
        comment_index = line.find("#")
        if comment_index >= 0:
            line = line[:comment_index]
        line = line.strip()
        if not line:
            continue
        lines.append(line)
    return lines

required_packages = read_requirements_file("requirements.txt")

setup(name='dockerhub_status_image_api',
      version=__version__,
      description='Status API server for dockerhub.',
      long_description=__doc__,
      author=__author__,
      author_email='nicco' + 'kunzmann@gmail.com',
      url='https://github.com/niccokunzmann/dockerhub-build-status-image',
      py_modules=['dockerhub_status_image_api'],
      scripts=['dockerhub_status_image_api.py'],
      license='AGPL',
      platforms='any',
      install_requires=required_packages,
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: AGPL License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   ],
)