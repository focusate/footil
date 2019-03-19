from distutils.core import setup

setup(
    name='Footil',
    version='0.2.0',
    packages=['footil'],
    license='LGPLv3',
    long_description=open('README.rst').read(),
    install_requires=['yattag']
)
