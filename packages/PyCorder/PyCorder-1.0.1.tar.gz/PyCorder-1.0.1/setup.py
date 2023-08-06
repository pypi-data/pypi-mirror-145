from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

f.close()

setup(
    name='PyCorder',
    version='1.0.1',
    description='A audio recorder for python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='LUA9',
    maintainer='LUA9',
    packages=['PyCorder'],
    requires=['pipwin']
)