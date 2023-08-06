#! /usr/bin/env python
import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pdf-generator-advinow',
    version='0.4.1',
    description='Utility for producing PDFs from Doctor Notes.',
    url='https://gitlab.com/AdviNow/pdf_generator/',
    download_url='https://gitlab.com/AdviNow/pdf_generator/-/archive/master/pdf_generator-master.tar.gz',
    install_requires=[
        'neo4jrestclient==2.1.1',
        'pandas==1.3.5',
        'python-dotenv==0.9.1',
        'reportlab==3.6.9',
        'requests==2.21.0',
        'restricted-pkg==1.1.2',
        'python-dateutil==2.7.3',
    ],
    license='MIT',
    include_package_data=True,
    author='AdviNow Medical',
    packages=['pdf_generator'],
)
