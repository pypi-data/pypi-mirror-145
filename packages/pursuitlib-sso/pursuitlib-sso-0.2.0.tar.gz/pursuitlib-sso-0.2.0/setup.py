from setuptools import setup, find_packages
from pathlib import Path

directory = Path(__file__).parent

setup(
    name='pursuitlib-sso',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={'pursuitlib_sso': ['templates/pursuitlib/*', 'templates/pursuitlib/*/*']},
    install_requires=[
        'pursuitlib-django',
        'pysaml2'
    ],
    entry_points={},
    author='Pursuit',
    author_email='fr.pursuit@gmail.com',
    description='Provides SSO functions for Django',
    long_description=(directory / "README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/frPursuit/pursuitlib-python',
    license='All rights reserved',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7"
)
