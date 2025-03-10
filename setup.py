from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    long_description = f.read()


setup(
    name='toscinterface',
    version='0.0.2',
    packages=find_packages(),
    install_requires=['osc4py3>=1.0.8'],
    author='Marius Seiter',
    author_email='mariuss98@hotmail.de',
    description='A simple package to receive OSC messages sent by TouchOSC',
    long_description=long_description,
    license='MIT',
    python_requires='>=3.10'

)
