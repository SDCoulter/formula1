"""
Create setup file to make the app installable.
"""

from setuptools import find_packages, setup

setup(
    name='formula1_data',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
