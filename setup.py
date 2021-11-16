"""
Create setup file to make the app installable.
"""

from setuptools import fined_packages, setup

setup(
    name='formula1-data'
    version='1.0.0'
    packages=fined_packages()
    include_package_data=True
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
