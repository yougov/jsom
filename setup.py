import os
import sys

from setuptools import setup, find_packages


setup(
    name='jsom',
    use_scm_version=True,
    description="JSON Schema Object Mapper",
    long_description='',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3',
    keywords='json schema object mapper',
    author='YouGov, Plc.',
    author_email='dev@yougov.com',
    url='https://github.com/yougov/jsom',
    license='BSD 2-Clause',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    setup_requires=['setuptools_scm'],
    entry_points='',
)
