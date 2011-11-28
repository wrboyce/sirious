#!/usr/bin/env python

from setuptools import setup


setup(name='Sirious',
        version='dev',
        author='Will Boyce',
        description='Tampering Siri Proxy',
        license="BSD",
        url='https://github.com/wrboyce/sirious',
        install_requires=['biplist', 'pydispatcher', 'pyopenssl', 'twisted'],
        packages=['sirious', 'sirious.plugins'],
        package_data={
            'sirious': ['scripts/gen_certs.zsh'],
        },
        entry_points={
            'console_scripts': [
                'sirious = sirious.scripts:start_proxy',
                'sirious-gencerts = sirious.scripts:gen_certs']
        })
