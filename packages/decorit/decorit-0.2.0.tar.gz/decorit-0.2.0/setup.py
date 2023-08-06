# -*- coding: utf-8 -*-
import pathlib
from collections import defaultdict

import setuptools


def get_extra_requirements(path, add_all=True):
    """Parse extra-requirements file."""

    with open(path) as depfile:
        extra_deps = defaultdict(set)
        for line in depfile:
            if not line.startswith('#'):
                if ':' not in line:
                    raise ValueError(
                        f'Dependency in {path} not correct formatted: {line}',
                    )
                dep, tags = line.split(':')
                tags = {tag.strip() for tag in tags.split(',')}
                for tag in tags:
                    extra_deps[tag].add(dep)

        # add tag `all` at the end
        if add_all:
            extra_deps['all'] = {
                tag for tags in extra_deps.values() for tag in tags
            }

    return extra_deps


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setuptools.setup(
    name='decorit',
    version='0.2.0',
    description='Handy ready-to-use decorators.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='decorators',
    author='braniii',
    url='https://gitlab.com/braniii/decorit',
    license='BSD 3-Clause License',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 3 - Alpha',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=['beartype>=0.10.4'],
    extras_require=get_extra_requirements('extra-requirements.txt'),
)
