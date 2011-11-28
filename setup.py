#!/usr/bin/env python

from setuptools import setup


setup(name='Sirious',
        version='dev',
        author='Will Boyce',
        description='Tampering Siri Proxy',
        license="BSD",
        url='https://github.com/wrboyce/sirious',
        install_requires=['biplist', 'pydispatcher', 'twisted'],
        packages=['sirious', 'sirious.plugins'])
