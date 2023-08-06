# -*- coding: utf-8 -*-
"""
Setup script for pymilestone.
"""

import setuptools

with open("README.rst", "r") as f:
    long_description = f.read()
    
setuptools.setup(
    name="pymilestone",
    version="1.0.0",
    author="Andriy Prots",
    author_email="andprosoft@gmail.com",
    description="Package for creating a milestone plan with python using matplotlib.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/andprosoft/py_milestone",
    packages=setuptools.find_packages('python'),
    package_dir={'': 'python'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'matplotlib',
        'python-dateutil'
    ]        
        
)

