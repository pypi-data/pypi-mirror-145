from setuptools import setup, find_namespace_packages

setup(
    name='pointevector-zip',
    version='0.0.1',
    author='Andrew Hoekstra',
    author_email='andrew@pointevector.com',
    url='https://github.com/Pointe-Vector/zip',
    packages=find_namespace_packages(),
    install_requires=[
        'dataclasses',
    ],
)
