#! /usr/bin/env python
import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pdf-generator-advinow',
    version='0.4.2',
    description='Utility for producing PDFs from Doctor Notes.',
    url='https://gitlab.com/AdviNow/pdf_generator/',
    download_url='https://gitlab.com/AdviNow/pdf_generator/-/archive/master/pdf_generator-master.tar.gz',
    install_requires=[
        'neo4jrestclient',
        'pandas',
        'python-dotenv',
        'reportlab',
        'requests',
        'restricted-pkg',
        'python-dateutil',
    ],
    license='MIT',
    include_package_data=True,
    author='AdviNow Medical',
    packages=['pdf_generator'],
)
