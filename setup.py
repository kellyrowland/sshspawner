#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) Juptyer Development Team.
# Distributed under the terms of the Modified BSD License.
#
# ----------------------------------------------------------------------------
# Minimal Python version sanity check (from IPython/Jupyterhub)
# ----------------------------------------------------------------------------
from __future__ import print_function

import argparse
import os
import socket
import sys

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, 'version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name='sshspawner',
    packages=['sshspawner'],
    version=version_ns['__version__'],
    description="""SSH Spawner: A custom spawner for Jupyterhub to spawn
                   notebooks over SSH""",
    long_description="""Spawn Jupyter notebooks on a remote node over SSH. Supports GSI and
                        SSH Key based authentication.""",
    author="Shreyas Cholia, Shane Canon, Rollin Thomas",
    author_email="scholia@lbl.gov, scanon@lbl.gov, rcthomas@lbl.gov",
    url="http://www.nersc.gov",
    license="BSD",
    platforms="Linux, Mac OS X",
    keywords=['Interactive', 'Interpreter', 'Shell', 'Web'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    entry_points = {
    	'console_scripts' : ['get_port=scripts/get_port.__main__:main'],
    }
)

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = []
    with open('requirements.txt') as f:
        for line in f.readlines():
            req = line.strip()
            if not req or req.startswith(('-e', '#')):
                continue
            install_requires.append(req)

def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
