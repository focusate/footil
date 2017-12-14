# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name="Amount in Words",
    version='0.1.0',
    author="Focusate",
    author_email="dev@focusate.eu",
    url='git@github.com:focusate/extra-tools.git',
    license='MIT',
    long_description=open('README.rst').read(),
    py_modules=['amount2words', ],
    install_requires=[
        'num2words',
    ],
)
