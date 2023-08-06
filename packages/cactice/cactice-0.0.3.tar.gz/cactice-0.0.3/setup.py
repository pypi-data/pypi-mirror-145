#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cactice',
    version='0.0.3',
    description='computing agricultural crop lattices',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Computational Plant Science Lab',
    author_email='wbonelli@uga.edu',
    license='BSD-3-Clause',
    url='https://github.com/Computational-Plant-Science/cactice',
    packages=setuptools.find_packages(),
    include_package_data=True,
    # TODO: CLI
    # entry_points={
    #     'console_scripts': [
    #         'cactice = cactice.cli:cli'
    #     ]
    # },
    python_requires='>=3.6.8',
    install_requires=['numpy', 'scipy', 'pandas', 'pytest', 'matplotlib', 'seaborn', 'jupyter', 'tqdm', 'click'],
    setup_requires=['wheel'],
    tests_require=['pytest', 'coveralls'])