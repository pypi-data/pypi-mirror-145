# -*- coding: utf-8 -*-

# @File    : setup.py
# @Date    : 2022-01-28
# @Author  : chenbo

__author__ = 'chenbo'

import io
import os

from setuptools import setup, find_packages

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'walnut_agent', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

with io.open("requirements.txt", encoding='utf-8') as f:
    install_requires = f.read().splitlines()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    python_requires='>=3.8',
    packages=find_packages(include=['walnut_agent', 'walnut_agent.script', 'walnut_agent.common', 'walnut_agent.unit']),
    package_data={},
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'htr=walnut_agent.script.flask_client:main',
        ]
    },
    include_package_data=True
)
